import bpy

from abc import ABC
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .generators import BoneGenerator

from . import rigify
from .constraints import Constraint, CopyTransformsConstraint
from .. import utils


@dataclass
class PoseOperations:
    """Groups all pose mode operations for a single bone."""
    rigify_settings: 'rigify.types.rigify_type | None' = None
    constraints: 'list[Constraint] | None' = None
    b_collection: str | None = None

    def execute(self, pose_bone: bpy.types.PoseBone, armature: bpy.types.Object):
        """Executes all pose operations on the given pose bone."""
        try:
            if self.rigify_settings:
                self.rigify_settings.apply(pose_bone, armature)
            
            if self.constraints:
                for constraint in self.constraints:
                    constraint.apply(pose_bone, armature)
            
            if self.b_collection:
                utils.armature.b_collection.assign_bones(armature, [pose_bone.name], self.b_collection)
        except Exception as e:
            print(f"[AetherBlend] Error executing PoseOperations for bone: {e}")

@dataclass
class TransformLink:
    """Links a bone to a target for rigging purposes."""
    target: str
    bone: str
    retarget: str | None = None

    def to_pose_operations(self) -> dict[str, list[PoseOperations]]:
        """Convert this TransformLink to PoseOperations."""
        pose_operations_dict: dict[str, list[PoseOperations]] = {}

        ff_bone = self.bone
        mch_bone = f"MCH-{ff_bone}"
        if ff_bone not in pose_operations_dict:
            pose_operations_dict[ff_bone] = []
        pose_operations_dict[ff_bone].append(
            PoseOperations(
                # rigify_settings=rigify.types.basic_raw_copy(True),
                constraints=[CopyTransformsConstraint(mch_bone, name=f"AetherBlend-CopyTransform@MCH-{ff_bone}", remove_target_shear=True)]
            )
        )

        if mch_bone not in pose_operations_dict:
            pose_operations_dict[mch_bone] = []
        pose_operations_dict[mch_bone].append(
            PoseOperations(
                rigify_settings=rigify.types.basic_raw_copy(True, self.target)
            )
        )
        return pose_operations_dict
    

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
    transform_link: list[TransformLink] | None = None
    bones: 'list[BoneGenerator] | None' = None
    
    def check(self, armature: bpy.types.Object) -> bool:
        """Check if all required bones exist in the armature for this bone group."""
        future_bones = []
        
        for bone_gen in self.bones:
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
    
    def generate(self, armature: bpy.types.Object, data: dict | None = None) -> list[str]:
        """Generate all bones in this group."""
        generated_bones = []
        
        for bone_gen in self.bones:
            new_bones = bone_gen.generate(armature, data=data)
            if new_bones:
                generated_bones.extend(new_bones)
        
        return generated_bones
    
    def execute(self, armature: bpy.types.Object, data: dict | None = None) -> tuple[list[str], dict[str, list[PoseOperations]]]:
        """Execute the full generation process for this bone group."""
        # Check if bone group can theoriticlly be generated
        if not self.check(armature):
            print(f"[AetherBlend] BoneGroup '{self.name}' check failed - missing required bones")
            return [], {}
        
        bpy.ops.object.mode_set(mode='EDIT')
        
        # Generate bones
        generated_bones = self.generate(armature, data=data)
        
        # Collect Pose Operations
        pose_operations_dict: dict[str, list[PoseOperations]] = {}

        # Add TransformLink operations
        for link_item in self.transform_link or []:
            for bone_name, operations in link_item.to_pose_operations().items():
                if bone_name not in pose_operations_dict:
                    pose_operations_dict[bone_name] = []
                pose_operations_dict[bone_name].extend(operations)
        
        # Add BoneGenerator pose operations
        for bone_gen in self.bones:
            # Collect dynamic pose operations (empty dict for most generators)
            dynamic_ops = bone_gen.get_dynamic_pose_operations()
            for bone_name, operations in dynamic_ops.items():
                if bone_name not in pose_operations_dict:
                    pose_operations_dict[bone_name] = []
                pose_operations_dict[bone_name].extend(operations)
            
            # Collect dynamic transform links (empty list for most generators)
            dynamic_links = bone_gen.get_dynamic_transform_links()
            for link_item in dynamic_links:
                for bone_name, operations in link_item.to_pose_operations().items():
                    if bone_name not in pose_operations_dict:
                        pose_operations_dict[bone_name] = []
                    pose_operations_dict[bone_name].extend(operations)
            
            # Add static pose operations from the generator
            if bone_gen.pose_operations:
                if bone_gen.name not in pose_operations_dict:
                    pose_operations_dict[bone_gen.name] = []
                pose_operations_dict[bone_gen.name].append(bone_gen.pose_operations)
        
        return generated_bones, pose_operations_dict
    
@dataclass(frozen=True)
class AetherRigGenerator:
    """Generates an armature based on defined bone groups."""
    name: str
    color_sets: 'list[dict[str, rigify.ColorSet]] | None' = None
    ui_collections: 'list[dict[str, rigify.BoneCollection]] | None' = None
    overrides: 'list[dict[str, Override]] | None' = None
    bone_groups: 'list[dict[str, list[BoneGroup]]] | None' = None

    def getColorSets(self) -> dict[str, rigify.ColorSet]:
        """Combine all color sets into a single dictionary."""
        combined: dict[str, rigify.ColorSet] = {}
        for cs_dict in self.color_sets or []:
            combined.update(cs_dict)
        return combined
    
    def getUICollections(self) -> dict[str, rigify.BoneCollection]:
        """Combine all UI collections into a single dictionary."""
        combined: dict[str, rigify.BoneCollection] = {}
        for ui_dict in self.ui_collections or []:
            combined.update(ui_dict)
        return combined
    
    def getOverrides(self) -> dict[str, Override]:
        """Combine all widget overrides into a single dictionary."""
        combined: dict[str, Override] = {}
        for ov_dict in self.overrides or []:
            combined.update(ov_dict)
        return combined
    
    def getBoneGroups(self) -> dict[str, list[BoneGroup]]:
        """Combine all bone groups into a single dictionary."""
        combined: dict[str, list[BoneGroup]] = {}
        for bg_dict in self.bone_groups or []:
            combined.update(bg_dict)
        return combined

