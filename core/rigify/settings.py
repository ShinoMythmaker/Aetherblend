import bpy
from dataclasses import dataclass

@dataclass
class BoneCollection:
    name: str
    ui: bool = False
    color_set: str = None
    row_index: int = 0
    title: str = ""
    visible: bool = True

    def create(self, armature: bpy.types.Object) -> bpy.types.BoneCollection | None:
        """Creates the bone collection in the armature."""
        if not armature or armature.type != 'ARMATURE':
            print(f"[AetherBlend] Invalid armature provided for bone collection creation.")
            return None
        
        coll = armature.data.collections.get(self.name)
        if not coll:
            coll = armature.data.collections.new(self.name)
        
        return coll

    def create_ui(self, armature: bpy.types.Object) -> type[tuple[bpy.types.BoneCollection | None, bool]]:
        """Creates the bone collection UI in the armature."""
        if not armature or armature.type != 'ARMATURE':
            return None, False
        
        coll = armature.data.collections.get(self.name)
        hide_collections = False
        if coll:
            if self.ui:
                if self.color_set:
                    coll.rigify_color_set_name = self.color_set
                coll.rigify_ui_row = self.row_index
                coll.rigify_ui_title = self.title

            if not self.visible:
                hide_collections = True

            return coll,  hide_collections
        return None, False
    
class UI_Collections:
    collections: list[BoneCollection]

    def __init__(self, collections: list[BoneCollection] | None = None):
        self.collections = collections if collections else []

    def add(self, diff: 'UI_Collections'):
        """Adds another UI_Collections to this one, changing row IDs to avoid conflicts."""
        max_row_index = max((coll.row_index for coll in self.collections), default=0)

        for coll in diff.collections:
            coll.row_index += max_row_index + 1
            self.collections.append(coll)

@dataclass(frozen=True)
class ColorSet:
    name: str
    normal: str = "#00EDFF"
    select: str = "#FFFFFF"
    active: str = "#FFFF00"

    def add(self, armature: bpy.types.Object) -> None:
        """Applies the color set to the given rigify armature."""
        if not armature or armature.type != 'ARMATURE':
            print(f"[AetherBlend] Invalid armature provided for color set application.")
            return
        
        ## make sure armature is selected
        bpy.context.view_layer.objects.active = armature
        bpy.ops.object.mode_set(mode='OBJECT')
        
        bpy.ops.armature.rigify_color_set_add()
        color_set = armature.data.rigify_colors[-1]

        color_set.name = self.name
        color_set.normal = self._hex_to_rgb(self.normal)
        color_set.select = self._hex_to_rgb(self.select)
        color_set.active = self._hex_to_rgb(self.active)

    def _hex_to_rgb(self, hex_color: str) -> tuple[float, float, float]:
        """Converts a hex color string to an RGB tuple with sRGB gamma correction."""
        hex_color = hex_color.lstrip('#')
        lv = len(hex_color)
        
        def srgb_to_linear(value: float) -> float:
            """Convert sRGB to linear color space."""
            value = value / 255.0
            if value <= 0.04045:
                return value / 12.92
            return ((value + 0.055) / 1.055) ** 2.4
        
        return tuple(srgb_to_linear(int(hex_color[i:i + lv // 3], 16)) for i in range(0, lv, lv // 3))