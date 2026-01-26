import bpy

def get_colorset_items(self, context):
    from . import module_manager
    config = module_manager.get_module_config('colorset')
    return [(key, key, "") for key in config.get('available_modules', {}).keys()]

def get_ui_collection_items(self, context):
    from . import module_manager
    config = module_manager.get_module_config('ui_collection')
    return [(key, key, "") for key in config.get('available_modules', {}).keys()]

def get_widget_override_items(self, context):
    from . import module_manager
    config = module_manager.get_module_config('widget_override')
    return [(key, key, "") for key in config.get('available_modules', {}).keys()]

def get_bone_group_items(self, context):
    from . import module_manager
    config = module_manager.get_module_config('bone_group')
    return [(key, key, "") for key in config.get('available_modules', {}).keys()]

# Get defaults from module_manager config
from . import module_manager
_DEFAULTS = {
    'colorset': module_manager.MODULE_TYPE_CONFIG['colorset']['default'],
    'ui_collection': module_manager.MODULE_TYPE_CONFIG['ui_collection']['default'],
    'widget_override': module_manager.MODULE_TYPE_CONFIG['widget_override']['default'],
    'bone_group': module_manager.MODULE_TYPE_CONFIG['bone_group']['default']
}

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
    
    # Template selection
    template_dropdown : bpy.props.EnumProperty(
        name="Template",
        description="Select a template to load",
        items=module_manager.get_template_items,
        default=0
    ) # type: ignore
    
    # Selected modules for rig generation
    selected_colorsets : bpy.props.StringProperty(
        name="Selected Colorsets",
        description="Comma-separated list of selected colorset module names",
        default=_DEFAULTS['colorset']
    ) # type: ignore
    
    selected_ui_collections : bpy.props.StringProperty(
        name="Selected UI Collections",
        description="Comma-separated list of selected UI collection module names",
        default=_DEFAULTS['ui_collection']
    ) # type: ignore
    
    selected_widget_overrides : bpy.props.StringProperty(
        name="Selected Widget Overrides",
        description="Comma-separated list of selected widget override module names",
        default=_DEFAULTS['widget_override']
    ) # type: ignore
    
    selected_bone_groups : bpy.props.StringProperty(
        name="Selected Bone Groups",
        description="Comma-separated list of selected bone group module names",
        default=_DEFAULTS['bone_group']
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