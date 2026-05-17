import bpy 
from typing import ClassVar

import util

class AETHER_OT_SetUpIris(bpy.types.Operator):
    bl_idname = "aether.setup_iris"
    bl_label = "Set Up Iris"

    group_name: ClassVar[str] = "[AetherBlend] Eye Scaling"

    def execute(self, context):
        try:
            util.append_node_group(self.group_name)
            self.report({'INFO'}, f"Node group '{self.group_name}' appended successfully.")
        except ValueError as e:
            self.report({'ERROR'}, str(e))
        return {'FINISHED'}
    

def register():
    bpy.utils.register_class(AETHER_OT_SetUpIris)

def unregister():
    bpy.utils.unregister_class(AETHER_OT_SetUpIris)
