"""Operators that apply shaders to materials."""

from typing import ClassVar

import bpy

from ...preferences import get_preferences
from ...utils import addon_dependencies
from ...utils.armature import find_meshes
from . import shader_util

# root socket: (target node name, target socket name)
_IRIS_SHADER_INPUT_CONNECTIONS = {}

_IRIS_SHADER_OUTPUT_CONNECTIONS = {
    "Vector": [("Image Texture.001", "Vector"), ("Image Texture", "Vector"), ("Image Texture.002", "Vector")],
    "Limbal UV": [
        ("[AetherBlend] Limbal Rings", "UVMap"),
    ],
}

_IRIS_SHADER_CUSTOM_PROPERTIES = [("Eye Scale X", 1.0), ("Eye Scale Y", 1.0), ("Pupil Scale", 0.0)]

_LIMBAL_SHADER_INPUT_CONNECTIONS = {
    "UVMap": [
        ("UV Map", "UV"),
        ("[AetherBlend] Eye Scaling", "Limbal UV"),
    ],
    "vertex_color": [
        ("Color Attribute", "Color"),
    ],
}

_LIMBAL_SHADER_OUTPUT_CONNECTIONS = {
    "Emission Color": [("Principled BSDF", "Emission Color")],
    "Emission Strength": [("Principled BSDF", "Emission Strength")],
}

# socket, material_prop, index (if applicable)
_IRIS_SHADER_CUSTOM_MAPPINGS = []

_LIMBAL_SHADER_CUSTOM_MAPPING = [
    ("left_iris_limbal_ring_intensity", "LeftIrisColor", 3),
    ("right_iris_limbal_ring_intensity", "RightIrisColor", 3),
]


class AETHER_OT_shaders_iris(bpy.types.Operator):
    bl_idname = "aether.shaders_iris"
    bl_label = "Set Up Iris"
    bl_description = "Apply AetherBlend Iris node-group setup to iris materials"

    group_name: ClassVar[str] = "[AetherBlend] Eye Scaling"

    def execute(self, context: bpy.types.Context) -> set[str]:
        try:
            armature = context.active_object
            if not armature or armature.type != "ARMATURE":
                self.report({"ERROR"}, "Please select an armature object.")
                return {"CANCELLED"}

            #####
            # Get Material
            #####
            meshes = find_meshes(armature)
            if not meshes:
                self.report({"ERROR"}, "No meshes found using the selected armature.")
                return {"CANCELLED"}

            eyes = shader_util.find_material_by_property(meshes, "ShaderPackage", "iris.shpk")
            if not eyes:
                self.report(
                    {"ERROR"}, "No materials with ShaderPackage='iris.shpk' found on meshes driven by the armature."
                )
                return {"CANCELLED"}

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
            shader_util.pop_default_mappings(eye_material, group_node)

            ####
            # Apply custom Mapping
            ####
            shader_util.pop_custom_mappings(eye_material, group_node, _IRIS_SHADER_CUSTOM_MAPPINGS)

            #####
            ## Connect node group
            #####
            shader_util.connect_sockets(
                eye_material.node_tree, group_node, _IRIS_SHADER_INPUT_CONNECTIONS, _IRIS_SHADER_OUTPUT_CONNECTIONS
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

            self.report({"INFO"}, f"Node group '{self.group_name}' appended successfully.")
        except ValueError as e:
            self.report({"ERROR"}, str(e))
        return {"FINISHED"}


class AETHER_OT_shaders_limbal(bpy.types.Operator):
    bl_idname = "aether.shaders_limbal"
    bl_label = "Set Up Limbal Rings"
    bl_description = "Apply AetherBlend Limbal Rings node-group setup to iris materials"

    group_name: ClassVar[str] = "[AetherBlend] Limbal Rings"

    def execute(self, context: bpy.types.Context) -> set[str]:
        try:
            armature = context.active_object
            if not armature or armature.type != "ARMATURE":
                self.report({"ERROR"}, "Please select an armature object.")
                return {"CANCELLED"}

            #####
            # Get Material
            #####
            meshes = find_meshes(armature)
            if not meshes:
                self.report({"ERROR"}, "No meshes found using the selected armature.")
                return {"CANCELLED"}

            eyes = shader_util.find_material_by_property(meshes, "ShaderPackage", "iris.shpk")
            if not eyes:
                self.report(
                    {"ERROR"}, "No materials with ShaderPackage='iris.shpk' found on meshes driven by the armature."
                )
                return {"CANCELLED"}

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
            shader_util.pop_default_mappings(eye_material, group_node)

            ####
            # Apply custom Mapping
            ####
            shader_util.pop_custom_mappings(eye_material, group_node, _LIMBAL_SHADER_CUSTOM_MAPPING)

            #####
            ## Connect node group
            #####
            shader_util.connect_sockets(
                eye_material.node_tree, group_node, _LIMBAL_SHADER_INPUT_CONNECTIONS, _LIMBAL_SHADER_OUTPUT_CONNECTIONS
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

            self.report({"INFO"}, f"Node group '{self.group_name}' appended successfully.")
        except ValueError as e:
            self.report({"ERROR"}, str(e))
        return {"FINISHED"}


class AETHER_OT_shaders_ffgear(bpy.types.Operator):
    bl_idname = "aether.shaders_ffgear"
    bl_label = "Set Up FFGEAR"
    bl_description = "Run FFGear shader import for meshes bound to the selected armature"

    filter_glob: bpy.props.StringProperty(default="*.nofilesplease", options={"HIDDEN"})  # type: ignore
    filepath: bpy.props.StringProperty(subtype="FILE_PATH")  # type: ignore

    def invoke(self, context: bpy.types.Context, event: bpy.types.Event) -> set[str]:
        prefs = get_preferences()
        if prefs.default_meddle_import_path:
            self.filepath = prefs.default_meddle_import_path

        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}

    def execute(self, context: bpy.types.Context) -> set[str]:
        if not addon_dependencies.is_addon_enabled(display_name="FFGear"):
            self.report({"ERROR"}, "FFGear add-on is not enabled")
            return {"CANCELLED"}

        try:
            armature = context.active_object
            if not armature or armature.type != "ARMATURE":
                self.report({"ERROR"}, "Please select an armature object.")
                return {"CANCELLED"}

            # Get affected Meshes
            meshes = find_meshes(armature)

            # Reroute to FFGear Operator
            ok = shader_util.import_ffgear_shader(self.filepath, meshes)
            if not ok:
                self.report({"ERROR"}, "Failed to import FFGear shader")
                return {"CANCELLED"}

            # Making sure only rig is selcted afterwards
            for obj in context.selected_objects:
                obj.select_set(False)

            armature.select_set(True)

            self.report({"INFO"}, "FFGEAR shader imported successfully.")
        except Exception as e:
            self.report({"ERROR"}, str(e))
            return {"CANCELLED"}
        return {"FINISHED"}


class AETHER_OT_shaders_meddle(bpy.types.Operator):
    bl_idname = "aether.shaders_meddle"
    bl_label = "Set Up Meddle"
    bl_description = "Run Meddle shader import for meshes bound to the selected armature"

    filter_glob: bpy.props.StringProperty(default="*.nofilesplease", options={"HIDDEN"})  # type: ignore
    filepath: bpy.props.StringProperty(subtype="FILE_PATH")  # type: ignore

    def invoke(self, context: bpy.types.Context, event: bpy.types.Event) -> set[str]:
        prefs = get_preferences()
        if prefs.default_meddle_import_path:
            self.filepath = prefs.default_meddle_import_path

        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}

    def execute(self, context: bpy.types.Context) -> set[str]:
        if not addon_dependencies.is_addon_enabled(display_name="Meddle Tools"):
            self.report({"ERROR"}, "Meddle Tools add-on is not enabled")
            return {"CANCELLED"}

        window = context.window
        if window:
            window.cursor_set("WAIT")

        try:
            armature = context.active_object
            if not armature or armature.type != "ARMATURE":
                self.report({"ERROR"}, "Please select an armature object.")
                return {"CANCELLED"}

            # Get affected Meshes
            meshes = find_meshes(armature)

            # Reroute to Meddle Operator
            ok = shader_util.import_meddle_shader(self.filepath, meshes)
            if not ok:
                self.report({"ERROR"}, "Failed to import Meddle shader")
                return {"CANCELLED"}

            # Making sure only rig is selcted afterwards
            for obj in context.selected_objects:
                obj.select_set(False)

            armature.select_set(True)

            self.report({"INFO"}, "Meddle shader imported successfully.")
        except Exception as e:
            self.report({"ERROR"}, str(e))
            return {"CANCELLED"}
        finally:
            if window:
                window.cursor_set("DEFAULT")

        return {"FINISHED"}


def register() -> None:
    """Register this module's classes."""
    bpy.utils.register_class(AETHER_OT_shaders_iris)
    bpy.utils.register_class(AETHER_OT_shaders_limbal)
    bpy.utils.register_class(AETHER_OT_shaders_ffgear)
    bpy.utils.register_class(AETHER_OT_shaders_meddle)


def unregister() -> None:
    """Unregister this module's classes."""
    bpy.utils.unregister_class(AETHER_OT_shaders_iris)
    bpy.utils.unregister_class(AETHER_OT_shaders_limbal)
    bpy.utils.unregister_class(AETHER_OT_shaders_ffgear)
    bpy.utils.unregister_class(AETHER_OT_shaders_meddle)
