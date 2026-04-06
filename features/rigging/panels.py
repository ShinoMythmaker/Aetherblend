import bpy
import addon_utils
import collections
from ...properties.tab_prop import get_active_tab
from ...utils.ui_visibility import visible_in_current_area
from . import template_manager


def _flatten_children(iterable):
    """Enumerate the iterator items as well as their children in the tree order."""
    for item in iterable:
        yield item
        yield from _flatten_children(item.children)


class AETHER_UL_RigModules(bpy.types.UIList):
    """Display the currently selected rig modules in a Blender-style list."""
    def draw_filter(self, context, layout):
        # Intentionally draw nothing so Blender does not show the filter/sort footer.
        pass

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        module = template_manager.AVAILABLE_MODULES.get(item.module_key)
        if not module:
            layout.label(text=item.module_key or "Unknown Module", icon='ERROR')
            return

        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            split = layout.split(factor=0.78, align=True)
            split.label(text=f"{module.type.replace('_', ' ').title()}", icon='GROUP_BONE')
            right = split.row(align=True)
            right.alignment = 'RIGHT'
            right.label(text=module.name)
        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(text="", icon='PROPERTIES')


class AETHER_PT_RigCreation(bpy.types.Panel):
    bl_label = "Create Rig"
    bl_idname = "AETHER_PT_rig_creation_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AetherBlend'
    bl_order = 4

    @classmethod
    def poll(cls, context):
        if not visible_in_current_area(context):
            return False
        if get_active_tab(context) != 'GENERATE':
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

        row = col.row(align=True)

        # Template selection
        row = layout.row(align=True)
        row.label(text="Template", icon='PRESET')
        row.prop(aether_rig, "selected_template", text="")
        
        # Colorset override
        row = layout.row(align=True)
        row.label(text="Colorset", icon='COLOR')
        row.prop(aether_rig, "selected_colorset", text="")

        modules_box = layout.box()
        modules_box.label(text="Modules", icon='MODIFIER')

        if len(aether_rig.modules) == 0:
            modules_box.label(text="No modules found for this template.", icon='INFO')
        else:
            row = modules_box.row()
            row.template_list(
                "AETHER_UL_RigModules",
                "",
                aether_rig,
                "modules",
                aether_rig,
                "module_index",
                rows=max(4, min(10, len(aether_rig.modules))),
                sort_lock=True,
            )

            buttons = row.column(align=True)
            remove = buttons.operator("aether.remove_template_module", text="", icon='REMOVE')
            remove.module_index = aether_rig.module_index


class AETHER_PT_RigManipulation(bpy.types.Panel):
    bl_label = "Rig Manipulation"
    bl_idname = "AETHER_PT_rig_manipulation"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AetherBlend'
    bl_order = 5

    @classmethod
    def poll(cls, context):
        if not visible_in_current_area(context):
            return False
        if get_active_tab(context) != 'GENERATE':
            return False

        armature = context.active_object
        if not armature or armature.type != 'ARMATURE':
            return False
        
        aether_rig = getattr(armature, 'aether_rig', None)
        return aether_rig and aether_rig.rigified

    def draw(self, context):
        layout = self.layout
        armature = context.active_object
        aether_rig = getattr(armature, 'aether_rig', None)
        
        link_collection = armature.data.collections.get('LINK')
        if not link_collection:
            layout.label(text="LINK collection not found", icon='ERROR')
            return
        
        row = layout.row(align=True)
        row.label(text="Inherit Scale", icon='ORIENTATION_PARENT')
        
        current_text = "Full"
        if aether_rig:
            scale_labels = {
                'FULL': 'Full',
                'FIX_SHEAR': 'Aligned',
                'AVERAGE': 'Average',
                'NONE': 'None',
                'NONE_LEGACY': 'None (Legacy)'
            }
            current_text = scale_labels.get(aether_rig.link_inherit_scale, 'Full')
        
        row.operator_menu_enum("aether.set_bone_inherit_scale", "inherit_scale", text=current_text)

        layout.separator()

        row = layout.row(align=True)

        row.label(text="NoAnim Bones", icon='BONE_DATA')
        row.operator(
            "aether.delete_no_anim",
            text="Delete",
            icon="TRASH", 
            )

class AETHER_PT_RigLayersPanel(bpy.types.Panel):
    bl_label = "Rig Layers"
    bl_idname = "AETHER_PT_rig_layers"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AetherBlend'
    bl_order = 6

    @classmethod
    def poll(cls, context):
        if not visible_in_current_area(context):
            return False
        if get_active_tab(context) != 'RIG_LAYERS':
            return False

        try:
            return (context.active_object.data.get("rig_id") is not None)
        except (AttributeError, KeyError, TypeError):
            return False

    def draw(self, context):
        armature = context.active_object
        if not armature or armature.type != 'ARMATURE':
            return

        if not armature.data.get("rig_id"):
            return
        
        layout = self.layout
        any_soloed = any(collection.is_solo for collection in armature.data.collections)
        
        ## AB Additions
        if context.mode == 'POSE':
            row = layout.row(align=True)
            row.operator(
                "aether.solo_bone_collections",
                text="Unsolo All" if any_soloed else "Solo Selected",
                icon='SOLO_ON' if any_soloed else 'SOLO_OFF',
                depress=any_soloed,
            )
            layout.separator()
            
        ## Rigify UI
        layout = self.layout
        row_table = collections.defaultdict(list)
        for coll in _flatten_children(context.active_object.data.collections):
            row_id = coll.rigify_ui_row
            if row_id > 0:
                row_table[row_id].append(coll)
        col = layout.column()
        for row_id in range(min(row_table.keys()), 1 + max(row_table.keys())):
            row = col.row()
            row_buttons = row_table[row_id]
            if row_buttons:
                midpoint = len(row_buttons) / 2
                for index, coll in enumerate(row_buttons):
                    title = coll.rigify_ui_title or coll.name
                    row2 = row.row(align=True)
                    
                    place_solo_left = index < midpoint
                    if len(row_buttons) == 1:
                        place_solo_left = False

                    if place_solo_left:
                        solo = row2.row(align=True)
                        visibility = row2.row(align=True)
                    else:
                        visibility = row2.row(align=True)
                        solo = row2.row(align=True)

                    visibility.enabled = coll.is_visible_ancestors and not any_soloed
                    visibility.prop(coll, 'is_visible', toggle=True, text=title, translate=False)
                    solo.prop(coll, 'is_solo', toggle=True, text="", icon='RADIOBUT_OFF' if not coll.is_solo else 'RADIOBUT_ON', translate=False)
            else:
                row.separator()

class AETHER_PT_RigUIPanel(bpy.types.Panel):
    bl_label = "Rig UI"
    bl_idname = "AETHER_PT_rig_ui"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AetherBlend'
    bl_order = 7

    @classmethod
    def poll(cls, context):
        if not visible_in_current_area(context):
            return False
        if get_active_tab(context) != 'RIG_UI':
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
    bl_order = 8

    @classmethod
    def poll(cls, context):
        if not visible_in_current_area(context):
            return False
        if get_active_tab(context) != 'RIG_UI':
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
    bpy.utils.register_class(AETHER_UL_RigModules)
    bpy.utils.register_class(AETHER_PT_RigCreation)
    bpy.utils.register_class(AETHER_PT_RigManipulation)
    bpy.utils.register_class(AETHER_PT_RigLayersPanel)
    bpy.utils.register_class(AETHER_PT_RigUIPanel)
    bpy.utils.register_class(AETHER_PT_RigBakeSettingsPanel)

def unregister():
    bpy.utils.unregister_class(AETHER_PT_RigBakeSettingsPanel)
    bpy.utils.unregister_class(AETHER_PT_RigUIPanel)
    bpy.utils.unregister_class(AETHER_PT_RigLayersPanel)
    bpy.utils.unregister_class(AETHER_PT_RigManipulation)
    bpy.utils.unregister_class(AETHER_PT_RigCreation)
    bpy.utils.unregister_class(AETHER_UL_RigModules)