from dataclasses import dataclass
import math
import mathutils

import bpy

from .. import utils

@dataclass(frozen=True)
class MetaRigCollectionInfo:
    name: str
    color_type: str
    row_index: int
    title: str

@dataclass(frozen=True)
class RigifySettings:
    bone_name: str | None  = None
    rigify_type: str | None  = None
    fk_coll: str | None  = None
    tweak_coll: str | None  = None
    copy_rot_axes: dict[str, bool] | None = None
    make_extra_ik_control: bool | None = None
    super_copy_widget_type: str | None = None
    pivot_pos: int | None = None
    secondary_layer_extra: str | None  = None
    skin_chain_pivot_pos: int | None  = None
    skin_chain_falloff_spherical: list[bool] | None  = None
    skin_control_orientation_bone: str | None  = None

@dataclass(frozen=True)
class ExtensionBone:
    name: str | list[str]
    bone_a: str | list[str]
    size_factor: float = 1.0
    axis_type: str = "local"# e.g., "global", "local", "armature"
    axis: str  = "Y" # e.g., "X", "Y", "Z"
    start: str = "tail" # e.g., "head", "tail"
    is_connected: bool = False
    parent: str | list[str] | None = None
    roll: float = 0.0

    def generate(self, ref: bpy.types.Armature, target: bpy.types.Armature) -> list[str] | None:
        """Generates the ExtensionBone extending from bone_a in the target armature."""
        if not ref or not target:
            print(f"[AetherBlend] Invalid armatures provided for ExtensionBone '{self.name}'.")
            return None
        
        ref_bones = ref.data.bones
        bone_a_ref = None
        bone_name_to_create = self.name
        
        if isinstance(self.bone_a, list):
            for i, ref_bone_name in enumerate(self.bone_a):
                bone_a_ref = ref_bones.get(ref_bone_name)
                if bone_a_ref:
                    if isinstance(self.name, list):
                        if i < len(self.name):
                            bone_name_to_create = self.name[i]
                        else:
                            bone_name_to_create = self.name[-1]  
                    break
        else:
            bone_a_ref = ref_bones.get(self.bone_a)
            if isinstance(self.name, list):
                bone_name_to_create = self.name[0]

        if not bone_a_ref:
            print(f"[AetherBlend] Reference bone '{self.bone_a}' not found in either armature for ExtensionBone '{bone_name_to_create}'.")
            return None
        
        if self.start == "tail":
            start_pos = bone_a_ref.tail_local.copy()
        else:  # "head"
            start_pos = bone_a_ref.head_local.copy()

        direction_vector = None
        if self.axis_type == "local":
            local_bone_matrix = bone_a_ref.matrix_local.to_3x3().inverted()
            if self.axis == "X":
                direction_vector = local_bone_matrix[0]
            elif self.axis == "Y":
                direction_vector = local_bone_matrix[1] 
            elif self.axis == "Z":
                direction_vector = local_bone_matrix[2]
        elif self.axis_type == "armature":
            armature_matrix = target.matrix_world.to_3x3().inverted()
            if self.axis == "X":
                direction_vector = armature_matrix[0]
            elif self.axis == "Y":
                direction_vector = armature_matrix[1]
            elif self.axis == "Z":
                direction_vector = armature_matrix[2]
        elif self.axis_type == "global":
            if self.axis == "X":
                direction_vector = mathutils.Vector((1.0, 0.0, 0.0))
            elif self.axis == "Y":
                direction_vector = mathutils.Vector((0.0, 1.0, 0.0))
            elif self.axis == "Z":
                direction_vector = mathutils.Vector((0.0, 0.0, 1.0))
        
        if not direction_vector:
            print(f"[AetherBlend] Invalid axis configuration for ExtensionBone '{bone_name_to_create}': axis_type='{self.axis_type}', axis='{self.axis}'.")
            return None
        
        ref_bone_length = bone_a_ref.length if bone_a_ref.length > 0 else 1.0
        extension_length = ref_bone_length * self.size_factor
        tail_pos = start_pos + direction_vector.normalized() * extension_length

        original_mode = bpy.context.object.mode
        bpy.context.view_layer.objects.active = target
        bpy.ops.object.mode_set(mode='EDIT')
        
        try:
            target_edit_bones = target.data.edit_bones
            
            if bone_name_to_create in target_edit_bones:
                target_edit_bones.remove(target_edit_bones[bone_name_to_create])

            new_bone = target_edit_bones.new(bone_name_to_create)
            new_bone.head = start_pos
            new_bone.tail = tail_pos
            new_bone.roll = math.radians(self.roll) if self.roll != 0.0 else 0.0

            if self.parent:
                if isinstance(self.parent, list):
                    for bone_name in self.parent:
                        parent_bone = target_edit_bones.get(bone_name)
                        if parent_bone and parent_bone != new_bone:
                            break
                else :
                    parent_bone = target_edit_bones.get(self.parent)

                if parent_bone:
                    new_bone.parent = parent_bone
                    new_bone.use_connect = self.is_connected
                else:
                    print(f"[AetherBlend] Warning: Parent bone '{self.parent}' not found for ExtensionBone '{bone_name_to_create}'.")
            
            created_name = new_bone.name  
            return [created_name]
            
        finally:
            bpy.ops.object.mode_set(mode=original_mode)

@dataclass(frozen=True)
class SkinBone:
    name: str
    bone_a: str
    parent: str | None = None
    size_factor: float = 1.0
    lead_bone: bool = False

@dataclass(frozen=True)
class ConnectBone:
    name: str | list[str]
    bone_a: str | list[str]
    bone_b: str | list[str]
    parent: str | list[str] | None = None
    is_connected: bool = False
    roll: float = 0.0

    def generate(self, ref: bpy.types.Armature, target: bpy.types.Armature) -> list[str] | None:
        """Generates the ConnectBone from bone_a.head to bone_b.head in target armature."""
        if not ref or not target:
            print(f"[AetherBlend] Invalid armatures provided for ConnectBone '{self.name}'.")
            return None
            
        ref_bones = ref.data.bones
        bone_a_ref = None
        bone_name_to_create = self.name
        
        if isinstance(self.bone_a, list):
            for i, ref_bone_name in enumerate(self.bone_a):
                bone_a_ref = ref_bones.get(ref_bone_name)
                if bone_a_ref:
                    if isinstance(self.name, list):
                        if i < len(self.name):
                            bone_name_to_create = self.name[i]
                        else:
                            bone_name_to_create = self.name[-1]  
                    break
        else:
            bone_a_ref = ref_bones.get(self.bone_a)
            if isinstance(self.name, list):
                bone_name_to_create = self.name[0]


        if isinstance(self.bone_b, list):
            for ref_bone_name in self.bone_b:
                bone_b_ref = ref_bones.get(ref_bone_name)
                if bone_b_ref:
                    break
        else:
            bone_b_ref = ref_bones.get(self.bone_b)

        if not bone_a_ref or not bone_b_ref:
            print(f"[AetherBlend] Cannot create ConnectBone '{bone_name_to_create}': reference bones '{self.bone_a}' or '{self.bone_b}' not found in source armature.")
            return None
        
        head_pos = bone_a_ref.head_local.copy()
        tail_pos = bone_b_ref.head_local.copy()
        
        original_mode = bpy.context.object.mode
        bpy.context.view_layer.objects.active = target
        bpy.ops.object.mode_set(mode='EDIT')
        
        try:
            target_edit_bones = target.data.edit_bones
            
            if bone_name_to_create in target_edit_bones:
                target_edit_bones.remove(target_edit_bones[bone_name_to_create])

            new_bone = target_edit_bones.new(bone_name_to_create)
            new_bone.head = head_pos
            new_bone.tail = tail_pos
            new_bone.roll = math.radians(self.roll) if self.roll != 0.0 else 0.0
            
            if self.parent:
                if isinstance(self.parent, list):
                    for bone_name in self.parent:
                        parent_bone = target_edit_bones.get(bone_name)
                        if parent_bone  and parent_bone != new_bone:    
                            break
                else :
                    parent_bone = target_edit_bones.get(self.parent)
                if parent_bone:
                    new_bone.parent = parent_bone
                    new_bone.use_connect = self.is_connected
                else:
                    print(f"[AetherBlend] Warning: Parent bone '{self.parent}' not found for ConnectBone '{bone_name_to_create}'.")
            
            created_name = new_bone.name  
            return [created_name]
            
        finally:
            bpy.ops.object.mode_set(mode=original_mode)

@dataclass(frozen=True)
class BridgeBone:
    bone_a: str
    bone_b: str
    segments: int = 1
    offset_factor: mathutils.Vector = mathutils.Vector((0.0, 0.0, 0.0))
    is_connected: bool = True

@dataclass(frozen=True)
class TrackToBone:
    origin_name: str 
    target_name: str
    custom_space: str
    parent_name: str | None

@dataclass(frozen=True)
class BoneChainInfo:
    ffxiv_bones: list[str] | None = None
    gen_bones: dict[str, RigifySettings | None] | None = None
    parent_bone: str | None = None
    bone_extensions: ExtensionBone | None = None
    roll: float | None = 0.0
    extend_last: bool = False
    extension_factor: float = 0.0
    skin_bones: list[SkinBone] | None = None
    bridge_bones: list[BridgeBone] | None = None

@dataclass(frozen=True)
class EyeBone:
    outer_bones: list[SkinBone]
    bridges: list[BridgeBone]
    eye_name: str
    eye_collection: str
    parent_bone: str | None = None
    bone_settings: dict[str, RigifySettings | None] | None = None

@dataclass(frozen=True)
class GenerativeBone:
    ref: str # e.g. "src" or "tgt"
    data: ConnectBone | ExtensionBone
    req_bones: list[str] | None = None
    settings: RigifySettings | None = None
    b_collection: str | None = None
    is_optional: bool = False


    def generate(self, ref: bpy.types.Armature, tgt: bpy.types.Armature) -> list[str] | None:
        """Generates the bone in the given armature and returns the new bone's name."""
        generated_bones = self.data.generate(ref, tgt)

        if generated_bones and self.b_collection:
           utils.armature.b_collection.assign_bones(tgt, generated_bones, self.b_collection)

        return generated_bones

