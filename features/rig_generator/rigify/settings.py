"""Bone collection and rig UI setting types."""

from dataclasses import dataclass

import bpy


@dataclass
class BoneCollection:
    """One curated collection's Rigify display settings and initial visibility."""

    name: str
    ui: bool = False
    color_set: str | None = None
    row_index: int = 0
    title: str = ""
    visible: bool = True

    def create(self, armature: bpy.types.Object) -> bpy.types.BoneCollection | None:
        """Create the bone collection in the armature."""
        if not armature or armature.type != "ARMATURE":
            print("[AetherBlend] Invalid armature provided for bone collection creation.")
            return None

        coll = armature.data.collections.get(self.name)
        if not coll:
            coll = armature.data.collections.new(self.name)

        return coll

    def create_ui(self, armature: bpy.types.Object) -> tuple[bpy.types.BoneCollection | None, bool]:
        """Create the bone collection UI in the armature."""
        if not armature or armature.type != "ARMATURE":
            return None, False

        coll = armature.data.collections.get(self.name)
        show_collection = True
        if coll:
            if self.ui:
                coll.rigify_color_set_name = self.color_set or ""
                coll.rigify_ui_row = self.row_index
                coll.rigify_ui_title = self.title
            coll.is_visible = self.visible

            if not self.visible:
                show_collection = False

            return coll, show_collection
        return None, True


@dataclass(frozen=True)
class ColorSet:
    name: str
    normal: str = "#00EDFF"
    select: str = "#FFFFFF"
    active: str = "#FFFF00"

    def add(self, armature: bpy.types.Object) -> None:
        """Apply the color set to the given rigify armature."""
        if not armature or armature.type != "ARMATURE":
            print("[AetherBlend] Invalid armature provided for color set application.")
            return

        ## make sure armature is selected
        bpy.context.view_layer.objects.active = armature
        bpy.ops.object.mode_set(mode="OBJECT")

        bpy.ops.armature.rigify_color_set_add()
        color_set = armature.data.rigify_colors[-1]

        color_set.name = self.name
        color_set.normal = self._hex_to_rgb(self.normal)
        color_set.select = self._hex_to_rgb(self.select)
        color_set.active = self._hex_to_rgb(self.active)

    def _hex_to_rgb(self, hex_color: str) -> tuple[float, float, float]:
        """Convert a hex color string to an RGB tuple with sRGB gamma correction."""
        hex_color = hex_color.lstrip("#")
        lv = len(hex_color)

        def srgb_to_linear(value: float) -> float:
            """Convert sRGB to linear color space."""
            value = value / 255.0
            if value <= 0.04045:
                return value / 12.92
            return ((value + 0.055) / 1.055) ** 2.4

        return tuple(srgb_to_linear(int(hex_color[i : i + lv // 3], 16)) for i in range(0, lv, lv // 3))
