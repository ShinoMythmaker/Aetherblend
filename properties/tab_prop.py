import bpy
from bpy.props import EnumProperty

class AetherTabProperties(bpy.types.PropertyGroup):
    """Properties for AetherBlend tab management"""
    
    active_tab: EnumProperty(
        name="Active Tab",
        description="Currently active tab in AetherBlend panel",
        items=[
            ('IMPORT_EXPORT', "Import/Export", "Import and Export tools", 'IMPORT', 0),
            ('CPLUS', "C+", "Customize Plus tools", 'MODIFIER', 1),
            ('GENERATE', "Generate", "Rig generation tools", 'ARMATURE_DATA', 2),
            ('RIG_LAYERS', "Rig Layers", "Rig layers", 'BONE_DATA', 3),
            ('RIG_UI', "Rig UI", "Rig UI and bake settings", 'PROPERTIES', 4),
        ],
        default='IMPORT_EXPORT'
    ) #type: ignore

def register():
    bpy.utils.register_class(AetherTabProperties)
    bpy.types.Scene.aether_tabs = bpy.props.PointerProperty(type=AetherTabProperties)

def unregister():
    del bpy.types.Scene.aether_tabs
    bpy.utils.unregister_class(AetherTabProperties)
