import bpy
from dataclasses import dataclass

class rigify_type:
    """Base class for rigify types."""
    
    def apply(self, pose_bone: bpy.types.PoseBone, armature: bpy.types.Object) -> None:
        """
        Apply rigify settings to a bone.
        
        Args:
            pose_bone: The pose bone to apply settings to
            armature: The armature object
        """
        raise NotImplementedError("Subclasses must implement apply()")


@dataclass
class limbs_leg(rigify_type):
    """Rigify type: limbs.leg - Used for leg rigs."""
    fk_coll: str = None
    tweak_coll: str = None
    
    def apply(self, pose_bone: bpy.types.PoseBone, armature: bpy.types.Object) -> None:
        if pose_bone is None:
            print(f"[AetherBlend] Warning: pose_bone is None")
            return
        
        armature.data.bones.active = pose_bone.bone
        pose_bone.rigify_type = "limbs.leg"
        rigify_params = pose_bone.rigify_parameters
        
        try:
            if self.fk_coll:
                rigify_params.fk_coll_refs.clear()
                if self.fk_coll in armature.data.collections:
                    bpy.ops.pose.rigify_collection_ref_add(prop_name="fk_coll_refs")
                    if len(rigify_params.fk_coll_refs) > 0:
                        fk_ref = rigify_params.fk_coll_refs[-1]
                        fk_ref.name = self.fk_coll
        except Exception as e:
            print(f"[AetherBlend] Error setting FK collection: {e}")
        try:
            if self.tweak_coll:
                rigify_params.tweak_coll_refs.clear()
                if self.tweak_coll in armature.data.collections:
                    bpy.ops.pose.rigify_collection_ref_add(prop_name="tweak_coll_refs")
                    if len(rigify_params.tweak_coll_refs) > 0:
                        tweak_ref = rigify_params.tweak_coll_refs[-1]
                        tweak_ref.name = self.tweak_coll
        except Exception as e:
            print(f"[AetherBlend] Error setting Tweak collection: {e}")
        

@dataclass
class limbs_arm(rigify_type):
    """Rigify type: limbs.arm - Used for arm rigs."""
    fk_coll: str = None
    tweak_coll: str = None
    
    def apply(self, pose_bone: bpy.types.PoseBone, armature: bpy.types.Object) -> None:
        if pose_bone is None:
            print(f"[AetherBlend] Warning: pose_bone is None")
            return
        
        armature.data.bones.active = pose_bone.bone
        pose_bone.rigify_type = "limbs.arm"
        rigify_params = pose_bone.rigify_parameters
        
        try:
            if self.fk_coll:
                rigify_params.fk_coll_refs.clear()
                if self.fk_coll in armature.data.collections:
                    bpy.ops.pose.rigify_collection_ref_add(prop_name="fk_coll_refs")
                    if len(rigify_params.fk_coll_refs) > 0:
                        fk_ref = rigify_params.fk_coll_refs[-1]
                        fk_ref.name = self.fk_coll
            
            if self.tweak_coll:
                rigify_params.tweak_coll_refs.clear()
                if self.tweak_coll in armature.data.collections:
                    bpy.ops.pose.rigify_collection_ref_add(prop_name="tweak_coll_refs")
                    if len(rigify_params.tweak_coll_refs) > 0:
                        tweak_ref = rigify_params.tweak_coll_refs[-1]
                        tweak_ref.name = self.tweak_coll
        except Exception as e:
            print(f"[AetherBlend] Error setting arm collections: {e}")

@dataclass
class limbs_super_finger(rigify_type):
    """Rigify type: limbs.super_finger - Used for finger and toe rigs."""
    tweak_coll: str = None
    make_extra_ik_control: bool = False
    
    def apply(self, pose_bone: bpy.types.PoseBone, armature: bpy.types.Object) -> None:
        if pose_bone is None:
            print(f"[AetherBlend] Warning: pose_bone is None")
            return
        
        armature.data.bones.active = pose_bone.bone
        pose_bone.rigify_type = "limbs.super_finger"
        rigify_params = pose_bone.rigify_parameters
        
        try:
            if self.tweak_coll:
                rigify_params.tweak_coll_refs.clear()
                if self.tweak_coll in armature.data.collections:
                    bpy.ops.pose.rigify_collection_ref_add(prop_name="tweak_coll_refs")
                    if len(rigify_params.tweak_coll_refs) > 0:
                        tweak_ref = rigify_params.tweak_coll_refs[-1]
                        tweak_ref.name = self.tweak_coll
            
            if self.make_extra_ik_control:
                rigify_params.make_extra_ik_control = self.make_extra_ik_control
        except Exception as e:
            print(f"[AetherBlend] Error setting super finger parameters: {e}")

@dataclass
class limbs_super_palm(rigify_type):
    """Rigify type: limbs.super_palm - Palm rig"""
    palm_both_sides: bool = None

    def apply(self, pose_bone: bpy.types.PoseBone, armature: bpy.types.Object) -> None:
        if pose_bone is None:
            print(f"[AetherBlend] Warning: pose_bone is None")
            return
        
        armature.data.bones.active = pose_bone.bone
        pose_bone.rigify_type = "limbs.super_palm"
        rigify_params = pose_bone.rigify_parameters

        try:
            if self.palm_both_sides:
                rigify_params.palm_both_sides = self.palm_both_sides
        except Exception as e:
            print(f"[AetherBlend] Error setting super palm parameters: {e}")


@dataclass
class spines_basic_spine(rigify_type):
    """Rigify type: spines.basic_spine - Used for spine rigs."""
    fk_coll: str = None
    tweak_coll: str = None
    pivot_pos: int = None
    
    def apply(self, pose_bone: bpy.types.PoseBone, armature: bpy.types.Object) -> None:
        if pose_bone is None:
            print(f"[AetherBlend] Warning: pose_bone is None")
            return
        
        armature.data.bones.active = pose_bone.bone
        pose_bone.rigify_type = "spines.basic_spine"
        rigify_params = pose_bone.rigify_parameters
        
        try:
            if self.fk_coll:
                rigify_params.fk_coll_refs.clear()
                if self.fk_coll in armature.data.collections:
                    bpy.ops.pose.rigify_collection_ref_add(prop_name="fk_coll_refs")
                    if len(rigify_params.fk_coll_refs) > 0:
                        fk_ref = rigify_params.fk_coll_refs[-1]
                        fk_ref.name = self.fk_coll
            
            if self.tweak_coll:
                rigify_params.tweak_coll_refs.clear()
                if self.tweak_coll in armature.data.collections:
                    bpy.ops.pose.rigify_collection_ref_add(prop_name="tweak_coll_refs")
                    if len(rigify_params.tweak_coll_refs) > 0:
                        tweak_ref = rigify_params.tweak_coll_refs[-1]
                        tweak_ref.name = self.tweak_coll
            
            if self.pivot_pos is not None:
                rigify_params.pivot_pos = self.pivot_pos
        except Exception as e:
            print(f"[AetherBlend] Error setting spine parameters: {e}")

@dataclass
class spines_super_head(rigify_type):
    """Rigify type: spines.super_head - Used for neck/head rigs."""
    tweak_coll: str = None
    
    def apply(self, pose_bone: bpy.types.PoseBone, armature: bpy.types.Object) -> None:
        if pose_bone is None:
            print(f"[AetherBlend] Warning: pose_bone is None")
            return
        
        armature.data.bones.active = pose_bone.bone
        pose_bone.rigify_type = "spines.super_head"
        rigify_params = pose_bone.rigify_parameters
        
        try:
            if self.tweak_coll:
                rigify_params.tweak_coll_refs.clear()
                if self.tweak_coll in armature.data.collections:
                    bpy.ops.pose.rigify_collection_ref_add(prop_name="tweak_coll_refs")
                    if len(rigify_params.tweak_coll_refs) > 0:
                        tweak_ref = rigify_params.tweak_coll_refs[-1]
                        tweak_ref.name = self.tweak_coll
        except Exception as e:
            print(f"[AetherBlend] Error setting tweak collection: {e}")

@dataclass
class spines_basic_tail(rigify_type):
    """Rigify type: spines.basic_tail - Used for tail rigs."""
    use_x: bool = False
    use_y: bool = False
    use_z: bool = False
    
    def apply(self, pose_bone: bpy.types.PoseBone, armature: bpy.types.Object) -> None:
        if pose_bone is None:
            print(f"[AetherBlend] Warning: pose_bone is None")
            return
        
        armature.data.bones.active = pose_bone.bone
        pose_bone.rigify_type = "spines.basic_tail"
        rigify_params = pose_bone.rigify_parameters
        
        try:
            rigify_params.copy_rotation_axes[0] = self.use_x
            rigify_params.copy_rotation_axes[1] = self.use_y
            rigify_params.copy_rotation_axes[2] = self.use_z
        except Exception as e:
            print(f"[AetherBlend] Error setting copy rotation axes: {e}")

@dataclass
class basic_super_copy(rigify_type):
    """Rigify type: basic.super_copy - Used for simple control bones."""
    widget_type: str = None
    
    def apply(self, pose_bone: bpy.types.PoseBone, armature: bpy.types.Object) -> None:
        if pose_bone is None:
            print(f"[AetherBlend] Warning: pose_bone is None")
            return
        
        armature.data.bones.active = pose_bone.bone
        pose_bone.rigify_type = "basic.super_copy"
        rigify_params = pose_bone.rigify_parameters

        try:
            if self.widget_type:
                rigify_params.super_copy_widget_type = self.widget_type
        except Exception as e:
            print(f"[AetherBlend] Error setting widget type: {e}")

@dataclass
class skin_stretchy_chain(rigify_type):
    """Rigify type: skin.stretchy_chain - Used for facial and stretchy chains."""
    skin_chain_pivot_pos: int = None
    skin_control_orientation_bone: str = None
    skin_chain_falloff: list = None
    skin_chain_falloff_length: bool = None
    skin_chain_falloff_spherical: list = None
    skin_chain_priority: int = None
    skin_chain_use_scale: list = None
    primary_layer_extra: str = None
    secondary_layer_extra: str = None
    skin_control_orientation_bone: str = None
    
    def apply(self, pose_bone: bpy.types.PoseBone, armature: bpy.types.Object) -> None:
        if pose_bone is None:
            print(f"[AetherBlend] Warning: pose_bone is None")
            return

        armature.data.bones.active = pose_bone.bone
        pose_bone.rigify_type = "skin.stretchy_chain"
        rigify_params = pose_bone.rigify_parameters
        
        try:
            if self.skin_chain_pivot_pos is not None:
                rigify_params.skin_chain_pivot_pos = self.skin_chain_pivot_pos
            if self.skin_control_orientation_bone:
                rigify_params.skin_control_orientation_bone = self.skin_control_orientation_bone
            if self.skin_chain_falloff:
                rigify_params.skin_chain_falloff = self.skin_chain_falloff
            if self.skin_chain_falloff_length:
                rigify_params.skin_chain_falloff_length = self.skin_chain_falloff_length
            if self.skin_chain_falloff_spherical:
                rigify_params.skin_chain_falloff_spherical = self.skin_chain_falloff_spherical
            if self.skin_chain_priority is not None:
                rigify_params.skin_chain_priority = self.skin_chain_priority
            if self.skin_chain_use_scale:
                rigify_params.skin_chain_use_scale = self.skin_chain_use_scale
            if self.skin_control_orientation_bone:
                rigify_params.skin_control_orientation_bone = self.skin_control_orientation_bone
            
            if self.primary_layer_extra:
                rigify_params.skin_primary_layers_extra = True
                rigify_params.skin_primary_coll_refs.clear()
                if self.primary_layer_extra in armature.data.collections:
                    bpy.ops.pose.rigify_collection_ref_add(prop_name="skin_primary_coll_refs")
                    if len(rigify_params.skin_primary_coll_refs) > 0:
                        skin_ref = rigify_params.skin_primary_coll_refs[-1]
                        skin_ref.name = self.primary_layer_extra
            
            if self.secondary_layer_extra:
                rigify_params.skin_secondary_layers_extra = True
                rigify_params.skin_secondary_coll_refs.clear()
                if self.secondary_layer_extra in armature.data.collections:
                    bpy.ops.pose.rigify_collection_ref_add(prop_name="skin_secondary_coll_refs")
                    if len(rigify_params.skin_secondary_coll_refs) > 0:
                        skin_ref = rigify_params.skin_secondary_coll_refs[-1]
                        skin_ref.name = self.secondary_layer_extra
        except Exception as e:
            print(f"[AetherBlend] Error setting stretchy chain parameters: {e}")

@dataclass
class skin_basic_chain(rigify_type):
    """Rigify type: skin.basic_chain - Used for basic skin chains."""
    skin_chain_priority: int = None
    skin_control_orientation_bone: str = None
    
    def apply(self, pose_bone: bpy.types.PoseBone, armature: bpy.types.Object) -> None:
        if pose_bone is None:
            print(f"[AetherBlend] Warning: pose_bone is None")
            return
        
        armature.data.bones.active = pose_bone.bone
        pose_bone.rigify_type = "skin.basic_chain"
        rigify_params = pose_bone.rigify_parameters
        
        try:
            if self.skin_chain_priority is not None:
                rigify_params.skin_chain_priority = self.skin_chain_priority
            if self.skin_control_orientation_bone:
                rigify_params.skin_control_orientation_bone = self.skin_control_orientation_bone
        except Exception as e:
            print(f"[AetherBlend] Error setting basic chain priority: {e}")

@dataclass
class skin_glue(rigify_type):
    """Rigify type: skin.glue - Used for glue bones in facial rigs."""
    relink_constraints: bool = None
    skin_glue_use_tail: bool = None
    skin_glue_tail_reparent: bool = None
    skin_glue_add_constraint: str = None
    skin_glue_add_constraint_influence: float = None
    
    def apply(self, pose_bone: bpy.types.PoseBone, armature: bpy.types.Object) -> None:
        if pose_bone is None:
            print(f"[AetherBlend] Warning: pose_bone is None")
            return
        
        armature.data.bones.active = pose_bone.bone
        pose_bone.rigify_type = "skin.glue"
        rigify_params = pose_bone.rigify_parameters
        
        try:
            if self.relink_constraints:
                rigify_params.relink_constraints = self.relink_constraints
            if self.skin_glue_use_tail:
                rigify_params.skin_glue_use_tail = self.skin_glue_use_tail
            if self.skin_glue_tail_reparent:
                rigify_params.skin_glue_tail_reparent = self.skin_glue_tail_reparent
            if self.skin_glue_add_constraint:
                rigify_params.skin_glue_add_constraint = self.skin_glue_add_constraint
            if self.skin_glue_add_constraint_influence is not None:
                rigify_params.skin_glue_add_constraint_influence = self.skin_glue_add_constraint_influence
        except Exception as e:
            print(f"[AetherBlend] Error setting glue parameters: {e}")

@dataclass
class skin_anchor(rigify_type):
    """Rigify type: skin.anchor - Used for anchor bones in facial rigs."""
    pivot_master_widget_type: str = None
    skin_anchor_hide: bool = None
    
    def apply(self, pose_bone: bpy.types.PoseBone, armature: bpy.types.Object) -> None:
        if pose_bone is None:
            print(f"[AetherBlend] Warning: pose_bone is None")
            return
        
        armature.data.bones.active = pose_bone.bone
        pose_bone.rigify_type = "skin.anchor"
        rigify_params = pose_bone.rigify_parameters
        
        try:
            if self.pivot_master_widget_type:
                rigify_params.pivot_master_widget_type = self.pivot_master_widget_type
            if self.skin_anchor_hide is not None:
                rigify_params.skin_anchor_hide = self.skin_anchor_hide
        except Exception as e:
            print(f"[AetherBlend] Error setting pivot master widget type: {e}")

@dataclass
class face_skin_eye(rigify_type):
    """Rigify type: face.skin_eye - Used for eye rigs."""
    
    def apply(self, pose_bone: bpy.types.PoseBone, armature: bpy.types.Object) -> None:
        if pose_bone is None:
            print(f"[AetherBlend] Warning: pose_bone is None")
            return
        
        armature.data.bones.active = pose_bone.bone
        pose_bone.rigify_type = "face.skin_eye"

@dataclass
class face_skin_jaw(rigify_type):
    """Rigify type: face.skin_jaw - Used for jaw rigs."""
    jaw_mouth_influence: float = None
    
    def apply(self, pose_bone: bpy.types.PoseBone, armature: bpy.types.Object) -> None:
        if pose_bone is None:
            print(f"[AetherBlend] Warning: pose_bone is None")
            return
        
        armature.data.bones.active = pose_bone.bone
        pose_bone.rigify_type = "face.skin_jaw"
        rigify_params = pose_bone.rigify_parameters
        
        try:
            if self.jaw_mouth_influence is not None:
                rigify_params.jaw_mouth_influence = self.jaw_mouth_influence
        except Exception as e:
            print(f"[AetherBlend] Error setting jaw mouth influence: {e}")

@dataclass
class face_basic_tongue(rigify_type):
    """Rigify type: face.basic_tongue - Used for tongue rigs."""
    tweak_coll: str = None
    
    def apply(self, pose_bone: bpy.types.PoseBone, armature: bpy.types.Object) -> None:
        if pose_bone is None:
            print(f"[AetherBlend] Warning: pose_bone is None")
            return
        
        armature.data.bones.active = pose_bone.bone
        pose_bone.rigify_type = "face.basic_tongue"
        rigify_params = pose_bone.rigify_parameters
        
        try:
            if self.tweak_coll:
                rigify_params.tweak_coll_refs.clear()
                if self.tweak_coll in armature.data.collections:
                    bpy.ops.pose.rigify_collection_ref_add(prop_name="tweak_coll_refs")
                    if len(rigify_params.tweak_coll_refs) > 0:
                        tweak_ref = rigify_params.tweak_coll_refs[-1]
                        tweak_ref.name = self.tweak_coll
        except Exception as e:
            print(f"[AetherBlend] Error setting tweak collection: {e}")

@dataclass
class basic_raw_copy(rigify_type):
    """Rigify type: basic.raw_copy - Used for raw copy bones."""
    relink_constraints: bool = None
    parent: str = None
    widget_type: str = None
    
    def apply(self, pose_bone: bpy.types.PoseBone, armature: bpy.types.Object) -> None:
        if pose_bone is None:
            print(f"[AetherBlend] Warning: pose_bone is None")
            return
        
        armature.data.bones.active = pose_bone.bone
        pose_bone.rigify_type = "basic.raw_copy"
        rigify_params = pose_bone.rigify_parameters
        
        try:
            if self.relink_constraints:
                rigify_params.relink_constraints = self.relink_constraints
                if self.parent:
                    rigify_params.parent_bone = self.parent
            if self.widget_type:
                rigify_params.raw_copy_widget_type = self.widget_type
        except Exception as e:
            print(f"[AetherBlend] Error setting raw copy parameters: {e}")


@dataclass
class basic_copy_chain(rigify_type):
    """Rigify type: basic.copy_chain - Used for copy chain bones."""
    make_deforms: bool = None
    make_controls: bool = None

    def apply(self, pose_bone: bpy.types.PoseBone, armature: bpy.types.Object) -> None:
        if pose_bone is None:
            print(f"[AetherBlend] Warning: pose_bone is None")
            return
        
        armature.data.bones.active = pose_bone.bone
        pose_bone.rigify_type = "basic.copy_chain"
        rigify_params = pose_bone.rigify_parameters
        
        try:
            if self.make_deforms is not None:
                rigify_params.make_deforms = self.make_deforms
            if self.make_controls is not None:
                rigify_params.make_controls = self.make_controls
        except Exception as e:
            print(f"[AetherBlend] Error setting copy chain parameters: {e}")

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
    "basic.raw_copy": basic_raw_copy,
}

def get_rigify_type_class(rigify_type_name: str):
    """Get the rigify type class for a given type name."""
    return RIGIFY_TYPE_REGISTRY.get(rigify_type_name)