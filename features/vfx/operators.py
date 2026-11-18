"""VFX object creation and specialized glTF export operators."""

import json
import os
from collections.abc import Iterable

import bmesh
import bpy
from bpy.types import Menu, Operator
from bpy_extras.io_utils import ExportHelper

from ...preferences import get_preferences


def _rename_gltf_attribute(filepath: str, old_name: str, new_name: str) -> None:
    """Rename a mesh primitive attribute key in a glTF file."""
    with open(filepath, "r", encoding="utf-8") as file:
        gltf_data = json.load(file)

    for mesh in gltf_data.get("meshes", []):
        for primitive in mesh.get("primitives", []):
            attributes = primitive.get("attributes", {})
            if old_name in attributes:
                attributes[new_name] = attributes.pop(old_name)

    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(gltf_data, file, indent=2)


def _create_uv_offset_duplicates(
    context: bpy.types.Context,
    objects: Iterable[bpy.types.Object],
    offset_u: float,
    offset_v: float,
) -> list[bpy.types.Object]:
    """Bake evaluated meshes into triangulated temp objects, shifting every UV layer if an offset is given."""
    depsgraph = context.evaluated_depsgraph_get()
    temp_objects = []
    temp_meshes = []
    try:
        for obj in objects:
            if obj.type != "MESH":
                continue
            obj_eval = obj.evaluated_get(depsgraph)
            mesh = bpy.data.meshes.new_from_object(obj_eval, preserve_all_data_layers=True, depsgraph=depsgraph)
            if mesh is None:
                raise RuntimeError(f"Could not create an evaluated mesh for '{obj.name}'.")
            temp_meshes.append(mesh)

            bm = bmesh.new()
            try:
                bm.from_mesh(mesh)
                bmesh.ops.triangulate(bm, faces=bm.faces[:])
                bm.to_mesh(mesh)
            finally:
                bm.free()
            mesh.update()

            if (offset_u or offset_v) and mesh.uv_layers:
                for uv_layer in mesh.uv_layers:
                    for loop in uv_layer.data:
                        loop.uv.x += offset_u
                        loop.uv.y += offset_v

            temp_obj = bpy.data.objects.new(obj.name + "_vfx_export_tmp", mesh)
            temp_objects.append(temp_obj)
            temp_obj.matrix_world = obj.matrix_world
            collection = obj.users_collection[0] if obj.users_collection else context.collection
            collection.objects.link(temp_obj)
        return temp_objects
    except Exception:
        for obj in temp_objects:
            bpy.data.objects.remove(obj, do_unlink=True)
        for mesh in temp_meshes:
            if bpy.data.meshes.get(mesh.name) is mesh and mesh.users == 0:
                bpy.data.meshes.remove(mesh)
        raise


def _remove_temp_objects(temp_objects: Iterable[bpy.types.Object]) -> None:
    """Remove temporary export objects and their unused meshes."""
    for obj in temp_objects:
        mesh = obj.data
        bpy.data.objects.remove(obj, do_unlink=True)
        if mesh.users == 0:
            bpy.data.meshes.remove(mesh)


def _spawn_opp_object(
    operator: bpy.types.Operator,
    context: bpy.types.Context,
    object_name: str,
) -> set[str]:
    """Append a named VFX template object from the bundled asset."""
    blend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "assets", "blend", "opp.blend"))
    if not os.path.exists(blend_path):
        operator.report({"ERROR"}, f"Could not find blend file: {blend_path}")
        return {"CANCELLED"}

    object_path = os.path.join(blend_path, "Object") + os.sep

    existing_objects = set(bpy.data.objects)
    try:
        bpy.ops.wm.append(
            filepath=os.path.join(object_path, object_name),
            directory=object_path,
            filename=object_name,
            link=False,
            autoselect=True,
        )
    except RuntimeError as exc:
        operator.report({"ERROR"}, f"Failed to append {object_name}: {exc}")
        return {"CANCELLED"}

    obj = next(
        (obj for obj in bpy.data.objects if obj not in existing_objects and obj.name.startswith(object_name)),
        None,
    )
    if obj is None:
        operator.report({"ERROR"}, f"The {object_name} object could not be created.")
        return {"CANCELLED"}

    obj.select_set(True)
    context.view_layer.objects.active = obj
    context.view_layer.update()

    operator.report({"INFO"}, f"Added {object_name} to the scene")
    return {"FINISHED"}


class AETHER_OT_VFXSpawnOPPCurve(Operator):
    """Create an OPP curve template."""

    bl_idname = "aether.vfx_spawn_opp_curve"
    bl_label = "OPP Curve"

    def execute(self, context: bpy.types.Context) -> set[str]:
        """Append an OPP curve."""
        return _spawn_opp_object(self, context, "OPP Curve")


class AETHER_OT_VFXSpawnOPPCircle(Operator):
    """Create an OPP circle template."""

    bl_idname = "aether.vfx_spawn_opp_circle"
    bl_label = "OPP Circle"

    def execute(self, context: bpy.types.Context) -> set[str]:
        """Append an OPP circle."""
        return _spawn_opp_object(self, context, "OPP Circle")


class AETHER_OT_VFXSpawnOPPPath(Operator):
    """Create an OPP path template."""

    bl_idname = "aether.vfx_spawn_opp_path"
    bl_label = "OPP Path"

    def execute(self, context: bpy.types.Context) -> set[str]:
        """Append an OPP path."""
        return _spawn_opp_object(self, context, "OPP Path")


class AETHER_OT_VFXSpawnEmicloudCube(Operator):
    """Create an EmiCloud cube template."""

    bl_idname = "aether.vfx_spawn_emicloud_cube"
    bl_label = "Emicloud Cube"

    def execute(self, context: bpy.types.Context) -> set[str]:
        """Append an EmiCloud cube."""
        return _spawn_opp_object(self, context, "EmiCloud Cube")


class AETHER_OT_VFXSpawnEmicloudCylinder(Operator):
    """Create an EmiCloud cylinder template."""

    bl_idname = "aether.vfx_spawn_emicloud_cylinder"
    bl_label = "Emicloud Cylinder"

    def execute(self, context: bpy.types.Context) -> set[str]:
        """Append an EmiCloud cylinder."""
        return _spawn_opp_object(self, context, "EmiCloud Cylinder")


class AETHER_OT_VFXSpawnEmicloudSphere(Operator):
    """Create an EmiCloud sphere template."""

    bl_idname = "aether.vfx_spawn_emicloud_sphere"
    bl_label = "Emicloud Sphere"

    def execute(self, context: bpy.types.Context) -> set[str]:
        """Append an EmiCloud sphere."""
        return _spawn_opp_object(self, context, "EmiCloud Sphere")


class AETHER_OT_VFXSpawnEmicloudCone(Operator):
    """Create an EmiCloud cone template."""

    bl_idname = "aether.vfx_spawn_emicloud_cone"
    bl_label = "Emicloud Cone"

    def execute(self, context: bpy.types.Context) -> set[str]:
        """Append an EmiCloud cone."""
        return _spawn_opp_object(self, context, "EmiCloud Cone")


class AETHER_OT_VFXSpawnEmicloudTorus(Operator):
    """Create an EmiCloud torus template."""

    bl_idname = "aether.vfx_spawn_emicloud_torus"
    bl_label = "Emicloud Torus"

    def execute(self, context: bpy.types.Context) -> set[str]:
        """Append an EmiCloud torus."""
        return _spawn_opp_object(self, context, "EmiCloud Torus")


class AETHER_MT_VFXModel(Menu):
    """Menu containing the bundled VFX model templates."""

    bl_idname = "AETHER_MT_vfx_model"
    bl_label = "VFX Model"

    def draw(self, context: bpy.types.Context) -> None:
        """Draw the template submenus."""
        self.layout.menu("AETHER_MT_vfx_projection_plane", text="Projection Plane", icon="IMAGE_PLANE")
        self.layout.menu("AETHER_MT_vfx_emicloud", text="Emiclouds", icon="OUTLINER_OB_POINTCLOUD")


class AETHER_MT_VFXProjectionPlane(Menu):
    """Menu of OPP projection plane templates."""

    bl_idname = "AETHER_MT_vfx_projection_plane"
    bl_label = "Projection Plane"

    def draw(self, context: bpy.types.Context) -> None:
        """Draw OPP template operators."""
        self.layout.operator(AETHER_OT_VFXSpawnOPPCurve.bl_idname, text="OPP Curve", icon="CURVE_DATA")
        self.layout.operator(AETHER_OT_VFXSpawnOPPCircle.bl_idname, text="OPP Circle", icon="MESH_CIRCLE")
        self.layout.operator(AETHER_OT_VFXSpawnOPPPath.bl_idname, text="OPP Path", icon="CURVE_PATH")


class AETHER_MT_VFXEmiClouds(Menu):
    """Menu of EmiCloud mesh templates."""

    bl_idname = "AETHER_MT_vfx_emicloud"
    bl_label = "Emiclouds"

    def draw(self, context: bpy.types.Context) -> None:
        """Draw EmiCloud template operators."""
        self.layout.operator(AETHER_OT_VFXSpawnEmicloudCube.bl_idname, text="EmiCloud Cube", icon="MESH_CUBE")
        self.layout.operator(AETHER_OT_VFXSpawnEmicloudCylinder.bl_idname, text="EmiCloud Cylinder", icon="MESH_CYLINDER")
        self.layout.operator(AETHER_OT_VFXSpawnEmicloudSphere.bl_idname, text="EmiCloud Sphere", icon="MESH_UVSPHERE")
        self.layout.operator(AETHER_OT_VFXSpawnEmicloudCone.bl_idname, text="EmiCloud Cone", icon="MESH_CONE")
        self.layout.operator(AETHER_OT_VFXSpawnEmicloudTorus.bl_idname, text="EmiCloud Torus", icon="MESH_TORUS")


class AETHER_OT_VFXExportModel(Operator, ExportHelper):
    """Export selected objects as a triangulated VFX GLB model."""

    bl_idname = "aether.vfx_export_model"
    bl_label = "Export VFX Model (GLB)"
    bl_options = {"REGISTER", "UNDO"}
    bl_description = "Export VFX Model. This is meant for VFX not Animations !"

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")  # type: ignore
    filename_ext = ".glb"
    filter_glob: bpy.props.StringProperty(default="*.glb", options={"HIDDEN"})  # type: ignore

    uv_offset_u: bpy.props.FloatProperty(name="U Offset", default=0.0)  # type: ignore
    uv_offset_v: bpy.props.FloatProperty(name="V Offset", default=0.0)  # type: ignore

    def invoke(self, context: bpy.types.Context, event: bpy.types.Event) -> set[str]:
        """Initialize the file browser with the user's VFX export path."""
        prefs = get_preferences()
        blend_filename = bpy.path.basename(bpy.data.filepath)
        if blend_filename:
            blend_filename = os.path.splitext(blend_filename)[0] + "_vfx.glb"
        else:
            blend_filename = "untitled_vfx_model.glb"

        if prefs.default_vfx_export_path:
            self.filepath = os.path.join(prefs.default_vfx_export_path, blend_filename)
        else:
            self.filepath = blend_filename

        return super().invoke(context, event)

    def draw(self, context: bpy.types.Context) -> None:
        """Draw UV offset options in the file browser."""
        layout = self.layout
        layout.prop(self, "uv_offset_u")
        layout.prop(self, "uv_offset_v")

    def execute(self, context: bpy.types.Context) -> set[str]:
        """Bake selected geometry, apply UV offsets, and export it."""
        original_selection = list(context.selected_objects)
        if not original_selection:
            self.report({"ERROR"}, "Please select objects to export.")
            return {"CANCELLED"}

        active_obj = context.view_layer.objects.active
        temp_objects = []

        try:
            # triangulated meshes and shift their UVs before export
            temp_objects = _create_uv_offset_duplicates(context, original_selection, self.uv_offset_u, self.uv_offset_v)
            if not temp_objects:
                self.report({"ERROR"}, "No selected objects could be converted to export meshes.")
                return {"CANCELLED"}
            for obj in original_selection:
                obj.select_set(False)
            for obj in temp_objects:
                obj.select_set(True)
            if temp_objects:
                context.view_layer.objects.active = temp_objects[0]

            result = bpy.ops.export_scene.gltf(
                filepath=self.filepath,
                export_format="GLB",
                use_selection=True,
                export_yup=True,  # Y up enabled for VFX
                export_apply=True,
                export_animations=False,
                export_normals=True,
                export_tangents=True,  # keep tangents
                export_attributes=True,
                export_materials="NONE",
                export_image_format="NONE",
                use_mesh_edges=False,
                use_mesh_vertices=False,
            )
            if "FINISHED" not in result:
                self.report({"ERROR"}, "The glTF exporter did not complete.")
                return {"CANCELLED"}
            self.report({"INFO"}, f"VFX model exported to {self.filepath}")
            return {"FINISHED"}

        except Exception as e:
            self.report({"ERROR"}, f"Export failed: {str(e)}")
            return {"CANCELLED"}

        finally:
            if temp_objects:
                _remove_temp_objects(temp_objects)
            for obj in original_selection:
                obj.select_set(True)
            context.view_layer.objects.active = active_obj


class AETHER_OT_VFXExportEmitter(Operator, ExportHelper):
    """Export selected objects as a VFX emitter glTF."""

    bl_idname = "aether.vfx_export_emitter"
    bl_label = "Export VFX Emitter (GLTF)"
    bl_options = {"REGISTER", "UNDO"}
    bl_description = "Export VFX Emitter Model, This is meant for VFX"

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")  # type: ignore
    filename_ext = ".gltf"
    filter_glob: bpy.props.StringProperty(default="*.gltf", options={"HIDDEN"})  # type: ignore

    def invoke(self, context: bpy.types.Context, event: bpy.types.Event) -> set[str]:
        """Initialize the file browser with the user's VFX export path."""
        prefs = get_preferences()
        blend_filename = bpy.path.basename(bpy.data.filepath)
        if blend_filename:
            blend_filename = os.path.splitext(blend_filename)[0] + "_vfx.gltf"
        else:
            blend_filename = "untitled_vfx_emitter.gltf"

        if prefs.default_vfx_export_path:
            self.filepath = os.path.join(prefs.default_vfx_export_path, blend_filename)
        else:
            self.filepath = blend_filename

        return super().invoke(context, event)

    def execute(self, context: bpy.types.Context) -> set[str]:
        """Export selected emitter geometry and rename its normal attribute."""
        if not context.selected_objects:
            self.report({"ERROR"}, "Please select objects to export.")
            return {"CANCELLED"}

        try:
            result = bpy.ops.export_scene.gltf(
                filepath=self.filepath,
                export_format="GLTF_SEPARATE",
                use_selection=True,
                export_yup=True,  # Y up enabled for VFX
                export_apply=True,
                export_animations=False,
                export_normals=False,
                export_tangents=False,
                export_attributes=True,
                export_materials="EXPORT",
                export_image_format="AUTO",
                use_mesh_edges=False,
                use_mesh_vertices=True,
            )
            if "FINISHED" not in result:
                self.report({"ERROR"}, "The glTF exporter did not complete.")
                return {"CANCELLED"}

            _rename_gltf_attribute(self.filepath, "_CUSTOM_NORMAL", "NORMAL")

            self.report({"INFO"}, f"VFX model exported to {self.filepath}")
            return {"FINISHED"}

        except Exception as e:
            self.report({"ERROR"}, f"Export failed: {str(e)}")
            return {"CANCELLED"}


def _menu_draw(self: bpy.types.Menu, context: bpy.types.Context) -> None:
    """Add VFX model templates to Blender's Add menu."""
    self.layout.menu(AETHER_MT_VFXModel.bl_idname, icon="GEOMETRY_SET")


CLASSES = (
    AETHER_OT_VFXSpawnOPPCurve,
    AETHER_OT_VFXSpawnOPPCircle,
    AETHER_OT_VFXSpawnOPPPath,
    AETHER_OT_VFXSpawnEmicloudCube,
    AETHER_OT_VFXSpawnEmicloudCylinder,
    AETHER_OT_VFXSpawnEmicloudSphere,
    AETHER_OT_VFXSpawnEmicloudCone,
    AETHER_OT_VFXSpawnEmicloudTorus,
    AETHER_MT_VFXProjectionPlane,
    AETHER_MT_VFXEmiClouds,
    AETHER_MT_VFXModel,
    AETHER_OT_VFXExportModel,
    AETHER_OT_VFXExportEmitter,
)


def register() -> None:
    """Register VFX operators, menus, and Blender's Add menu hook."""
    for cls in CLASSES:
        bpy.utils.register_class(cls)
    bpy.types.VIEW3D_MT_add.append(_menu_draw)


def unregister() -> None:
    """Unregister VFX operators, menus, and Blender's Add menu hook."""
    bpy.types.VIEW3D_MT_add.remove(_menu_draw)
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)
