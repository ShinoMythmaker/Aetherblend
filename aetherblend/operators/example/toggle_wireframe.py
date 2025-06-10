import bpy

class OBJECT_OT_toggle_wireframe(bpy.types.Operator):
    """Toggle wireframe mode"""
    bl_idname = "object.toggle_wireframe"
    bl_label = "Toggle Wireframe"

    def execute(self, context):
        for obj in bpy.context.selected_objects:
            obj.show_wire = not obj.show_wire
        return {'FINISHED'}

def register():
    bpy.utils.register_class(OBJECT_OT_toggle_wireframe)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_toggle_wireframe)