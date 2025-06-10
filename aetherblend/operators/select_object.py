import bpy

class OBJECT_OT_select(bpy.types.Operator):
    """Select an object by name"""
    bl_idname = "object.select_by_name"
    bl_label = "Select Object"
    
    object_name: bpy.props.StringProperty(name="Object Name")
    
    def execute(self, context):
        obj = bpy.data.objects.get(self.object_name)
        if obj:
            bpy.context.view_layer.objects.active = obj
            obj.select_set(True)
            return {'FINISHED'}
        return {'CANCELLED'}

def register():
    bpy.utils.register_class(OBJECT_OT_select)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_select)