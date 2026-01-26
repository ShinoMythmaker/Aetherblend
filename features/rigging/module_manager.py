"""
Module management system for rig generation.
Centralizes all module type definitions and operations.
"""
import bpy
from .templates import CS_COLORSETS, UI_COLLECTIONS, WO_OVERRIDES, BG_GROUPS, TEMPLATES


def get_template_items(self, context):
    """Get available templates for dropdown."""
    return [(key, key, "") for key in TEMPLATES.keys()]


def _normalize_default(default):
    """Convert default value to comma-separated string."""
    if isinstance(default, list):
        return ", ".join(default)
    return default


# Get default template configuration
DEFAULT_TEMPLATE_NAME = 'Player SFW'
_default_template = TEMPLATES.get(DEFAULT_TEMPLATE_NAME)

# Module type configuration - single source of truth
MODULE_TYPE_CONFIG = {
    'colorset': {
        'label': 'Colorsets',
        'icon': 'COLOR',
        'property': 'selected_colorsets',
        'dropdown_property': 'dropdown_colorset',
        'available_modules': CS_COLORSETS,
        'default': _default_template.color_sets if _default_template else []
    },
    'ui_collection': {
        'label': 'UI Collections',
        'icon': 'OUTLINER_COLLECTION',
        'property': 'selected_ui_collections',
        'dropdown_property': 'dropdown_ui_collection',
        'available_modules': UI_COLLECTIONS,
        'default': _default_template.ui_collections if _default_template else []
    },
    'widget_override': {
        'label': 'Widget Overrides',
        'icon': 'MESH_CUBE',
        'property': 'selected_widget_overrides',
        'dropdown_property': 'dropdown_widget_override',
        'available_modules': WO_OVERRIDES,
        'default': _default_template.widget_overrides if _default_template else []
    },
    'bone_group': {
        'label': 'Bone Groups',
        'icon': 'GROUP_BONE',
        'property': 'selected_bone_groups',
        'dropdown_property': 'dropdown_bone_group',
        'available_modules': BG_GROUPS,
        'default': _default_template.bone_groups if _default_template else []
    }
}

# Normalize all defaults to strings
for config in MODULE_TYPE_CONFIG.values():
    config['default'] = _normalize_default(config['default'])

# Generate enum items for operators
MODULE_TYPES = [(key, config['label'], "") for key, config in MODULE_TYPE_CONFIG.items()]


def get_module_config(module_type: str) -> dict:
    """Get configuration for a specific module type."""
    return MODULE_TYPE_CONFIG.get(module_type, {})


def get_property_name(module_type: str) -> str:
    """Get the property name for a given module type."""
    config = get_module_config(module_type)
    return config.get('property', '')


def get_selected_modules(aether_rig, module_type: str) -> list[str]:
    """Get the list of selected modules for a given type."""
    prop_name = get_property_name(module_type)
    if not prop_name:
        return []
    current = getattr(aether_rig, prop_name, "")
    return [m.strip() for m in current.split(",") if m.strip()]


def set_selected_modules(aether_rig, module_type: str, modules: list[str]):
    """Set the list of selected modules for a given type."""
    prop_name = get_property_name(module_type)
    if prop_name:
        setattr(aether_rig, prop_name, ", ".join(modules))


def load_template(aether_rig, template_name: str):
    """Load a template and apply its module configuration."""
    if template_name not in TEMPLATES:
        return False
    
    template = TEMPLATES[template_name]
    
    # Set modules for each type based on template
    set_selected_modules(aether_rig, 'colorset', template.color_sets or [])
    set_selected_modules(aether_rig, 'ui_collection', template.ui_collections or [])
    set_selected_modules(aether_rig, 'widget_override', template.widget_overrides or [])
    set_selected_modules(aether_rig, 'bone_group', template.bone_groups or [])
    
    return True


class AETHER_OT_LoadTemplate(bpy.types.Operator):
    bl_idname = "aether.load_template"
    bl_label = "Load Template"
    bl_description = "Load a predefined template configuration"
    bl_options = {'REGISTER', 'UNDO'}
    
    template_name: bpy.props.StringProperty(name="Template Name") # type: ignore
    
    def execute(self, context):
        armature = context.active_object
        if not armature or armature.type != 'ARMATURE':
            self.report({'ERROR'}, "No armature selected")
            return {'CANCELLED'}
        
        aether_rig = armature.aether_rig
        
        if load_template(aether_rig, self.template_name):
            self.report({'INFO'}, f"Loaded template: {self.template_name}")
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, f"Template not found: {self.template_name}")
            return {'CANCELLED'}


class AETHER_OT_AddModuleToRig(bpy.types.Operator):
    bl_idname = "aether.add_module_to_rig"
    bl_label = "Add Module"
    bl_description = "Add a module to the rig generator configuration"
    bl_options = {'REGISTER', 'UNDO'}
    
    module_type: bpy.props.EnumProperty(
        name="Module Type",
        items=MODULE_TYPES
    ) # type: ignore
    
    module_name: bpy.props.StringProperty(name="Module Name") # type: ignore
    
    def execute(self, context):
        armature = context.active_object
        if not armature or armature.type != 'ARMATURE':
            self.report({'ERROR'}, "No armature selected")
            return {'CANCELLED'}
        
        aether_rig = armature.aether_rig
        current_list = get_selected_modules(aether_rig, self.module_type)
        
        # Add module if not already in list
        if self.module_name not in current_list:
            current_list.append(self.module_name)
            set_selected_modules(aether_rig, self.module_type, current_list)
        
        return {'FINISHED'}


class AETHER_OT_RemoveModuleFromRig(bpy.types.Operator):
    bl_idname = "aether.remove_module_from_rig"
    bl_label = "Remove Module"
    bl_description = "Remove a module from the rig generator configuration"
    bl_options = {'REGISTER', 'UNDO'}
    
    module_type: bpy.props.EnumProperty(
        name="Module Type",
        items=MODULE_TYPES
    ) # type: ignore
    
    module_name: bpy.props.StringProperty(name="Module Name") # type: ignore
    
    def execute(self, context):
        armature = context.active_object
        if not armature or armature.type != 'ARMATURE':
            self.report({'ERROR'}, "No armature selected")
            return {'CANCELLED'}
        
        aether_rig = armature.aether_rig
        current_list = get_selected_modules(aether_rig, self.module_type)
        
        # Remove module
        if self.module_name in current_list:
            current_list.remove(self.module_name)
            set_selected_modules(aether_rig, self.module_type, current_list)
        
        return {'FINISHED'}


class AETHER_OT_MoveModuleUp(bpy.types.Operator):
    bl_idname = "aether.move_module_up"
    bl_label = "Move Module Up"
    bl_description = "Move a module up in the list"
    bl_options = {'REGISTER', 'UNDO'}
    
    module_type: bpy.props.EnumProperty(
        name="Module Type",
        items=MODULE_TYPES
    ) # type: ignore
    
    module_name: bpy.props.StringProperty(name="Module Name") # type: ignore
    
    def execute(self, context):
        armature = context.active_object
        if not armature or armature.type != 'ARMATURE':
            return {'CANCELLED'}
        
        aether_rig = armature.aether_rig
        current_list = get_selected_modules(aether_rig, self.module_type)
        
        # Find index and move up
        if self.module_name in current_list:
            index = current_list.index(self.module_name)
            if index > 0:
                current_list[index], current_list[index - 1] = current_list[index - 1], current_list[index]
                set_selected_modules(aether_rig, self.module_type, current_list)
        
        return {'FINISHED'}


class AETHER_OT_MoveModuleDown(bpy.types.Operator):
    bl_idname = "aether.move_module_down"
    bl_label = "Move Module Down"
    bl_description = "Move a module down in the list"
    bl_options = {'REGISTER', 'UNDO'}
    
    module_type: bpy.props.EnumProperty(
        name="Module Type",
        items=MODULE_TYPES
    ) # type: ignore
    
    module_name: bpy.props.StringProperty(name="Module Name") # type: ignore
    
    def execute(self, context):
        armature = context.active_object
        if not armature or armature.type != 'ARMATURE':
            return {'CANCELLED'}
        
        aether_rig = armature.aether_rig
        current_list = get_selected_modules(aether_rig, self.module_type)
        
        # Find index and move down
        if self.module_name in current_list:
            index = current_list.index(self.module_name)
            if index < len(current_list) - 1:
                current_list[index], current_list[index + 1] = current_list[index + 1], current_list[index]
                set_selected_modules(aether_rig, self.module_type, current_list)
        
        return {'FINISHED'}


def register():
    bpy.utils.register_class(AETHER_OT_LoadTemplate)
    bpy.utils.register_class(AETHER_OT_AddModuleToRig)
    bpy.utils.register_class(AETHER_OT_RemoveModuleFromRig)
    bpy.utils.register_class(AETHER_OT_MoveModuleUp)
    bpy.utils.register_class(AETHER_OT_MoveModuleDown)


def unregister():
    bpy.utils.unregister_class(AETHER_OT_LoadTemplate)
    bpy.utils.unregister_class(AETHER_OT_AddModuleToRig)
    bpy.utils.unregister_class(AETHER_OT_RemoveModuleFromRig)
    bpy.utils.unregister_class(AETHER_OT_MoveModuleUp)
    bpy.utils.unregister_class(AETHER_OT_MoveModuleDown)
