import bpy

from . import template_manager


class AETHER_PROP_RigModuleItem(bpy.types.PropertyGroup):
    module_key : bpy.props.StringProperty(
        name="Module Key",
        description="Stable identifier for the selected rig module"
    ) # type: ignore

    group_index : bpy.props.IntProperty(
        name="Priority Group",
        description="Ordered fallback group this module belongs to",
        default=-1,
        options={'HIDDEN'}
    ) # type: ignore


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
        description="Select a rig template or switch to the editable custom module list",
        items=template_manager.get_template_items,
        update=template_manager.on_template_changed,
        default=0
    ) # type: ignore

    custom_template_source : bpy.props.StringProperty(
        name="Custom Template Source",
        description="Built-in template used to seed the editable custom module list",
        default=template_manager.DEFAULT_TEMPLATE_NAME,
        options={'HIDDEN'}
    ) # type: ignore

    custom_template_name : bpy.props.StringProperty(
        name="Template Name",
        description="Name used when saving this custom template as a JSON file",
        default="",
    ) # type: ignore

    custom_modules_initialized : bpy.props.BoolProperty(
        name="Custom Modules Initialized",
        description="Whether the editable custom module list has been intentionally created or populated",
        default=False,
        options={'HIDDEN'}
    ) # type: ignore

    selected_colorset : bpy.props.EnumProperty(
        name="Colorset",
        description="Select a colorset (replaces template default)",
        items=template_manager.get_colorset_items,
        default=0
    ) # type: ignore

    modules : bpy.props.CollectionProperty(
        type=AETHER_PROP_RigModuleItem
    ) # type: ignore

    module_index : bpy.props.IntProperty(
        name="Module Index",
        default=0,
        options={'HIDDEN'}
    ) # type: ignore
    
    link_inherit_scale : bpy.props.EnumProperty(
        name="LINK Inherit Scale",
        description="Inherit scale setting for LINK collection bones",
        items=[
            ('FULL', "Full", "Full inherit scale"),
            ('FIX_SHEAR', "Aligned", "Inherit scale with shear fixed"),
            ('AVERAGE', "Average", "Average scale inheritance"),
            ('NONE', "None", "No scale inheritance"),
            ('NONE_LEGACY', "None (Legacy)", "No scale inheritance (legacy)"),
        ],
        default='FULL',
    ) # type: ignore


def register():
    bpy.utils.register_class(AETHER_PROP_RigModuleItem)
    bpy.utils.register_class(AETHER_PROP_Rig)
    bpy.types.Object.aether_rig = bpy.props.PointerProperty(type=AETHER_PROP_Rig)

def unregister():
    if hasattr(bpy.types.Object, 'aether_rig'):
        del bpy.types.Object.aether_rig
    bpy.utils.unregister_class(AETHER_PROP_Rig)
    bpy.utils.unregister_class(AETHER_PROP_RigModuleItem)