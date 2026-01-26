import bpy

def get_available_modules(module_type):
    """Dynamically get available modules for dropdown"""
    from .templates import CS_COLORSETS, UI_COLLECTIONS, WO_OVERRIDES, BG_GROUPS
    
    module_map = {
        'colorset': CS_COLORSETS,
        'ui_collection': UI_COLLECTIONS,
        'widget_override': WO_OVERRIDES,
        'bone_group': BG_GROUPS
    }
    
    modules = module_map.get(module_type, {})
    return [(key, key, "") for key in modules.keys()]

def get_colorset_items(self, context):
    return get_available_modules('colorset')

def get_ui_collection_items(self, context):
    return get_available_modules('ui_collection')

def get_widget_override_items(self, context):
    return get_available_modules('widget_override')

def get_bone_group_items(self, context):
    return get_available_modules('bone_group')

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
    
    # Selected modules for rig generation
    selected_colorsets : bpy.props.StringProperty(
        name="Selected Colorsets",
        description="Comma-separated list of selected colorset module names",
        default="Aether Blend"
    ) # type: ignore
    
    selected_ui_collections : bpy.props.StringProperty(
        name="Selected UI Collections",
        description="Comma-separated list of selected UI collection module names",
        default="Player SFW"
    ) # type: ignore
    
    selected_widget_overrides : bpy.props.StringProperty(
        name="Selected Widget Overrides",
        description="Comma-separated list of selected widget override module names",
        default="Default"
    ) # type: ignore
    
    selected_bone_groups : bpy.props.StringProperty(
        name="Selected Bone Groups",
        description="Comma-separated list of selected bone group module names",
        default="Player SFW"
    ) # type: ignore
    
    # Dropdown selections for adding modules
    dropdown_colorset : bpy.props.EnumProperty(
        name="Colorset",
        description="Select a colorset to add",
        items=get_colorset_items
    ) # type: ignore
    
    dropdown_ui_collection : bpy.props.EnumProperty(
        name="UI Collection",
        description="Select a UI collection to add",
        items=get_ui_collection_items
    ) # type: ignore
    
    dropdown_widget_override : bpy.props.EnumProperty(
        name="Widget Override",
        description="Select a widget override to add",
        items=get_widget_override_items
    ) # type: ignore
    
    dropdown_bone_group : bpy.props.EnumProperty(
        name="Bone Group",
        description="Select a bone group to add",
        items=get_bone_group_items
    ) # type: ignore


def register():
    bpy.utils.register_class(AETHER_PROP_Rig)
    bpy.types.Object.aether_rig = bpy.props.PointerProperty(type=AETHER_PROP_Rig)

def unregister():
    if hasattr(bpy.types.Object, 'aether_rig'):
        del bpy.types.Object.aether_rig
    bpy.utils.unregister_class(AETHER_PROP_Rig)