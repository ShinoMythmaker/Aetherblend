import bpy
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .generators import BoneGenerator

from . import rigify
from .constraints import Constraint, CopyTransformsConstraint
from .. import utils


@dataclass
class link:
    """Links a bone to a target for rigging purposes."""
    target: str
    bone: str
    retarget: str | None = None


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
class BoneGroup:
    """A group of bone generators that can be executed together."""
    name: str
    description: str = ""
    linking: list[link] | None = None
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
        # Check if all required bones exist
        if not self.check(armature):
            print(f"[AetherBlend] BoneGroup '{self.name}' check failed - missing required bones")
            return [], {}
        
        # Switch to edit mode if needed
        current_mode = bpy.context.object.mode if bpy.context.object else None
        if current_mode != 'EDIT':
            bpy.ops.object.mode_set(mode='EDIT')
        
        # Generate bones
        generated_bones = self.generate(armature, data=data)
        
        # Collect pose operations by bone name (allowing multiple operations per bone)
        pose_operations_dict: dict[str, list[PoseOperations]] = {}

        for link_item in self.linking or []:
            ff_bone = link_item.bone
            mch_bone = f"MCH-{ff_bone}"
            if ff_bone not in pose_operations_dict:
                pose_operations_dict[ff_bone] = []
            pose_operations_dict[ff_bone].append(
                PoseOperations(
                    # rigify_settings=rigify.types.basic_raw_copy(True),
                    constraints=[CopyTransformsConstraint(mch_bone, name=f"AetherBlend-CopyTransform@MCH-{ff_bone}")]
                )
            )

            if mch_bone not in pose_operations_dict:
                pose_operations_dict[mch_bone] = []
            pose_operations_dict[mch_bone].append(
                PoseOperations(
                    rigify_settings=rigify.types.basic_raw_copy(True, link_item.target)
                )
            )
        
        for bone_gen in self.bones:
            # Only add to dict if there are operations to perform
            if bone_gen.pose_operations:
                if bone_gen.name not in pose_operations_dict:
                    pose_operations_dict[bone_gen.name] = []
                pose_operations_dict[bone_gen.name].append(bone_gen.pose_operations)
        
        return generated_bones, pose_operations_dict
    
@dataclass
class AetherRigGenerator:
    """Generates an armature based on defined bone groups."""
    name: str
    color_sets: 'list[rigify.ColorSet] | None' = None
    b_collections: 'list[rigify.BoneCollection] | None' = None
    bone_groups: 'list[BoneGroup] | None' = None

    def generate_meta_rig(self, armature: bpy.types.Object, data: dict | None = None) -> 'dict[str, list[PoseOperations]]':
        """Generate the meta-rig for Rigify."""
        # TODO: Implementation will be added
        pass
    
    def generate_rigify_rig(self, armature: bpy.types.Object, data: dict | None = None) -> None:
        """Generate the final Rigify rig."""
        # TODO: Implementation will be added
        pass

