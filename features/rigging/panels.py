import bpy
import addon_utils

from . import module_manager
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
        
        # Template selection at the top
        box = layout.box()
        row = box.row(align=True)
        row.label(text="Template:", icon='PRESET')
        row.prop(aether_rig, "template_dropdown", text="")
        load_op = row.operator("aether.load_template", text="", icon='IMPORT')
        load_op.template_name = aether_rig.template_dropdown
        
        layout.separator()
        
        # Iterate through all module types
        for module_type, config in module_manager.MODULE_TYPE_CONFIG.items():
            box = layout.box()
            row = box.row()
            row.label(text=config['label'], icon=config['icon'])
            
            # Display selected modules
            selected_modules = module_manager.get_selected_modules(aether_rig, module_type)
            for i, module_name in enumerate(selected_modules):
                row = box.row(align=True)
                row.label(text=module_name, icon='CHECKMARK')
                
                # Up button
                up_col = row.column(align=True)
                up_col.enabled = i > 0
                up_op = up_col.operator("aether.move_module_up", text="", icon='TRIA_UP')
                up_op.module_type = module_type
                up_op.module_name = module_name
                
                # Down button
                down_col = row.column(align=True)
                down_col.enabled = i < len(selected_modules) - 1
                down_op = down_col.operator("aether.move_module_down", text="", icon='TRIA_DOWN')
                down_op.module_type = module_type
                down_op.module_name = module_name
                
                # Remove button
                remove_op = row.operator("aether.remove_module_from_rig", text="", icon='X')
                remove_op.module_type = module_type
                remove_op.module_name = module_name
            
            # Dropdown to add new module
            available_modules = [key for key in config['available_modules'].keys() if key not in selected_modules]
            if available_modules:
                row = box.row(align=True)
                row.prop(aether_rig, config['dropdown_property'], text="")
                add_op = row.operator("aether.add_module_to_rig", text="", icon='ADD')
                add_op.module_type = module_type
                add_op.module_name = getattr(aether_rig, config['dropdown_property'])


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