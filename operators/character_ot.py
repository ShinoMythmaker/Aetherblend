import bpy
from .. import utils
from bpy.props import BoolProperty, StringProperty
from ..preferences import get_preferences

class AETHER_OT_Character_Import(bpy.types.Operator):
    """Import a character model into Blender with various options."""
    bl_idname = "aether.character_import"
    bl_label = "Import Character"
    bl_options = {'REGISTER', 'UNDO'}
    
    filepath: StringProperty(subtype="FILE_PATH")  # type: ignore
    filter_glob: StringProperty(default='*.gltf;*.glb;*.fbx', options={'HIDDEN'})  # type: ignore
    
    s_pack_images: BoolProperty(name="Pack-Images", description="Pack all Images into .blend file", default=True)  # type: ignore
    s_merge_vertices: BoolProperty(name="Merge Vertices", description="The glTF format requires discontinuous normals, UVs, and other vertex attributes to be stored as separate vertices, as required for rendering on typical graphics hardware. This option attempts to combine co -located vertices where possible. Currently cannot combine verts with different normals.", default=False)  # type: ignore
    s_import_collection: BoolProperty(name="Import-Collection", description="Stores all import in a seperatre Collection", default=True)  # type: ignore
    
    s_merge_skin: BoolProperty(name="Merge Skin", description="Merges all skin objects", default=True)  # type: ignore
    s_merge_by_material: BoolProperty(name="Merge by Material", description="Merges all objects with the same material", default=True)  # type: ignore
    
    s_import_with_shaders_setting: BoolProperty(name="Import with Meddle Shaders", description="Tries to also import all shaders from meddle shader cache", default=True)  # type: ignore
        
    s_disable_bone_shape: BoolProperty(name="Disable Bone Shapes", description="Disables the generation of Bone Shapes on Import", default=True)  # type: ignore
    s_apply_pose_track: BoolProperty(name="Apply Pose Track", description="Applies the pose track to the rest pose on Import", default=False)  # type: ignore

    s_temperence: BoolProperty(name="Temperence Mode", description="Imports with temperence mode enabled", default=False)  # type: ignore
    
    
    def invoke(self, context, event):
        prefs = get_preferences()
        if prefs.default_meddle_import_path:
            self.filepath = prefs.default_meddle_import_path
        context.window_manager.fileselect_add(self)

        return {'RUNNING_MODAL'}
    
    def draw(self, context):
        indent = 0.3
        indent_nested = 0.3
        layout = self.layout

        # Import Settings Title
        layout.label(text="Import Settings", icon="PREFERENCES")

        # Import Options Section
        box = layout.box()
        row = box.row()
        row.label(text="GLTF Import", icon="IMPORT")

        col = box.column(align=True)
    
        split = col.split(factor=indent)
        split.label(text=" ")
        split.prop(self, "s_pack_images")
        
        split = col.split(factor=indent)
        split.label(text=" ")
        split.prop(self, "s_merge_vertices")

        split = col.split(factor=indent)  
        split.label(text=" ")
        split.prop(self, "s_import_collection")
        
        # Mesh Options Section
        box = layout.box()
        row = box.row()
        row.label(text="Mesh Options", icon="MESH_DATA")

        col = box.column(align=True)
    
        split = col.split(factor=indent)
        split.label(text=" ")
        split.prop(self, "s_merge_skin")

        split = col.split(factor=indent)  
        split.label(text=" ")
        split.prop(self, "s_merge_by_material")

        # Shaders Section
        box = layout.box()
        row = box.row()
        row.label(text="Shaders", icon="SHADING_RENDERED")

        col = box.column(align=True)
        split = col.split(factor=indent)  
        split.label(text=" ")
        split.prop(self, "s_import_with_shaders_setting")

        # Armature Section
        box = layout.box()
        row = box.row()
        row.label(text="Armature", icon="ARMATURE_DATA")

        col = box.column(align=True)
        split = col.split(factor=indent)  
        split.label(text=" ")
        split.prop(self, "s_disable_bone_shape")

        split = col.split(factor=indent)  
        split.label(text=" ")
        split.prop(self, "s_apply_pose_track")

        split = col.split(factor=indent)  
        split.label(text=" ")
        split.prop(self, "s_temperence")
 
    def execute(self, context):  
        bpy.context.window.cursor_set('WAIT')   
        
        if not self.filepath or not (self.filepath.lower().endswith(".gltf") or self.filepath.lower().endswith(".glb") or self.filepath.lower().endswith(".fbx")): 
            self.report({'ERROR'}, "[AetherBlend] Invalid file format. Please select a .gltf, .glb, or .fbx file.")
            return {'CANCELLED'}   

        # Import the model
        imported_objects = utils.import_export.import_model(self.filepath, self.s_pack_images, self.s_disable_bone_shape, self.s_merge_vertices, self.s_temperence)

        # Process the imported objects with settings in mind
        if self.s_import_collection:
            import_collection = utils.collection.create_collection("Model_Import")
            import_collection.color_tag = "COLOR_05"
            utils.collection.link_to_collection(imported_objects, import_collection)
        
        if self.s_merge_by_material:
            imported_objects = utils.object.merge_by_material(imported_objects)
        
        if self.s_merge_skin:
            imported_objects = utils.object.merge_by_name(imported_objects, 'skin')
          
        if self.s_import_with_shaders_setting:
            try:
                utils.object.import_meddle_shader(self.filepath, imported_objects)
            except Exception as e:
                self.report({'ERROR'}, f"[AetherBlend] Failed to import Meddle shaders. Applying default shaders instead: {e}")

    
        bpy.ops.object.select_all(action='DESELECT')

        armature = utils.armature.find_armature_in_objects(imported_objects)
        if armature:
            if self.s_apply_pose_track:
                apply_pose_to_rest_pose(armature)

            clear_animation_data(armature)
            utils.armature.reset_transforms(armature)

            bpy.context.view_layer.objects.active = armature
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.armature.select_all(action='SELECT')
            bpy.ops.armature.assign_to_collection(new_collection_name="FFXIV")
            bpy.ops.object.mode_set(mode='OBJECT')
        
        self.report({'INFO'}, "[AetherBlend] Model imported and processed successfully.")
        
        if get_preferences().auto_navigate_tabs:
            bpy.context.scene.aether_tabs.active_tab = 'GENERATE'
        
        bpy.context.window.cursor_set('DEFAULT')
        return {'FINISHED'}
    
def apply_pose_to_rest_pose(armature: bpy.types.Object) -> None:
    """Apply a pose track to rest pose, similar to C+ quick apply process."""
    if not armature or armature.type != "ARMATURE":
        print(f"[AetherBlend] Invalid armature provided.")
        return
    
    if not armature.animation_data or not armature.animation_data.action:
        print(f"[AetherBlend] No animation data found on armature.")
        return
        
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.context.view_layer.objects.active = armature
    
    # parent_map = utils.armature.snapshot_parenting(armature)
    
    # utils.armature.unparent_all_bones(armature)
    
    # # Parent all bones to n_root if it exists
    # bpy.ops.object.mode_set(mode='EDIT')
    # edit_bones = armature.data.edit_bones
    # n_root = edit_bones.get('n_root')
    
    # if n_root:
    #     for bone in edit_bones:
    #         if bone != n_root and bone.parent is None:
    #             bone.parent = n_root
    #             bone.use_connect = False
    #     print(f"[AetherBlend] Parented all bones to n_root")
    
    bpy.ops.object.mode_set(mode='OBJECT')
    
    utils.armature.apply_all_as_shapekey(armature, shapekey_name=f"ImportedPose")
    
    utils.armature.new_rest_pose(armature)
    
    # utils.armature.restore_bone_parenting(armature, parent_map)
    
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = armature
    
    print(f"[AetherBlend] Applied pose to rest pose successfully.")

def remove_action(armature: bpy.types.Object, action_name: str) -> None:
    action = bpy.data.actions.get(action_name)
    if not action:
        print(f"[AetherBlend] Pose track '{action_name}' not found.")
        return
    
    try:
        bpy.data.actions.remove(action)
        print(f"[AetherBlend] Deleted pose track '{action_name}'")
    except Exception as e:
        print(f"[AetherBlend] Warning: Could not delete pose track '{action_name}': {e}")

def clear_animation_data(armature: bpy.types.Object) -> None:
    anim_data = armature.animation_data
    if not anim_data:
        print(f"[AetherBlend] Armature {armature.name} has no animation data.")
        return      
    
    try:
        armature.animation_data_clear()    
    except Exception as e:
        print(f"[AetherBlend] Warning: Could not clear '{armature.name}''s animation_data: {e}")


def register():
    bpy.utils.register_class(AETHER_OT_Character_Import)

def unregister():
    bpy.utils.unregister_class(AETHER_OT_Character_Import)

