import bpy

from . import module_manager


class AETHER_PROP_Rig(bpy.types.PropertyGroup):
    meta_rig : bpy.props.PointerProperty(
        name="Meta Rig",
        type=bpy.types.Object,
        description="Reference to the Meta-Rig for this armature",
        poll=lambda self, obj: obj.type == 'ARMATURE'
    ) # type: ignore
    
    rigified : bpy.props.BoolProperty(
        name="Rigified",
        description="Whether the armature went through generation process or not",
        default=False
    ) # type: ignore
    
    selected_template : bpy.props.EnumProperty(
        name="Template",
        description="Select a rig template",
        items=module_manager.get_template_items,
        default=0
    ) # type: ignore
    
    selected_colorset : bpy.props.EnumProperty(
        name="Colorset",
        description="Select a colorset (replaces template default)",
        items=module_manager.get_colorset_items,
        default=0
    ) # type: ignore


def register():
    bpy.utils.register_class(AETHER_PROP_Rig)
    bpy.types.Object.aether_rig = bpy.props.PointerProperty(type=AETHER_PROP_Rig)

def unregister():
    if hasattr(bpy.types.Object, 'aether_rig'):
        del bpy.types.Object.aether_rig
    bpy.utils.unregister_class(AETHER_PROP_Rig)