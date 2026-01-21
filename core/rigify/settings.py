import bpy
from dataclasses import dataclass

@dataclass(frozen=True)
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

    def create_ui(self, armature: bpy.types.Object) -> type[tuple[bpy.types.BoneCollection | None, list[bpy.types.BoneCollection] | None]]:
        """Creates the bone collection UI in the armature."""
        if not armature or armature.type != 'ARMATURE':
            return None, []
        
        coll = armature.data.collections.get(self.name)
        hide_collections = []
        if coll:
            if self.ui:
                coll.rigify_color_set_name = self.color_set
                coll.rigify_ui_row = self.row_index
                coll.rigify_ui_title = self.title

            if not self.visible:
                hide_collections.append(coll)

            return coll,  hide_collections
        return None, []
    
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
        color_set.color_normal = self._hex_to_rgb(self.normal)
        color_set.color_select = self._hex_to_rgb(self.select)
        color_set.color_active = self._hex_to_rgb(self.active)

    def _hex_to_rgb(self, hex_color: str) -> tuple[float, float, float]:
        """Converts a hex color string to an RGB tuple."""
        hex_color = hex_color.lstrip('#')
        lv = len(hex_color)
        return tuple(int(hex_color[i:i + lv // 3], 16) / 255.0 for i in range(0, lv, lv // 3))