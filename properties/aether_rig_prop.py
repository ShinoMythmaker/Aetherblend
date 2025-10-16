import bpy

class AETHER_PROP_Rig(bpy.types.PropertyGroup):
    meta_rig : bpy.props.PointerProperty(
        name="Meta Rig",
        type=bpy.types.Object,
        description="Reference to the Meta-Rig for this armature",
        poll=lambda self, obj: obj.type == 'ARMATURE'
    ) # type: ignore
    
    rigify_rig : bpy.props.PointerProperty(
        name="Control Rig",
        type=bpy.types.Object,
        description="Reference to the Rigify-Rig for this armature",
        poll=lambda self, obj: obj.type == 'ARMATURE'
    ) # type: ignore
    
    rigify_linked : bpy.props.BoolProperty(
        name="Control Linked",
        description="Whether the Rigify-Rig is linked to this armature",
        default=False
    ) # type: ignore


def register():
    bpy.utils.register_class(AETHER_PROP_Rig)
    bpy.types.Object.aether_rig = bpy.props.PointerProperty(type=AETHER_PROP_Rig)

def unregister():
    if hasattr(bpy.types.Object, 'aether_rig'):
        del bpy.types.Object.aether_rig
    bpy.utils.unregister_class(AETHER_PROP_Rig)