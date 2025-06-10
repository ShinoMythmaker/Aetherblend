import bpy

class OBJECT_OT_create_cube(bpy.types.Operator):
    """Create a new cube"""
    bl_idname = "object.create_cube"
    bl_label = "Create Cube"

    def execute(self, context):
        bpy.ops.mesh.primitive_cube_add()
        return {'FINISHED'}

def register():
    bpy.utils.register_class(OBJECT_OT_create_cube)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_create_cube)