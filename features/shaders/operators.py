import bpy 
from typing import ClassVar

from . import shader_util
from ...utils.armature import find_meshes

_IRIS_SHADER_OUTPUT_CONNECTIONS = {
    "Vector": [
        ("g_SamplerDiffuse_PngCachePath", "Vector"),
        ("g_SamplerNormal_PngCachePath", "Vector"),
        ("g_SamplerMask_PngCachePath", "Vector")
    ],
}

_IRIS_SHADER_CUSTOM_PROPERTIES = [
    ("Eye Scale X", 1.0),
    ("Eye Scale Y", 1.0),
    ("Pupil Scale", 0.0)
]

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
            
            #####
            # Get Material
            #####
            meshes = find_meshes(armature)
            if not meshes:
                self.report({'ERROR'}, "No meshes found using the selected armature.")
                return {'CANCELLED'}
            
            eyes = shader_util.find_material_by_property(meshes, "ShaderPackage", "iris.shpk")
            if not eyes:
                self.report({'ERROR'}, "No materials with ShaderPackage='iris.shpk' found on meshes driven by the armature.")
                return {'CANCELLED'}
            
            eye_material = eyes[0][1]

            #####
            # Add needed Custom Properties to Meshes
            #####
            for obj, material in eyes:
                for prop_name, default_value in _IRIS_SHADER_CUSTOM_PROPERTIES:
                    if prop_name not in obj:
                        obj[prop_name] = default_value

            #####
            # Append Node Group and Add to Material
            #####
            node_group = shader_util.append_node_group(self.group_name)
            group_node = shader_util.add_node_group_to_node_tree(eye_material, node_group)

            #####
            # Apply material properties to node group inputs
            #####
            inputs = group_node.inputs
            for input in inputs:
                material_prop = shader_util.get_value_from_material_property(eye_material, input.name)
                if material_prop is not None:
                    shader_util.apply_material_property_to_socket(input, material_prop)

            #####
            ## Connect node group
            #####
            outputs = group_node.outputs

            for output_name, connections in _IRIS_SHADER_OUTPUT_CONNECTIONS.items():
                output_socket = outputs.get(output_name)
                if not output_socket:
                    self.report({'WARNING'}, f"Output socket '{output_name}' not found in node group.")
                    continue

                for target_node_label, target_socket_name in connections:
                    target_socket = shader_util.get_socket_by_name(eye_material.node_tree, target_node_label, target_socket_name)
                    if not target_socket:
                        self.report({'WARNING'}, f"Target socket '{target_socket_name}' on node '{target_node_label}' not found.")
                        continue

                    eye_material.node_tree.links.new(output_socket, target_socket)

            #####
            # Style 
            #####
            group_node.location = (-1100, -600)
            group_node.width = 300

            shader_util.refresh_shader_dependency_state(
                context,
                [obj for obj, _material in eyes],
                eye_material,
            )
        
            self.report({'INFO'}, f"Node group '{self.group_name}' appended successfully.")
        except ValueError as e:
            self.report({'ERROR'}, str(e))
        return {'FINISHED'}
    

def register():
    bpy.utils.register_class(AETHER_OT_S_Iris)

def unregister():
    bpy.utils.unregister_class(AETHER_OT_S_Iris)
