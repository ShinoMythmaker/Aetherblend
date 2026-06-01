import bpy
from ...data.constants import sb_tail_collection, sb_ears_collection, sb_breast_collection
from ...data.constants import spring_bone_collection
from ...properties.tab_prop import get_active_tab
from ...utils.ui_visibility import visible_in_current_area

class AETHER_PT_SpringBones(bpy.types.Panel):
    bl_label = "Spring Bones"
    bl_idname = "AETHER_PT_spring_bones"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'  
    bl_category = 'AetherBlend'
    bl_order = 6 

    @classmethod
    def poll(cls, context):
        if not visible_in_current_area(context):
            return False
        if get_active_tab(context) != 'GENERATE':
            return False
        armature = context.active_object
        return armature is not None and armature.type == 'ARMATURE'
    
    def draw(self, context):
        armature = context.active_object
        layout = self.layout

        box = layout.box()
        header = box.row(align=True)

        spring_active = getattr(context.scene, "ab_sb_global_spring", False)
        spring_frame_active = getattr(context.scene, "ab_sb_global_spring_frame", False)

        spring_col = header.column(align=True)
        spring_col.enabled = not spring_frame_active
        spring_col.operator("aether.spring_bone", text="Interactive", icon='PLAY' if not spring_active else 'PAUSE')

        frame_col = header.column(align=True)
        frame_col.enabled = not spring_active
        frame_col.operator("aether.spring_bone_frame", text="Frame", icon='PLAY' if not spring_frame_active else 'PAUSE')

        if spring_frame_active:
            box.operator("aether.bake_all_spring_bones", text="Bake All", icon='LIGHT_SUN')

        sections = box.column(align=True)

        def has_spring_collection(collection_name):
            return armature.data.collections.get(f"{spring_bone_collection}/{collection_name}") is not None

        def draw_section(title, collection_name, generate_id, bake_id, delete_id):
            row = sections.row(align=True)
            row.label(text=title, icon='BONE_DATA')
            ops = row.row(align=True)

            if has_spring_collection(collection_name):
                if spring_frame_active:
                    ops.operator(bake_id, text="Bake", icon='LIGHT_SUN')
                ops.operator(delete_id, text="Delete", icon='TRASH')
            else:
                ops.operator(generate_id, text="Generate", icon='PIVOT_MEDIAN')

        draw_section("Tail", sb_tail_collection, "aether.generate_spring_tail", "aether.bake_spring_tail", "aether.delete_spring_tail")
        draw_section("Ears", sb_ears_collection, "aether.generate_spring_ears", "aether.bake_spring_ears", "aether.delete_spring_ears")
        draw_section("Breasts", sb_breast_collection, "aether.generate_spring_breasts", "aether.bake_spring_breasts", "aether.delete_spring_breasts")

        if context.mode == 'POSE' and context.active_pose_bone:
            active_bone = context.active_pose_bone

            layout.separator()
            box = layout.box()
            col = box.column(align=True)
            col.label(text=f"Active Bone: {active_bone.name}", icon='BONE_DATA')

            spring_col = col.column(align=True)
            spring_col.enabled = not active_bone.ab_sb_bone_collider
            spring_col.prop(active_bone, 'ab_sb_bone_spring', text="Spring")
            spring_col.prop(active_bone, 'ab_sb_bone_rot', text="Rotation")
            spring_col.prop(active_bone, 'ab_sb_stiffness', text="Bouncy")
            spring_col.prop(active_bone, 'ab_sb_damp', text="Speed")
            spring_col.prop(active_bone, 'ab_sb_gravity', text="Gravity")
            spring_col.prop(active_bone, 'ab_sb_global_influence', text="Influence")
            spring_col.prop(active_bone, 'ab_sb_collide', text="Is Colliding")
            spring_col.prop(active_bone, 'ab_sb_lock_axis', text="Lock Axis")

            collider_col = col.column(align=True)
            collider_col.enabled = not active_bone.ab_sb_bone_spring
            collider_col.prop(active_bone, 'ab_sb_bone_collider', text="Collider")
            collider_col.prop(active_bone, 'ab_sb_collider_dist', text="Collider Distance")
            collider_col.prop(active_bone, 'ab_sb_collider_force', text="Collider Force")

            col.separator()
            col.prop(context.scene, "ab_sb_show_colliders", text="Show Colliders")
            if context.scene.ab_sb_show_colliders:
                for pbone in armature.pose.bones:
                    if pbone.get("ab_sb_bone_collider"):
                        row = col.row(align=True)
                        row.label(text=pbone.name)
                        select = row.operator("aether.select_bone", text="Select")
                        select.bone_name = pbone.name


def register():
    bpy.utils.register_class(AETHER_PT_SpringBones)

def unregister():  
    bpy.utils.unregister_class(AETHER_PT_SpringBones)