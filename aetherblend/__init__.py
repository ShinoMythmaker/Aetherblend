from . import registry

bl_info = {
    "name": "AetherBlend",
    "author": "Shino Mythmaker",
    "version": (0,0,3),
    "blender": (4,4,0),
    "description": "A collection of tools for working with FFXIV models in Blender.",
    "category": "AetherBlend",
    "location": "View3D > AetherBlend Tab",
}

def register():
    registry.register()  # Register operators/panels dynamically

def unregister():
    registry.unregister()


    
