import bpy
import addon_utils
from ...preferences import get_preferences

class AETHER_PT_RigCreation(bpy.types.Panel):
    bl_label = "Create Rig"
    bl_idname = "AETHER_PT_rig_creation_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AetherBlend'
    bl_order = 4

    @classmethod
    def poll(cls, context):
        if context.scene.aether_tabs.active_tab != 'GENERATE':
            return False

        armature = context.active_object
        return (
            armature is not None 
            and armature.visible_get()
            and armature.type == 'ARMATURE' 
            and getattr(armature, 'aether_rig', None)
        )

    def draw(self, context):
        addon_enabled = addon_utils.check("rigify")[0]
        if not addon_enabled:
            layout = self.layout
            box = layout.box()
            box.label(text="Rigify addon is not enabled", icon='ERROR')
            return None
        
        layout = self.layout
        armature = context.active_object
        aether_rig = getattr(armature, 'aether_rig', None)
        if not aether_rig:
            return

        col = layout.column(align=True)
        
        full_rig_button = col.row(align=True)
        full_rig_button.scale_y = 1.3
        if aether_rig.rigified:
            full_rig_button.operator("aether.generate_full_rig", text="Regenerate", icon="FILE_REFRESH")
        else:
            full_rig_button.operator("aether.generate_full_rig", text="Generate Rig", icon="PLAY")

        unlink = full_rig_button.column(align=False)
        unlink.scale_x = 1.3
        unlink.operator("aether.clean_up_rig", text="", icon="UNLINKED")


        reset = full_rig_button.column(align=False)
        reset.scale_x = 1.3
        reset.operator("aether.reset_rig", text="", icon="RESTRICT_INSTANCED_ON")
        
        col.separator()
        
        row = col.row(align=True)
        
        meta_col = row.column(align=True)
        meta_col.operator("aether.generate_meta_rig", text="Meta", icon="OUTLINER_DATA_ARMATURE")
        

        control_col = row.column(align=True)
        control_col.enabled = bool(aether_rig.meta_rig)
        
        control_col.operator("aether.generate_rigify_rig", text="Control", icon="OUTLINER_OB_ARMATURE")


class AETHER_PT_RigModuleSelection(bpy.types.Panel):
    bl_label = "Rig Modules"
    bl_idname = "AETHER_PT_rig_module_selection"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AetherBlend'
    bl_parent_id = "AETHER_PT_rig_creation_panel"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        armature = context.active_object
        aether_rig = armature.aether_rig
        
        from .templates import CS_COLORSETS, UI_COLLECTIONS, WO_OVERRIDES, BG_GROUPS
        
        # Colorsets Section
        box = layout.box()
        row = box.row()
        row.label(text="Colorsets", icon='COLOR')
        
        # Display selected colorsets
        selected_colorsets = [m.strip() for m in aether_rig.selected_colorsets.split(",") if m.strip()]
        for i, module_name in enumerate(selected_colorsets):
            row = box.row(align=True)
            row.label(text=module_name, icon='CHECKMARK')
            
            # Up button
            up_col = row.column(align=True)
            up_col.enabled = i > 0
            up_op = up_col.operator("aether.move_module_up", text="", icon='TRIA_UP')
            up_op.module_type = 'colorset'
            up_op.module_name = module_name
            
            # Down button
            down_col = row.column(align=True)
            down_col.enabled = i < len(selected_colorsets) - 1
            down_op = down_col.operator("aether.move_module_down", text="", icon='TRIA_DOWN')
            down_op.module_type = 'colorset'
            down_op.module_name = module_name
            
            # Remove button
            op = row.operator("aether.remove_module_from_rig", text="", icon='X')
            op.module_type = 'colorset'
            op.module_name = module_name
        
        # Dropdown to add new colorset
        available_colorsets = [key for key in CS_COLORSETS.keys() if key not in selected_colorsets]
        if available_colorsets:
            row = box.row(align=True)
            row.prop(aether_rig, "dropdown_colorset", text="")
            op = row.operator("aether.add_module_to_rig", text="", icon='ADD')
            op.module_type = 'colorset'
            op.module_name = aether_rig.dropdown_colorset
        
        # UI Collections Section
        box = layout.box()
        row = box.row()
        row.label(text="UI Collections", icon='OUTLINER_COLLECTION')
        
        selected_ui = [m.strip() for m in aether_rig.selected_ui_collections.split(",") if m.strip()]
        for i, module_name in enumerate(selected_ui):
            row = box.row(align=True)
            row.label(text=module_name, icon='CHECKMARK')
            
            # Up button
            up_col = row.column(align=True)
            up_col.enabled = i > 0
            up_op = up_col.operator("aether.move_module_up", text="", icon='TRIA_UP')
            up_op.module_type = 'ui_collection'
            up_op.module_name = module_name
            
            # Down button
            down_col = row.column(align=True)
            down_col.enabled = i < len(selected_ui) - 1
            down_op = down_col.operator("aether.move_module_down", text="", icon='TRIA_DOWN')
            down_op.module_type = 'ui_collection'
            down_op.module_name = module_name
            
            # Remove button
            op = row.operator("aether.remove_module_from_rig", text="", icon='X')
            op.module_type = 'ui_collection'
            op.module_name = module_name
        
        available_ui = [key for key in UI_COLLECTIONS.keys() if key not in selected_ui]
        if available_ui:
            row = box.row(align=True)
            row.prop(aether_rig, "dropdown_ui_collection", text="")
            op = row.operator("aether.add_module_to_rig", text="", icon='ADD')
            op.module_type = 'ui_collection'
            op.module_name = aether_rig.dropdown_ui_collection
        
        # Widget Overrides Section
        box = layout.box()
        row = box.row()
        row.label(text="Widget Overrides", icon='MESH_CUBE')
        
        selected_wo = [m.strip() for m in aether_rig.selected_widget_overrides.split(",") if m.strip()]
        for i, module_name in enumerate(selected_wo):
            row = box.row(align=True)
            row.label(text=module_name, icon='CHECKMARK')
            
            # Up button
            up_col = row.column(align=True)
            up_col.enabled = i > 0
            up_op = up_col.operator("aether.move_module_up", text="", icon='TRIA_UP')
            up_op.module_type = 'widget_override'
            up_op.module_name = module_name
            
            # Down button
            down_col = row.column(align=True)
            down_col.enabled = i < len(selected_wo) - 1
            down_op = down_col.operator("aether.move_module_down", text="", icon='TRIA_DOWN')
            down_op.module_type = 'widget_override'
            down_op.module_name = module_name
            
            # Remove button
            op = row.operator("aether.remove_module_from_rig", text="", icon='X')
            op.module_type = 'widget_override'
            op.module_name = module_name
        
        available_wo = [key for key in WO_OVERRIDES.keys() if key not in selected_wo]
        if available_wo:
            row = box.row(align=True)
            row.prop(aether_rig, "dropdown_widget_override", text="")
            op = row.operator("aether.add_module_to_rig", text="", icon='ADD')
            op.module_type = 'widget_override'
            op.module_name = aether_rig.dropdown_widget_override
        
        # Bone Groups Section
        box = layout.box()
        row = box.row()
        row.label(text="Bone Groups", icon='GROUP_BONE')
        
        selected_bg = [m.strip() for m in aether_rig.selected_bone_groups.split(",") if m.strip()]
        for i, module_name in enumerate(selected_bg):
            row = box.row(align=True)
            row.label(text=module_name, icon='CHECKMARK')
            
            # Up button
            up_col = row.column(align=True)
            up_col.enabled = i > 0
            up_op = up_col.operator("aether.move_module_up", text="", icon='TRIA_UP')
            up_op.module_type = 'bone_group'
            up_op.module_name = module_name
            
            # Down button
            down_col = row.column(align=True)
            down_col.enabled = i < len(selected_bg) - 1
            down_op = down_col.operator("aether.move_module_down", text="", icon='TRIA_DOWN')
            down_op.module_type = 'bone_group'
            down_op.module_name = module_name
            
            # Remove button
            op = row.operator("aether.remove_module_from_rig", text="", icon='X')
            op.module_type = 'bone_group'
            op.module_name = module_name
        
        available_bg = [key for key in BG_GROUPS.keys() if key not in selected_bg]
        if available_bg:
            row = box.row(align=True)
            row.prop(aether_rig, "dropdown_bone_group", text="")
            op = row.operator("aether.add_module_to_rig", text="", icon='ADD')
            op.module_type = 'bone_group'
            op.module_name = aether_rig.dropdown_bone_group


class AETHER_PT_RigLayersPanel(bpy.types.Panel):
    bl_label = "Rig Layers"
    bl_idname = "AETHER_PT_rig_layers"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AetherBlend'
    bl_order = 5

    @classmethod
    def poll(cls, context):
        if context.scene.aether_tabs.active_tab != 'RIG_LAYERS':
            return False

        armature = context.active_object
        if not armature or armature.type != 'ARMATURE':
            return False
        
        # Get rig_id from armature custom properties
        rig_id = armature.data.get("rig_id")
        if not rig_id:
            return False
            
        panel_name = "VIEW3D_PT_rig_layers_" + rig_id
        panel_class = getattr(bpy.types, panel_name, None)
        
        if panel_class and hasattr(panel_class, 'poll'):
            return panel_class.poll(context)
        
        return False

    def draw(self, context):
        armature = context.active_object
        if not armature or armature.type != 'ARMATURE':
            return
        
        # Get rig_id from armature custom properties
        rig_id = armature.data.get("rig_id")
        if not rig_id:
            return
            
        panel_name = "VIEW3D_PT_rig_layers_" + rig_id
        panel_class = getattr(bpy.types, panel_name, None)
        
        if panel_class and hasattr(panel_class, 'draw'):
            panel_class.draw(self, context)
        else:
            # Fallback to default behavior if panel not found
            layout = self.layout
            layout.label(text=f"Rig layers panel not found for: {rig_id}")


class AETHER_PT_RigUIPanel(bpy.types.Panel):
    bl_label = "Rig UI"
    bl_idname = "AETHER_PT_rig_ui"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AetherBlend'
    bl_order = 6

    @classmethod
    def poll(cls, context):
        if context.scene.aether_tabs.active_tab != 'RIG_UI':
            return False
        
        armature = context.active_object
        if not armature or armature.type != 'ARMATURE':
            return False
        
        # Get rig_id from armature custom properties
        rig_id = armature.data.get("rig_id")
        if not rig_id:
            return False
            
        panel_name = "VIEW3D_PT_rig_ui_" + rig_id
        panel_class = getattr(bpy.types, panel_name, None)
        
        if panel_class and hasattr(panel_class, 'poll'):
            return panel_class.poll(context)
        
        return False

    def draw(self, context):
        armature = context.active_object
        if not armature or armature.type != 'ARMATURE':
            return
        
        rig_id = armature.data.get("rig_id")
        if not rig_id:
            return
            
        panel_name = "VIEW3D_PT_rig_ui_" + rig_id
        panel_class = getattr(bpy.types, panel_name, None)
        
        if panel_class and hasattr(panel_class, 'draw'):

            # layout = self.layout
            
            # selected_bones = {bone.name for bone in context.selected_pose_bones or []}
            
            # controllers_to_show = []
            # for bone_name in selected_bones:
            #     if bone_name in UI_CONTROLLER_MAPPING:
            #         controllers_to_show.extend(UI_CONTROLLER_MAPPING[bone_name])
            
            # seen = set()
            # unique_controllers = []
            # for controller in controllers_to_show:
            #     if controller.name not in seen:
            #         seen.add(controller.name)
            #         unique_controllers.append(controller)
            
            # if unique_controllers:
            #     for controller in unique_controllers:
            #         controller.create_ui(layout, armature)

            panel_class.draw(self, context)
        else:
            # Fallback to default behavior if panel not found
            layout = self.layout
            layout.label(text=f"Rig UI panel not found for: {rig_id}")
       


class AETHER_PT_RigBakeSettingsPanel(bpy.types.Panel):
    bl_label = "Rig Bake Settings"
    bl_idname = "AETHER_PT_rig_bake_settings"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AetherBlend'
    bl_order = 7

    @classmethod
    def poll(cls, context):
        if context.scene.aether_tabs.active_tab != 'RIG_UI':
            return False
        
        armature = context.active_object
        if not armature or armature.type != 'ARMATURE':
            return False
        
        # Get rig_id from armature custom properties
        rig_id = armature.data.get("rig_id")
        if not rig_id:
            return False
            
        panel_name = "VIEW3D_PT_rig_bake_settings_" + rig_id
        panel_class = getattr(bpy.types, panel_name, None)
        
        if panel_class and hasattr(panel_class, 'poll'):
            return panel_class.poll(context)
        
        return False

    def draw(self, context):
        armature = context.active_object
        if not armature or armature.type != 'ARMATURE':
            return
        
        # Get rig_id from armature custom properties
        rig_id = armature.data.get("rig_id")
        if not rig_id:
            return
            
        panel_name = "VIEW3D_PT_rig_bake_settings_" + rig_id
        panel_class = getattr(bpy.types, panel_name, None)
        
        if panel_class and hasattr(panel_class, 'draw'):
            panel_class.draw(self, context)
        else:
            # Fallback to default behavior if panel not found
            layout = self.layout
            layout.label(text=f"Rig bake settings panel not found for: {rig_id}")

def register():
    bpy.utils.register_class(AETHER_PT_RigCreation)
    bpy.utils.register_class(AETHER_PT_RigModuleSelection)
    bpy.utils.register_class(AETHER_PT_RigLayersPanel)
    bpy.utils.register_class(AETHER_PT_RigUIPanel)
    bpy.utils.register_class(AETHER_PT_RigBakeSettingsPanel)

def unregister():
    bpy.utils.unregister_class(AETHER_PT_RigCreation)
    bpy.utils.unregister_class(AETHER_PT_RigModuleSelection)
    bpy.utils.unregister_class(AETHER_PT_RigLayersPanel)
    bpy.utils.unregister_class(AETHER_PT_RigUIPanel)
    bpy.utils.unregister_class(AETHER_PT_RigBakeSettingsPanel)