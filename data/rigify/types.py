"""
Rigify type classes for AetherBlend.

This module defines classes for commonly used rigify types with their specific
parameter application methods. Each class inherits from the base rigify_type class.
Each rigify type stores its own parameters and can be instantiated directly.
"""

import bpy
from dataclasses import dataclass, field


class rigify_type:
    """Base class for rigify types."""
    
    def apply(self, armature: bpy.types.Object) -> None:
        """
        Apply rigify settings to a bone.
        
        Args:
            armature: The armature object
        """
        raise NotImplementedError("Subclasses must implement apply()")


@dataclass
class limbs_leg(rigify_type):
    """Rigify type: limbs.leg - Used for leg rigs."""
    bone_name: str = None
    fk_coll: str = None
    
    def apply(self, armature: bpy.types.Object) -> None:
        """Apply leg rig settings."""
        bpy.context.view_layer.objects.active = armature
        bpy.ops.object.mode_set(mode='POSE')
        
        pose_bone = armature.pose.bones.get(self.bone_name)

        armature.data.bones.active = pose_bone.bone
        
        if pose_bone:
            pose_bone.rigify_type = "limbs.leg"
            
            if self.fk_coll:
                try:
                    rigify_params = pose_bone.rigify_parameters
                    rigify_params.fk_coll_refs.clear()
                    
                    if self.fk_coll in armature.data.collections:
                        bpy.ops.pose.rigify_collection_ref_add(prop_name="fk_coll_refs")
                        if len(rigify_params.fk_coll_refs) > 0:
                            fk_ref = rigify_params.fk_coll_refs[-1]
                            fk_ref.name = self.fk_coll
                except Exception as e:
                    print(f"[AetherBlend] Error setting FK collection: {e}")
        
        bpy.ops.object.mode_set(mode='OBJECT')

@dataclass
class limbs_arm(rigify_type):
    """Rigify type: limbs.arm - Used for arm rigs."""
    bone_name: str = None
    fk_coll: str = None
    tweak_coll: str = None
    
    def apply(self, armature: bpy.types.Object) -> None:
        """Apply arm rig settings."""
        bpy.context.view_layer.objects.active = armature
        
        pose_bone = armature.pose.bones.get(self.bone_name)
    
        armature.data.bones.active = pose_bone.bone

        if pose_bone:
            pose_bone.rigify_type = "limbs.arm"
            
            if self.fk_coll:
                try:
                    rigify_params = pose_bone.rigify_parameters
                    rigify_params.fk_coll_refs.clear()
                    
                    if self.fk_coll in armature.data.collections:
                        bpy.ops.pose.rigify_collection_ref_add(prop_name="fk_coll_refs")
                        if len(rigify_params.fk_coll_refs) > 0:
                            fk_ref = rigify_params.fk_coll_refs[-1]
                            fk_ref.name = self.fk_coll
                except Exception as e:
                    print(f"[AetherBlend] Error setting FK collection: {e}")
            
            if self.tweak_coll:
                try:
                    rigify_params = pose_bone.rigify_parameters
                    rigify_params.tweak_coll_refs.clear()
                    
                    if self.tweak_coll in armature.data.collections:
                        bpy.ops.pose.rigify_collection_ref_add(prop_name="tweak_coll_refs")
                        if len(rigify_params.tweak_coll_refs) > 0:
                            tweak_ref = rigify_params.tweak_coll_refs[-1]
                            tweak_ref.name = self.tweak_coll
                except Exception as e:
                    print(f"[AetherBlend] Error setting tweak collection: {e}")
        
        bpy.ops.object.mode_set(mode='OBJECT')

@dataclass
class limbs_super_finger(rigify_type):
    """Rigify type: limbs.super_finger - Used for finger and toe rigs."""
    bone_name: str = None
    tweak_coll: str = None
    make_extra_ik_control: bool = False
    
    def apply(self, armature: bpy.types.Object) -> None:
        """Apply super finger rig settings."""
        bpy.context.view_layer.objects.active = armature
        bpy.ops.object.mode_set(mode='POSE')
        
        pose_bone = armature.pose.bones.get(self.bone_name)
        if pose_bone:
            pose_bone.rigify_type = "limbs.super_finger"
            
            if self.tweak_coll:
                try:
                    rigify_params = pose_bone.rigify_parameters
                    rigify_params.tweak_coll_refs.clear()
                    
                    if self.tweak_coll in armature.data.collections:
                        bpy.ops.pose.rigify_collection_ref_add(prop_name="tweak_coll_refs")
                        if len(rigify_params.tweak_coll_refs) > 0:
                            tweak_ref = rigify_params.tweak_coll_refs[-1]
                            tweak_ref.name = self.tweak_coll
                except Exception as e:
                    print(f"[AetherBlend] Error setting tweak collection: {e}")
            
            if self.make_extra_ik_control:
                try:
                    rigify_params = pose_bone.rigify_parameters
                    rigify_params.make_extra_ik_control = self.make_extra_ik_control
                except Exception as e:
                    print(f"[AetherBlend] Error setting make_extra_ik_control: {e}")
        
        bpy.ops.object.mode_set(mode='OBJECT')

@dataclass
class spines_basic_spine(rigify_type):
    """Rigify type: spines.basic_spine - Used for spine rigs."""
    bone_name: str = None
    fk_coll: str = None
    tweak_coll: str = None
    pivot_pos: int = None
    
    def apply(self, armature: bpy.types.Object) -> None:
        """Apply basic spine rig settings."""
        bpy.context.view_layer.objects.active = armature
        bpy.ops.object.mode_set(mode='POSE')
        
        pose_bone = armature.pose.bones.get(self.bone_name)
        if pose_bone:
            pose_bone.rigify_type = "spines.basic_spine"
            
            if self.fk_coll:
                try:
                    rigify_params = pose_bone.rigify_parameters
                    rigify_params.fk_coll_refs.clear()
                    
                    if self.fk_coll in armature.data.collections:
                        bpy.ops.pose.rigify_collection_ref_add(prop_name="fk_coll_refs")
                        if len(rigify_params.fk_coll_refs) > 0:
                            fk_ref = rigify_params.fk_coll_refs[-1]
                            fk_ref.name = self.fk_coll
                except Exception as e:
                    print(f"[AetherBlend] Error setting FK collection: {e}")
            
            if self.tweak_coll:
                try:
                    rigify_params = pose_bone.rigify_parameters
                    rigify_params.tweak_coll_refs.clear()
                    
                    if self.tweak_coll in armature.data.collections:
                        bpy.ops.pose.rigify_collection_ref_add(prop_name="tweak_coll_refs")
                        if len(rigify_params.tweak_coll_refs) > 0:
                            tweak_ref = rigify_params.tweak_coll_refs[-1]
                            tweak_ref.name = self.tweak_coll
                except Exception as e:
                    print(f"[AetherBlend] Error setting tweak collection: {e}")
            
            if self.pivot_pos is not None:
                try:
                    rigify_params = pose_bone.rigify_parameters
                    rigify_params.pivot_pos = self.pivot_pos
                except Exception as e:
                    print(f"[AetherBlend] Error setting pivot_pos: {e}")
        
        bpy.ops.object.mode_set(mode='OBJECT')

@dataclass
class spines_super_head(rigify_type):
    """Rigify type: spines.super_head - Used for neck/head rigs."""
    bone_name: str = None
    tweak_coll: str = None
    
    def apply(self, armature: bpy.types.Object) -> None:
        """Apply super head rig settings."""
        bpy.context.view_layer.objects.active = armature
        bpy.ops.object.mode_set(mode='POSE')
        
        pose_bone = armature.pose.bones.get(self.bone_name)
        if pose_bone:
            pose_bone.rigify_type = "spines.super_head"
            
            if self.tweak_coll:
                try:
                    rigify_params = pose_bone.rigify_parameters
                    rigify_params.tweak_coll_refs.clear()
                    
                    if self.tweak_coll in armature.data.collections:
                        bpy.ops.pose.rigify_collection_ref_add(prop_name="tweak_coll_refs")
                        if len(rigify_params.tweak_coll_refs) > 0:
                            tweak_ref = rigify_params.tweak_coll_refs[-1]
                            tweak_ref.name = self.tweak_coll
                except Exception as e:
                    print(f"[AetherBlend] Error setting tweak collection: {e}")
        
        bpy.ops.object.mode_set(mode='OBJECT')

@dataclass
class spines_basic_tail(rigify_type):
    """Rigify type: spines.basic_tail - Used for tail rigs."""
    bone_name: str = None
    use_x: bool = False
    use_y: bool = False
    use_z: bool = False
    
    def apply(self, armature: bpy.types.Object) -> None:
        """Apply basic tail rig settings."""
        bpy.context.view_layer.objects.active = armature
        bpy.ops.object.mode_set(mode='POSE')
        
        pose_bone = armature.pose.bones.get(self.bone_name)
        if pose_bone:
            pose_bone.rigify_type = "spines.basic_tail"
            
            try:
                rigify_params = pose_bone.rigify_parameters
                rigify_params.copy_rotation_axes[0] = self.use_x
                rigify_params.copy_rotation_axes[1] = self.use_y
                rigify_params.copy_rotation_axes[2] = self.use_z
            except Exception as e:
                print(f"[AetherBlend] Error setting copy rotation axes: {e}")
        
        bpy.ops.object.mode_set(mode='OBJECT')

@dataclass
class basic_super_copy(rigify_type):
    """Rigify type: basic.super_copy - Used for simple control bones."""
    bone_name: str = None
    widget_type: str = None
    
    def apply(self, armature: bpy.types.Object) -> None:
        """Apply super copy rig settings."""
        bpy.context.view_layer.objects.active = armature
        bpy.ops.object.mode_set(mode='POSE')
        
        pose_bone = armature.pose.bones.get(self.bone_name)
        if pose_bone:
            pose_bone.rigify_type = "basic.super_copy"
            
            if self.widget_type:
                try:
                    rigify_params = pose_bone.rigify_parameters
                    rigify_params.super_copy_widget_type = self.widget_type
                except Exception as e:
                    print(f"[AetherBlend] Error setting widget type: {e}")
        
        bpy.ops.object.mode_set(mode='OBJECT')

@dataclass
class skin_stretchy_chain(rigify_type):
    """Rigify type: skin.stretchy_chain - Used for facial and stretchy chains."""
    bone_name: str = None
    skin_chain_pivot_pos: int = None
    skin_control_orientation_bone: str = None
    skin_chain_falloff: list = None
    skin_chain_falloff_length: bool = None
    skin_chain_falloff_spherical: list = None
    skin_chain_priority: int = None
    skin_chain_use_scale: list = None
    primary_layer_extra: str = None
    secondary_layer_extra: str = None
    
    def apply(self, armature: bpy.types.Object) -> None:
        """Apply stretchy chain rig settings."""
        bpy.context.view_layer.objects.active = armature
        bpy.ops.object.mode_set(mode='POSE')
        
        pose_bone = armature.pose.bones.get(self.bone_name)
        if pose_bone:
            pose_bone.rigify_type = "skin.stretchy_chain"
            
            rigify_params = pose_bone.rigify_parameters
            
            if self.skin_chain_pivot_pos is not None:
                rigify_params.skin_chain_pivot_pos = self.skin_chain_pivot_pos
            if self.skin_control_orientation_bone is not None:
                rigify_params.skin_control_orientation_bone = self.skin_control_orientation_bone
            if self.skin_chain_falloff is not None:
                rigify_params.skin_chain_falloff = self.skin_chain_falloff
            if self.skin_chain_falloff_length is not None:
                rigify_params.skin_chain_falloff_length = self.skin_chain_falloff_length
            if self.skin_chain_falloff_spherical is not None:
                rigify_params.skin_chain_falloff_spherical = self.skin_chain_falloff_spherical
            if self.skin_chain_priority is not None:
                rigify_params.skin_chain_priority = self.skin_chain_priority
            if self.skin_chain_use_scale is not None:
                rigify_params.skin_chain_use_scale = self.skin_chain_use_scale
            
            if self.primary_layer_extra is not None:
                rigify_params.skin_primary_layers_extra = True
                rigify_params.skin_primary_coll_refs.clear()
                if self.primary_layer_extra in armature.data.collections:
                    bpy.ops.pose.rigify_collection_ref_add(prop_name="skin_primary_coll_refs")
                    if len(rigify_params.skin_primary_coll_refs) > 0:
                        skin_ref = rigify_params.skin_primary_coll_refs[-1]
                        skin_ref.name = self.primary_layer_extra
            
            if self.secondary_layer_extra is not None:
                rigify_params.skin_secondary_layers_extra = True
                rigify_params.skin_secondary_coll_refs.clear()
                if self.secondary_layer_extra in armature.data.collections:
                    bpy.ops.pose.rigify_collection_ref_add(prop_name="skin_secondary_coll_refs")
                    if len(rigify_params.skin_secondary_coll_refs) > 0:
                        skin_ref = rigify_params.skin_secondary_coll_refs[-1]
                        skin_ref.name = self.secondary_layer_extra
        
        bpy.ops.object.mode_set(mode='OBJECT')

@dataclass
class skin_basic_chain(rigify_type):
    """Rigify type: skin.basic_chain - Used for basic skin chains."""
    bone_name: str = None
    skin_chain_priority: int = None
    
    def apply(self, armature: bpy.types.Object) -> None:
        """Apply basic chain rig settings."""
        bpy.context.view_layer.objects.active = armature
        bpy.ops.object.mode_set(mode='POSE')
        
        pose_bone = armature.pose.bones.get(self.bone_name)
        if pose_bone:
            pose_bone.rigify_type = "skin.basic_chain"
            
            if self.skin_chain_priority is not None:
                rigify_params = pose_bone.rigify_parameters
                rigify_params.skin_chain_priority = self.skin_chain_priority
        
        bpy.ops.object.mode_set(mode='OBJECT')

@dataclass
class skin_glue(rigify_type):
    """Rigify type: skin.glue - Used for glue bones in facial rigs."""
    bone_name: str = None
    relink_constraints: bool = None
    skin_glue_use_tail: bool = None
    skin_glue_tail_reparent: bool = None
    skin_glue_add_constraint: str = None
    skin_glue_add_constraint_influence: float = None
    
    def apply(self, armature: bpy.types.Object) -> None:
        """Apply glue rig settings."""
        bpy.context.view_layer.objects.active = armature
        bpy.ops.object.mode_set(mode='POSE')
        
        pose_bone = armature.pose.bones.get(self.bone_name)
        if pose_bone:
            pose_bone.rigify_type = "skin.glue"
            
            rigify_params = pose_bone.rigify_parameters
            
            if self.relink_constraints is not None:
                rigify_params.relink_constraints = self.relink_constraints
            if self.skin_glue_use_tail is not None:
                rigify_params.skin_glue_use_tail = self.skin_glue_use_tail
            if self.skin_glue_tail_reparent is not None:
                rigify_params.skin_glue_tail_reparent = self.skin_glue_tail_reparent
            if self.skin_glue_add_constraint is not None:
                rigify_params.skin_glue_add_constraint = self.skin_glue_add_constraint
            if self.skin_glue_add_constraint_influence is not None:
                rigify_params.skin_glue_add_constraint_influence = self.skin_glue_add_constraint_influence
        
        bpy.ops.object.mode_set(mode='OBJECT')

@dataclass
class skin_anchor(rigify_type):
    """Rigify type: skin.anchor - Used for anchor bones in facial rigs."""
    bone_name: str = None
    pivot_master_widget_type: str = None
    
    def apply(self, armature: bpy.types.Object) -> None:
        """Apply anchor rig settings."""
        bpy.context.view_layer.objects.active = armature
        bpy.ops.object.mode_set(mode='POSE')
        
        pose_bone = armature.pose.bones.get(self.bone_name)
        if pose_bone:
            pose_bone.rigify_type = "skin.anchor"
            
            if self.pivot_master_widget_type is not None:
                rigify_params = pose_bone.rigify_parameters
                rigify_params.pivot_master_widget_type = self.pivot_master_widget_type
        
        bpy.ops.object.mode_set(mode='OBJECT')

@dataclass
class face_skin_eye(rigify_type):
    """Rigify type: face.skin_eye - Used for eye rigs."""
    bone_name: str = None
    
    def apply(self, armature: bpy.types.Object) -> None:
        """Apply skin eye rig settings."""
        bpy.context.view_layer.objects.active = armature
        bpy.ops.object.mode_set(mode='POSE')
        
        pose_bone = armature.pose.bones.get(self.bone_name)
        if pose_bone:
            pose_bone.rigify_type = "face.skin_eye"
        
        bpy.ops.object.mode_set(mode='OBJECT')

@dataclass
class face_skin_jaw(rigify_type):
    """Rigify type: face.skin_jaw - Used for jaw rigs."""
    bone_name: str = None
    jaw_mouth_influence: float = None
    
    def apply(self, armature: bpy.types.Object) -> None:
        """Apply jaw rig settings."""
        bpy.context.view_layer.objects.active = armature
        bpy.ops.object.mode_set(mode='POSE')
        
        pose_bone = armature.pose.bones.get(self.bone_name)
        if pose_bone:
            pose_bone.rigify_type = "face.skin_jaw"
            
            if self.jaw_mouth_influence is not None:
                rigify_params = pose_bone.rigify_parameters
                rigify_params.jaw_mouth_influence = self.jaw_mouth_influence
        
        bpy.ops.object.mode_set(mode='OBJECT')

@dataclass
class face_basic_tongue(rigify_type):
    """Rigify type: face.basic_tongue - Used for tongue rigs."""
    bone_name: str = None
    tweak_coll: str = None
    
    def apply(self, armature: bpy.types.Object) -> None:
        """Apply basic tongue rig settings."""
        bpy.context.view_layer.objects.active = armature
        bpy.ops.object.mode_set(mode='POSE')
        
        pose_bone = armature.pose.bones.get(self.bone_name)
        if pose_bone:
            pose_bone.rigify_type = "face.basic_tongue"
            
            if self.tweak_coll:
                try:
                    rigify_params = pose_bone.rigify_parameters
                    rigify_params.tweak_coll_refs.clear()
                    
                    if self.tweak_coll in armature.data.collections:
                        bpy.ops.pose.rigify_collection_ref_add(prop_name="tweak_coll_refs")
                        if len(rigify_params.tweak_coll_refs) > 0:
                            tweak_ref = rigify_params.tweak_coll_refs[-1]
                            tweak_ref.name = self.tweak_coll
                except Exception as e:
                    print(f"[AetherBlend] Error setting tweak collection: {e}")
        
        bpy.ops.object.mode_set(mode='OBJECT')

# Registry mapping rigify type strings to their classes
RIGIFY_TYPE_REGISTRY = {
    "limbs.leg": limbs_leg,
    "limbs.arm": limbs_arm,
    "limbs.super_finger": limbs_super_finger,
    "spines.basic_spine": spines_basic_spine,
    "spines.super_head": spines_super_head,
    "spines.basic_tail": spines_basic_tail,
    "basic.super_copy": basic_super_copy,
    "skin.stretchy_chain": skin_stretchy_chain,
    "skin.basic_chain": skin_basic_chain,
    "skin.glue": skin_glue,
    "skin.anchor": skin_anchor,
    "face.skin_eye": face_skin_eye,
    "face.skin_jaw": face_skin_jaw,
    "face.basic_tongue": face_basic_tongue,
}

def get_rigify_type_class(rigify_type_name: str):
    """Get the rigify type class for a given type name."""
    return RIGIFY_TYPE_REGISTRY.get(rigify_type_name)