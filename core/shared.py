import bpy

from abc import ABC
from dataclasses import dataclass, field
from typing import TYPE_CHECKING
from typing import Literal



if TYPE_CHECKING:
    from .generators import BoneGenerator

from .operations import ABOperation, PoseOperations, PoseOperationsStack, ConstraintOperation, TransformLink
from . import rigify
from .constraints import Constraint, CopyTransformsConstraint
from .. import utils
from .generators import BoneGenerator

ModuleType = Literal["Generator", "Patch","UI-Addon"]
  
    

class Override(ABC):
    """Overrides properties of a bone."""
    bone: str

    def execute(self, armature: bpy.types.Object) -> None:
        """Applies the override to the given edit bone."""
        pass

@dataclass
class WidgetOverride(Override):
    """Overrides the widget of a bone."""
    bone: str
    custom_object: str | None = None
    translation: tuple[float, float, float] = (0.0, 0.0, 0.0)
    rotation: tuple[float, float, float] = (0.0, 0.0, 0.0)
    scale: tuple[float, float, float] = (1.0, 1.0, 1.0)
    scale_factor: float = 1.0
    override_transform: str | None = None  # Bone Name
    affect_gizmo: bool = False
    use_as_pivot: bool = False
    scale_to_bone_length: bool = True
    wireframe: bool = False
    wire_width: float = 1.0


    def execute(self, armature: bpy.types.Object) -> None:
        """Applies the widget override to the given pose bone."""
        pose_bone = armature.pose.bones.get(self.bone)
        if not pose_bone:
            print(f"[AetherBlend] WidgetOverride bone '{self.bone}' not found in armature.")
            return
        
        scale = (self.scale[0] * self.scale_factor, self.scale[1] * self.scale_factor, self.scale[2] * self.scale_factor)

        try:
            if self.custom_object:
                pose_bone.custom_shape = self.custom_object
            pose_bone.custom_shape_translation = self.translation
            pose_bone.custom_shape_rotation_euler = self.rotation
            pose_bone.custom_shape_scale_xyz = scale
            pose_bone.custom_shape_transform = self.override_transform
            pose_bone.use_transform_at_custom_shape = self.affect_gizmo      ## 5.0
            pose_bone.use_transform_around_custom_shape = self.use_as_pivot  ## 5.0
            pose_bone.use_custom_shape_bone_size = self.scale_to_bone_length
            ##pose_bone.show_wire = self.wireframe  ## 5.0
            pose_bone.custom_shape_wire_width = self.wire_width
        except Exception as e:
            print(f"[AetherBlend] Error applying WidgetOverride for bone '{pose_bone.name}': {e}")

@dataclass
class PropOverride(Override):
    """Overrides a custom property of a bone."""
    bone: str
    property_name: str
    value: float | int | str | bool

    def execute(self, armature: bpy.types.Object) -> None:
        """Applies the property override to the given pose bone."""
        pose_bone = armature.pose.bones.get(self.bone)
        if not pose_bone:
            print(f"[AetherBlend] PropOverride bone '{self.bone}' not found in armature.")
            return
        
        try:
            pose_bone[self.property_name] = self.value
        except Exception as e:
            print(f"[AetherBlend] Error applying PropOverride for bone '{pose_bone.name}': {e}")


@dataclass
class BoneGroup:
    """A group of bone generators that can be executed together."""
    name: str
    description: str = ""
    transform_link: list[TransformLink] = field(default_factory=list)
    generators: list[BoneGenerator] = field(default_factory=list)
    operations: list[ABOperation] = field(default_factory=list)

    def __post_init__(self):
        # Defensive copies prevent template-level singletons from sharing runtime state.
        self.transform_link = list(self.transform_link)
        self.generators = list(self.generators)
        self.operations = list(self.operations)
    
    def check(self, armature: bpy.types.Object) -> bool:
        """Check if all required bones exist in the armature for this bone group."""
        future_bones = []
        
        for bone_gen in self.generators:
            future_bones.append(bone_gen.name)
            
            if bone_gen.req_bones:
                for req_bone in bone_gen.req_bones:
                    # Check if bone will be created in this group or already exists
                    if req_bone not in future_bones:
                        if req_bone not in armature.data.bones:
                            if bone_gen.is_optional:
                                future_bones.remove(bone_gen.name)
                                continue
                            return False
        return True
    
    def generate(self, armature: bpy.types.Object, data: dict | None = None) -> tuple[list[str], list[ABOperation]]:
        """Generate all bones in this group."""

        generated_bones: list[str] = []
        generated_operations: list[ABOperation] = list(self.operations)

        for bone_gen in self.generators:
            # Generators are template singletons; isolate runtime-emitted operations per execution.
            static_operations = list(bone_gen.operations)
            bone_gen.operations = []
            new_bones = bone_gen.generate(armature, data=data)
            runtime_operations = list(bone_gen.operations)
            bone_gen.operations = static_operations

            if static_operations:
                generated_operations.extend(static_operations)
            if runtime_operations:
                generated_operations.extend(runtime_operations)
            if new_bones:
                generated_bones.extend(new_bones)

        return generated_bones, generated_operations
        
    
    def execute(self, armature: bpy.types.Object, data: dict | None = None) -> tuple[list[str], dict[str, list[PoseOperations]], list[ABOperation]]:
        """Execute the full generation process for this bone group."""
        # Check if bone group can theoriticlly be generated
        if not self.check(armature):
            print(f"[AetherBlend] BoneGroup '{self.name}' check failed - missing required bones")
            return [], {}, []
        
        bpy.ops.object.mode_set(mode='EDIT')
        
        # Generate bones and collect runtime operations for this execution only.
        generated_bones, generated_operations = self.generate(armature, data=data)
        
        # Collect Pose Operations
        pose_operations_dict: dict[str, list[PoseOperations]] = {}

        # # Add TransformLink operations
        # bpy.ops.object.mode_set(mode='OBJECT')
        # for link_item in self.transform_link:
        #     link_item.mark_linked(armature)
        #     for bone_name, operations in link_item.to_pose_operations().items():
        #         if bone_name not in pose_operations_dict:
        #             pose_operations_dict[bone_name] = []
        #         pose_operations_dict[bone_name].extend(operations)

        bpy.ops.object.mode_set(mode='OBJECT')
        for link_item in self.transform_link:
            link_item.mark_linked(armature)
            for operation in link_item.to_ABOperation():
                generated_operations.append(operation)
        
        # Add BoneGenerator pose operations
        for bone_gen in self.generators:
            # Collect dynamic pose operations (empty dict for most generators)
            dynamic_ops = bone_gen.get_dynamic_pose_operations()
            for bone_name, operations in dynamic_ops.items():
                if bone_name not in pose_operations_dict:
                    pose_operations_dict[bone_name] = []
                pose_operations_dict[bone_name].extend(operations)
            
            # Collect dynamic transform links (empty list for most generators)
            dynamic_links = bone_gen.get_dynamic_transform_links()
            for link_item in dynamic_links:
                link_item.mark_linked(armature)
                for bone_name, operations in link_item.to_pose_operations().items():
                    if bone_name not in pose_operations_dict:
                        pose_operations_dict[bone_name] = []
                    pose_operations_dict[bone_name].extend(operations)
            
            if bone_gen.pose_operations:
                if bone_gen.name not in pose_operations_dict:
                    pose_operations_dict[bone_gen.name] = []
                pose_operations_dict[bone_gen.name].append(bone_gen.pose_operations)
        
        return generated_bones, pose_operations_dict, generated_operations

@dataclass
class RigModule:
    """Defines a rig module and its behavior category."""
    name: str
    type: ModuleType
    bone_groups: list[BoneGroup]
    ui: rigify.settings.UI_Collections | None = None
    operations: list[ABOperation] = field(default_factory=list)

    def execute(self, armature: bpy.types.Object, data: dict) -> tuple[bool, PoseOperationsStack, rigify.settings.UI_Collections | None, list[ABOperation]]:
        bpy.context.view_layer.objects.active = armature
        pose_op_stack = PoseOperationsStack()
        module_operations: list[ABOperation] = list(self.operations)
        integrity = False
        if self.type == "Patch" or self.type == "UI-Addon":
            integrity = True
        for bone_group in self.bone_groups:
            bones, pose_ops, operations = bone_group.execute(armature, data)

            if not bones and not pose_ops:
                continue 
                
            integrity = True
            pose_op_stack.merge(PoseOperationsStack(stack = pose_ops))
            module_operations.extend(operations or [])

            
        return integrity, pose_op_stack, self.ui, module_operations
        

class AetherRigGenerator:
    """Generates an armature based on ordered module priority groups."""
    name: str
    modules: 'list[list[RigModule]]'
    color_sets: 'dict[str, rigify.ColorSet]'
    overrides: 'list[dict[str, Override]] | None' = None
    

    def __init__(self, name: str, color_sets: 'list[dict[str, rigify.ColorSet]] | None' = None, overrides: 'list[dict[str, Override]] | None' = None, modules: 'list[list[RigModule]] | None' = None):
        self.name = name
        self.color_sets = color_sets
        self.overrides = overrides
        
        self.set_modules(modules or [])
    
    def getOverrides(self) -> dict[str, Override]:
        """Combine all widget overrides into a single dictionary."""
        combined: dict[str, Override] = {}
        for ov_dict in self.overrides or []:
            combined.update(ov_dict)
        return combined
    
    def set_modules(self, modules: 'list[list[RigModule]]'):
        """Store the already-resolved module priority groups."""
        self.modules = [list(group) for group in modules if group]

@dataclass(frozen=True)
class Template():
    """Defines a rig template with its properties and modules."""
    name: str
    overrides: 'list[dict[str, Override]] | None'
    modules: 'list[list[RigModule]]'
