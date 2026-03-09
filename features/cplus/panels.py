import bpy
from ...preferences import get_preferences
from ...properties.tab_prop import get_active_tab


def _visible_in_current_area(context):
    prefs = get_preferences()
    area = context.area
    if area is None:
        return True
    if area.type == 'VIEW_3D':
        return prefs.show_n_panel == 'ON'
    if area.type == 'PROPERTIES':
        return prefs.show_properties_tool_tab == 'ON'
    return True

class AETHER_PT_CustomizePlus(bpy.types.Panel):
    bl_label = "Customize Plus"
    bl_idname = "AETHER_PT_customize_plus"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'  
    bl_category = 'AetherBlend'
    bl_order = 2 
    
    @classmethod
    def poll(cls, context):
        if not _visible_in_current_area(context):
            return False
        if get_active_tab(context) != 'CPLUS':
            return False

        armature = context.active_object
        return (
            armature is not None 
            and armature.type == 'ARMATURE'
            and getattr(armature, 'aether_cplus', None)
        )
    
    def draw(self, context):
        armature = context.active_object
        if not armature or armature.type != 'ARMATURE':
            return
        cplus = getattr(armature, 'aether_cplus', None)
        aether_rig = getattr(armature, 'aether_rig', None)


        layout = self.layout
        col = layout.column(align=True)

        if armature.data.collections.get("FFXIV") is None:
            box = col.box()
            box_row = box.row()
            box_row.alignment = 'CENTER'
            box_row.label(text="Missing FFXIV Bone Collection", icon="ERROR")
        else:
            row = col.row(align=True)
            label_col = row.column(align=True)
            label_col.scale_x = 0.8
            label_col.label(text="C+ String")
            
            field_col = row.column(align=True)
            field_col.scale_x = 1.2
            field_col.prop(cplus, "code", text="", icon='COPYDOWN')

            if (bool(cplus.code)):
                col.separator()
                box = col.box()
                box_row = box.row()
                box_row.alignment = 'CENTER'
                if(cplus.applied):
                    box_row.label(text="C+ currently applied", icon="RECORD_ON")
                else:
                    box_row.label(text="C+ not applied", icon="PAUSE")

            col.separator()

            row = col.row(align=True)
            if aether_rig.rigified:
                row = col.row(align=True)
                row.operator("aether.clean_up_rig", text="Clean Up Rig", icon="BRUSH_DATA")
            else:
                ref_col = row.column(align=True)
                ref_col.scale_x = 2.0
                if cplus.backup_armature:
                    ref_col.operator("aether.create_backup_armature", text="Update Backup", icon="RECOVER_LAST")
                else:
                    ref_col.operator("aether.create_backup_armature", text="Create Backup", icon="DUPLICATE")
                
                arrow_col = row.column(align=True)
                arrow_col.scale_x = 0.3
                arrow_col.label(text="→")

                cplus_col = row.column(align=True)
                cplus_col.scale_x = 2.0

                cplus_col.enabled = bool(cplus.code) and bool(cplus.backup_armature)
                if cplus.applied:
                    cplus_col.operator("aether.revert_cplus_to_backup", text="Revert to Backup", icon="LOOP_BACK")
                else:
                    cplus_col.operator("aether.q_apply_cplus_string", text="Quick Apply", icon="CHECKBOX_HLT")

def register():
    bpy.utils.register_class(AETHER_PT_CustomizePlus)

def unregister():
    bpy.utils.unregister_class(AETHER_PT_CustomizePlus) 