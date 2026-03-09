import bpy
from bpy.props import EnumProperty


TAB_ITEMS = [
    ('IMPORT_EXPORT', "Import/Export", "Import and Export tools", 'IMPORT', 0),
    ('CPLUS', "C+", "Customize Plus tools", 'MODIFIER', 1),
    ('GENERATE', "Generate", "Rig generation tools", 'ARMATURE_DATA', 2),
    ('RIG_LAYERS', "Rig Layers", "Rig layers", 'BONE_DATA', 3),
    ('RIG_UI', "Rig UI", "Rig UI and bake settings", 'PROPERTIES', 4),
]


def get_active_tab_prop_name(context):
    area = getattr(context, "area", None)
    if area is not None and area.type == 'PROPERTIES':
        return "active_tab_tool"
    return "active_tab"


def get_active_tab(context):
    tabs = getattr(getattr(context, "scene", None), "aether_tabs", None)
    if tabs is None:
        return 'IMPORT_EXPORT'
    return getattr(tabs, get_active_tab_prop_name(context), 'IMPORT_EXPORT')


def set_active_tab(context, value):
    tabs = getattr(getattr(context, "scene", None), "aether_tabs", None)
    if tabs is None:
        return
    setattr(tabs, get_active_tab_prop_name(context), value)

class AetherTabProperties(bpy.types.PropertyGroup):
    """Properties for AetherBlend tab management"""
    
    active_tab: EnumProperty(
        name="Active Tab",
        description="Currently active tab in AetherBlend panel",
        items=TAB_ITEMS,
        default='IMPORT_EXPORT'
    ) #type: ignore

    active_tab_tool: EnumProperty(
        name="Active Tool Tab",
        description="Currently active tab in AetherBlend tool panel",
        items=TAB_ITEMS,
        default='IMPORT_EXPORT'
    ) #type: ignore

def register():
    bpy.utils.register_class(AetherTabProperties)
    bpy.types.Scene.aether_tabs = bpy.props.PointerProperty(type=AetherTabProperties)

def unregister():
    del bpy.types.Scene.aether_tabs
    bpy.utils.unregister_class(AetherTabProperties)
