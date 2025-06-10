import bpy

class AETHER_OT_ConfirmDialog(bpy.types.Operator):
    """Confirmation Dialog"""
    bl_idname = "aether.confirm_dialog"
    bl_label = "Confirm Action"

    message: bpy.props.StringProperty(name="Message")

    def execute(self, context):
        self.report({'INFO'}, f"[AetherBlend] Confirmed: {self.message}")
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


def register():
    bpy.utils.register_class(AETHER_OT_ConfirmDialog)

def unregister():
    bpy.utils.unregister_class(AETHER_OT_ConfirmDialog)