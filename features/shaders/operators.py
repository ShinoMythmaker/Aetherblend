import bpy 
from typing import ClassVar

from . import shader_util
from ...utils import addon_dependencies
from ...utils.armature import find_meshes
from ...preferences import get_preferences

_IRIS_SHADER_INPUT_CONNECTIONS = {}

_IRIS_SHADER_OUTPUT_CONNECTIONS = {
    "Vector": [
        ("Image Texture.001", "Vector"),
        ("Image Texture", "Vector"),
        ("Image Texture.002", "Vector")
    ],
    "Limbal UV": [
        ("[AetherBlend] Limbal Rings", "UVMap"),
    ]
}

_IRIS_SHADER_CUSTOM_PROPERTIES = [
    ("Eye Scale X", 1.0),
    ("Eye Scale Y", 1.0),
    ("Pupil Scale", 0.0)
]

_LIMBAL_SHADER_INPUT_CONNECTIONS = {
    "UVMap": [
        ("UV Map", "UV"),
        ("[AetherBlend] Eye Scaling", "Limbal UV"),
    ],
}

_LIMBAL_SHADER_OUTPUT_CONNECTIONS = {
    "Emission Color": [
        ("Principled BSDF", "Emission Color")
    ],
    "Emission Strength": [
        ("Principled BSDF", "Emission Strength")
    ],
}
class AETHER_OT_S_Iris(bpy.types.Operator):
    """Apply AetherBlend Iris node-group setup to iris materials."""

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
            shader_util.connect_sockets(
                eye_material.node_tree,
                group_node,
                _IRIS_SHADER_INPUT_CONNECTIONS,
                _IRIS_SHADER_OUTPUT_CONNECTIONS
            )

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
    
class AETHER_OT_S_Limbal(bpy.types.Operator):
    """Apply AetherBlend Limbal Rings node-group setup to iris materials."""

    bl_idname = "aether.shader_limbal"
    bl_label = "Set Up Limbal Rings"

    group_name: ClassVar[str] = "[AetherBlend] Limbal Rings"

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
            # Append Node Group and Add to Material
            #####
            shader_util.remove_group_node_from_node_tree(eye_material.node_tree, self.group_name)
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
            shader_util.connect_sockets(
                eye_material.node_tree,
                group_node,
                _LIMBAL_SHADER_INPUT_CONNECTIONS,
                _LIMBAL_SHADER_OUTPUT_CONNECTIONS
            )

            #####
            # Style 
            #####
            group_node.location = (-0, -1450)
            group_node.width = 220

            shader_util.refresh_shader_dependency_state(
                context,
                [obj for obj, _material in eyes],
                eye_material,
            )
        
            self.report({'INFO'}, f"Node group '{self.group_name}' appended successfully.")
        except ValueError as e:
            self.report({'ERROR'}, str(e))
        return {'FINISHED'}
    
class AETHER_OT_S_FFGear(bpy.types.Operator):
    """Run FFGear shader import for meshes bound to the selected armature."""

    bl_idname = "aether.shader_ffgear"
    bl_label = "Set Up FFGEAR"

    filter_glob: bpy.props.StringProperty(default="*.nofilesplease", options={'HIDDEN'}) #type: ignore
    filepath: bpy.props.StringProperty(subtype="FILE_PATH") #type: ignore

    def invoke(self, context, event):
        prefs = get_preferences()
        if prefs.default_meddle_import_path:
            self.filepath = prefs.default_meddle_import_path

        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        if not addon_dependencies.is_addon_enabled(display_name="FFGear"):
            self.report({'ERROR'}, "FFGear add-on is not enabled")
            return {'CANCELLED'}

        try:
            armature = context.active_object
            if not armature or armature.type != 'ARMATURE':
                self.report({'ERROR'}, "Please select an armature object.")
                return {'CANCELLED'}
            
            # Get affected Meshes
            meshes = find_meshes(armature)

            # Reroute to FFGear Operator
            ok = shader_util.import_ffgear_shader(self.filepath, meshes)
            if not ok:
                self.report({'ERROR'}, "Failed to import FFGear shader")
                return {'CANCELLED'}

            # Making sure only rig is selcted afterwards
            for obj in context.selected_objects:
                obj.select_set(False)
            
            armature.select_set(True)
        
            self.report({'INFO'}, f"FFGEAR shader imported successfully.")
        except Exception as e:
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}
        return {'FINISHED'}

class AETHER_OT_S_Meddle(bpy.types.Operator):
    """Run Meddle shader import for meshes bound to the selected armature."""

    bl_idname = "aether.shader_meddle"
    bl_label = "Set Up Meddle"

    filter_glob: bpy.props.StringProperty(default="*.nofilesplease", options={'HIDDEN'}) #type: ignore
    filepath: bpy.props.StringProperty(subtype="FILE_PATH") #type: ignore

    def invoke(self, context, event):
        prefs = get_preferences()
        if prefs.default_meddle_import_path:
            self.filepath = prefs.default_meddle_import_path

        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        if not addon_dependencies.is_addon_enabled(display_name="Meddle Tools"):
            self.report({'ERROR'}, "Meddle Tools add-on is not enabled")
            return {'CANCELLED'}

        window = context.window
        if window:
            window.cursor_set('WAIT')

        try:
            armature = context.active_object
            if not armature or armature.type != 'ARMATURE':
                self.report({'ERROR'}, "Please select an armature object.")
                return {'CANCELLED'}
            
            # Get affected Meshes
            meshes = find_meshes(armature)

            # Reroute to Meddle Operator
            ok = shader_util.import_meddle_shader(self.filepath, meshes)
            if not ok:
                self.report({'ERROR'}, "Failed to import Meddle shader")
                return {'CANCELLED'}

            # Making sure only rig is selcted afterwards
            for obj in context.selected_objects:
                obj.select_set(False)
            
            armature.select_set(True)
        
            self.report({'INFO'}, f"Meddle shader imported successfully.")
        except Exception as e:
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}
        finally:
            if window:
                window.cursor_set('DEFAULT')

        return {'FINISHED'}




def register():
    bpy.utils.register_class(AETHER_OT_S_Iris)
    bpy.utils.register_class(AETHER_OT_S_Limbal)
    bpy.utils.register_class(AETHER_OT_S_FFGear)
    bpy.utils.register_class(AETHER_OT_S_Meddle)
def unregister():
    bpy.utils.unregister_class(AETHER_OT_S_Iris)
    bpy.utils.unregister_class(AETHER_OT_S_Limbal)
    bpy.utils.unregister_class(AETHER_OT_S_FFGear)
    bpy.utils.unregister_class(AETHER_OT_S_Meddle)
    