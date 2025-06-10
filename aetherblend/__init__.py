from . import registry, preferences

bl_info = {
    "name": "Aetherblend",
    "author": "Shino Mythmaker",
    "version": (0,0,1),
    "blender": (4,4,0),
    "description": "A collection of tools for working with FFXIV models in Blender.",
    "category": "Aetherblend",
    "location": "View3D > Aetherblend Tab",
}

def register():
    preferences.register() # Register settings 
    registry.register()  # Register operators/panels dynamically

def unregister():
    registry.unregister()
    preferences.unregister()


    
