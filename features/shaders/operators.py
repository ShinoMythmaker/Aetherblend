import bpy 
from typing import ClassVar

from . import shader_util
from ...utils.armature import find_meshes
from ...utils.object import find_by_armature_and_material_property

class AETHER_OT_S_Iris(bpy.types.Operator):
    bl_idname = "aether.shader_iris"
    bl_label = "Set Up Iris"

    group_name: ClassVar[str] = "[AetherBlend] Eye Scaling"

    def execute(self, context):
        try:
            armature = context.active_object
            if not armature or armature.type != 'ARMATURE':
                self.report({'ERROR'}, "Please select an armature object.")
                return {'CANCELLED'}
            

            meshes = find_meshes(armature)
            if not meshes:
                self.report({'ERROR'}, "No meshes found using the selected armature.")
                return {'CANCELLED'}
            
            eye_materials = shader_util.find_material_by_property(meshes, "ShaderPackage", "iris.shpk")
            if not eye_materials:
                self.report({'ERROR'}, "No materials with ShaderPackage='iris.shpk' found on meshes driven by the armature.")
                return {'CANCELLED'}
            
            eye_material = eye_materials[0]

            node_group = shader_util.append_node_group(self.group_name)
            shader_util.add_node_group_to_node_tree(eye_material, node_group)
            
            self.report({'INFO'}, f"Node group '{self.group_name}' appended successfully.")
        except ValueError as e:
            self.report({'ERROR'}, str(e))
        return {'FINISHED'}
    

def register():
    bpy.utils.register_class(AETHER_OT_S_Iris)

def unregister():
    bpy.utils.unregister_class(AETHER_OT_S_Iris)
