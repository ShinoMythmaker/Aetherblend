import bpy
from .. import utils
from bpy.props import BoolProperty, StringProperty

class AETHER_OT_Character_Import(bpy.types.Operator):
    """Import a character model into Blender with various options."""
    bl_idname = "aether.character_import"
    bl_label = "Import Character"
    bl_options = {'REGISTER', 'UNDO'}
    
    filepath: StringProperty(subtype="FILE_PATH")  # type: ignore
    filter_glob: StringProperty(default='*.gltf;*.glb;*.fbx', options={'HIDDEN'})  # type: ignore
    
    s_pack_images: BoolProperty(name="Pack-Images", description="Pack all Images into .blend file", default=True)  # type: ignore
    s_merge_vertices: BoolProperty(name="Merge Vertices", description="The glTF format requires discontinuous normals, UVs, and other vertex attributes to be stored as separate vertices, as required for rendering on typical graphics hardware. This option attempts to combine co -located vertices where possible. Currently cannot combine verts with different normals.", default=False)  # type: ignore
    s_import_collection: BoolProperty(name="Import-Collection", description="Stores all import in a seperatre Collection", default=False)  # type: ignore
    
    s_merge_skin: BoolProperty(name="Merge Skin", description="Merges all skin objects", default=True)  # type: ignore
    s_merge_by_material: BoolProperty(name="Merge by Material", description="Merges all objects with the same material", default=True)  # type: ignore
    
    s_import_with_shaders_setting: BoolProperty(name="Import with Meddle Shaders", description="Tries to also import all shaders from meddle shader cache", default=True)  # type: ignore
        
    s_disable_bone_shape: BoolProperty(name="Disable Bone Shapes", description="Disables the generation of Bone Shapes on Import", default=True)  # type: ignore
    
    
    def invoke(self, context, event):
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
 
    def execute(self, context):  
        bpy.context.window.cursor_set('WAIT')   
        
        if not self.filepath or not (self.filepath.lower().endswith(".gltf") or self.filepath.lower().endswith(".glb") or self.filepath.lower().endswith(".fbx")): 
            self.report({'ERROR'}, "[AetherBlend] Invalid file format. Please select a .gltf, .glb, or .fbx file.")
            return {'CANCELLED'}   

        # Import the model
        imported_objects = utils.import_export.import_model(self.filepath, self.s_pack_images, self.s_disable_bone_shape, self.s_merge_vertices)

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
        
        self.report({'INFO'}, "[AetherBlend] Model imported and processed successfully.")
        bpy.context.window.cursor_set('DEFAULT')
        return {'FINISHED'}

def register():
    bpy.utils.register_class(AETHER_OT_Character_Import)

def unregister():
    bpy.utils.unregister_class(AETHER_OT_Character_Import)