import bpy
import requests
import json
import re
from bpy.types import Panel

# Timer for auto-refresh
_timer = None
# Timer for pose streaming
_pose_timer = None
# Cached enum items for stable dropdown display
_cached_character_items = [('NONE', 'None', 'No character assigned', 'CANCEL', 0)]
# Track previous character IDs for change detection
_previous_character_ids = []

def refresh_characters():
    """Timer function to refresh character list"""
    global _cached_character_items, _previous_character_ids
    
    scene = bpy.context.scene
    if scene.get("aether_ffxiv_connected", False):
        port = scene.aether_ffxiv_port
        try:
            url = f"http://localhost:{port}/characters"
            response = requests.get(url, timeout=1)
            
            if response.status_code == 200:
                characters = response.json()
                scene["aether_ffxiv_character_count"] = len(characters)
                
                # Update character list if changed
                new_ids = [str(char.get("objectId", 0)) for char in characters]
                
                if _previous_character_ids != new_ids:
                    # Save current assignments before updating
                    armature_assignments = {}
                    for obj in bpy.data.objects:
                        if obj.type == 'ARMATURE':
                            try:
                                current_val = obj.aether_ffxiv_character_id
                                if current_val:
                                    armature_assignments[obj.name] = current_val
                            except:
                                pass
                    
                    # Build new character list
                    scene.aether_ffxiv_selected_character_items.clear()
                    for char in characters:
                        item = scene.aether_ffxiv_selected_character_items.add()
                        item.object_id = str(char.get("objectId", 0))
                        item.char_name = char.get("name", "Unknown")
                    
                    # Build new cached enum items FIRST
                    new_items = [('NONE', 'None', 'No character assigned', 'CANCEL', 0)]
                    for i, char in enumerate(scene.aether_ffxiv_selected_character_items):
                        new_items.append((char.object_id, char.char_name, f"ObjectID: {char.object_id}", 'ARMATURE_DATA', i + 1))
                    
                    # Update cache BEFORE restoring assignments
                    _cached_character_items = new_items
                    _previous_character_ids = new_ids
                    
                    # Small delay to ensure enum cache is updated
                    import time
                    time.sleep(0.05)
                    
                    # Now restore assignments (only for characters that still exist)
                    valid_ids = set(new_ids)
                    for obj_name, char_id in armature_assignments.items():
                        if char_id in valid_ids:
                            obj = bpy.data.objects.get(obj_name)
                            if obj and obj.type == 'ARMATURE':
                                try:
                                    obj.aether_ffxiv_character_id = char_id
                                except:
                                    pass
                        else:
                            obj = bpy.data.objects.get(obj_name)
                            if obj:
                                obj.aether_ffxiv_character_id = ""
                
        except:
            pass  # Silently fail, connection might be temporarily down
    
    # Force UI redraw to show updates
    for window in bpy.context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == 'VIEW_3D':
                area.tag_redraw()
    
    return 2.0  # Refresh every 2 seconds


def stream_pose():
    """Timer function to stream pose data"""
    scene = bpy.context.scene
    
    # Check if streaming is still enabled
    if not scene.get("aether_ffxiv_connected", False) or not scene.aether_ffxiv_stream_enabled:
        return None  # Stop timer
    
    # Find armature with streaming enabled
    for obj in bpy.data.objects:
        if obj.type == 'ARMATURE' and obj.aether_ffxiv_character_id and obj == bpy.context.active_object:
            armature = obj
            character_id = armature.aether_ffxiv_character_id
            
            # Find root bone
            root_bone = armature.pose.bones.get("n_throw")
            if not root_bone:
                continue
            
            # Build pose data
            root_matrix_world = armature.matrix_world @ root_bone.matrix
            pose_data = {
                "FileExtension": ".pose",
                "TypeName": "Aetherblend Pose",
                "FileVersion": 2,
                "Bones": {}
            }
            
            # Get bones from FFXIV collection
            ffxiv_col = armature.data.collections.get('FFXIV')
            if not ffxiv_col:
                continue
            
            selected_bones = [bone.name for bone in ffxiv_col.bones]
            for bone_name in selected_bones:
                clean_bone_name = re.sub(r"\.\d+$", "", bone_name)
                bone = armature.pose.bones.get(bone_name)
                if bone:
                    bone_matrix_world = armature.matrix_world @ bone.matrix
                    relative_matrix = root_matrix_world.inverted() @ bone_matrix_world
                    
                    pose_data["Bones"][clean_bone_name] = {
                        "Position": f"{relative_matrix.translation.x:.6f}, {relative_matrix.translation.y:.6f}, {relative_matrix.translation.z:.6f}",
                        "Rotation": f"{relative_matrix.to_quaternion().x:.6f}, {relative_matrix.to_quaternion().y:.6f}, {relative_matrix.to_quaternion().z:.6f}, {relative_matrix.to_quaternion().w:.6f}",
                        "Scale": f"{relative_matrix.to_scale().x:.8f}, {relative_matrix.to_scale().y:.8f}, {relative_matrix.to_scale().z:.8f}"
                    }
            
            # Send to server
            port = scene.aether_ffxiv_port
            try:
                url = f"http://localhost:{port}/character/{character_id}/pose"
                headers = {'Content-Type': 'application/json'}
                requests.post(url, json=pose_data, headers=headers, timeout=0.5)
            except:
                pass  # Silently fail during streaming
            
            break
    
    # Return interval based on FPS setting
    fps = scene.aether_ffxiv_stream_fps
    return 1.0 / fps if fps > 0 else 0.1


class AETHER_MT_CharacterSelect(bpy.types.Menu):
    bl_label = "Select FFXIV Character"
    bl_idname = "AETHER_MT_character_select"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        obj = context.active_object
        
        # None option
        op = layout.operator("aether.assign_character", text="None", icon='CANCEL')
        op.character_id = ""
        op.character_name = "None"
        
        layout.separator()
        
        # Character options
        for char in scene.aether_ffxiv_selected_character_items:
            op = layout.operator("aether.assign_character", text=char.char_name, icon='ARMATURE_DATA')
            op.character_id = char.object_id
            op.character_name = char.char_name


class AETHER_OT_AssignCharacter(bpy.types.Operator):
    bl_idname = "aether.assign_character"
    bl_label = "Assign Character"
    bl_description = "Assign FFXIV character to this armature"
    bl_options = {'REGISTER', 'UNDO'}
    
    character_id: bpy.props.StringProperty()  # type: ignore
    character_name: bpy.props.StringProperty()  # type: ignore
    
    def execute(self, context):
        if context.active_object and context.active_object.type == 'ARMATURE':
            context.active_object.aether_ffxiv_character_id = self.character_id
            if self.character_id:
                self.report({'INFO'}, f"Assigned {self.character_name} to {context.active_object.name}")
            else:
                self.report({'INFO'}, f"Cleared character assignment for {context.active_object.name}")
            return {'FINISHED'}
        return {'CANCELLED'}


class AETHER_PT_FFXIVBridgePanel(Panel):
    bl_label = "FFXIV Bridge"
    bl_idname = "AETHER_PT_ffxiv_bridge"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AetherBlend'
    bl_order = 5

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        # Port input
        box = layout.box()
        box.label(text="Connection Settings", icon='NETWORK_DRIVE')
        row = box.row()
        row.prop(scene, "aether_ffxiv_port", text="Port")
        
        # Connect button
        row = box.row()
        if scene.get("aether_ffxiv_connected", False):
            row.operator("aether.ffxiv_disconnect", text="Disconnect", icon='CANCEL')
        else:
            row.operator("aether.ffxiv_connect", text="Connect", icon='PLUGIN')
        
        # Character selection (only show when connected)
        if scene.get("aether_ffxiv_connected", False):
            box = layout.box()
            box.label(text="Character Assignment", icon='ARMATURE_DATA')
            
            # Show active armature
            if context.active_object and context.active_object.type == 'ARMATURE':
                row = box.row()
                row.label(text=f"Armature: {context.active_object.name}", icon='ARMATURE_DATA')
                
                character_count = scene.get("aether_ffxiv_character_count", 0)
                if character_count > 0:
                    row = box.row()
                    # Show currently assigned character
                    current_id = context.active_object.aether_ffxiv_character_id
                    if current_id:
                        # Find character name
                        char_name = "Unknown"
                        for char in scene.aether_ffxiv_selected_character_items:
                            if char.object_id == current_id:
                                char_name = char.char_name
                                break
                        row.label(text=f"Assigned: {char_name}", icon='ARMATURE_DATA')
                    else:
                        row.label(text="Assigned: None", icon='CANCEL')
                    
                    # Character selection menu
                    row = box.row()
                    row.menu("AETHER_MT_character_select", text="Select Character")
                    
                    # Send pose button and streaming toggle (only show if character is assigned)
                    if context.active_object.aether_ffxiv_character_id:
                        row = box.row()
                        row.operator("aether.ffxiv_send_pose", text="Send Pose", icon='EXPORT')
                        
                        row = box.row()
                        row.prop(scene, "aether_ffxiv_stream_enabled", text="Stream Pose", toggle=True)
                        
                        if scene.aether_ffxiv_stream_enabled:
                            row = box.row()
                            row.prop(scene, "aether_ffxiv_stream_fps", text="FPS")
                else:
                    box.label(text="No characters found", icon='INFO')
            else:
                box.label(text="Select an armature to assign", icon='INFO')


class AETHER_OT_FFXIVConnect(bpy.types.Operator):
    bl_idname = "aether.ffxiv_connect"
    bl_label = "Connect to FFXIV"
    bl_description = "Connect to FFXIV HTTP server and fetch available characters"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        global _timer
        scene = context.scene
        port = scene.aether_ffxiv_port
        
        try:
            # Try to connect and fetch characters
            url = f"http://localhost:{port}/characters"
            response = requests.get(url, timeout=2)
            
            if response.status_code == 200:
                global _cached_character_items, _previous_character_ids
                characters = response.json()
                
                # Store characters in scene
                scene["aether_ffxiv_connected"] = True
                scene["aether_ffxiv_character_count"] = len(characters)
                
                # Clear existing items
                scene.aether_ffxiv_selected_character_items.clear()
                
                # Populate character dropdown
                for char in characters:
                    item = scene.aether_ffxiv_selected_character_items.add()
                    item.object_id = str(char.get("objectId", 0))
                    item.char_name = char.get("name", "Unknown")
                
                # Build cached enum items
                new_items = [('NONE', 'None', 'No character assigned', 'CANCEL', 0)]
                for i, char in enumerate(scene.aether_ffxiv_selected_character_items):
                    new_items.append((char.object_id, char.char_name, f"ObjectID: {char.object_id}", 'ARMATURE_DATA', i + 1))
                _cached_character_items = new_items
                _previous_character_ids = [char.object_id for char in scene.aether_ffxiv_selected_character_items]
                
                # Start auto-refresh timer
                if _timer is None:
                    _timer = bpy.app.timers.register(refresh_characters)
                
                # Force UI redraw
                for window in bpy.context.window_manager.windows:
                    for area in window.screen.areas:
                        if area.type == 'VIEW_3D':
                            area.tag_redraw()
                
                self.report({'INFO'}, f"Connected! Found {len(characters)} character(s)")
                return {'FINISHED'}
            else:
                self.report({'ERROR'}, f"Server returned status code: {response.status_code}")
                return {'CANCELLED'}
                
        except requests.exceptions.ConnectionError:
            self.report({'ERROR'}, f"Could not connect to localhost:{port}. Is FFXIV server running?")
            return {'CANCELLED'}
        except requests.exceptions.Timeout:
            self.report({'ERROR'}, f"Connection timeout to localhost:{port}")
            return {'CANCELLED'}
        except Exception as e:
            self.report({'ERROR'}, f"Error connecting: {str(e)}")
            return {'CANCELLED'}


class AETHER_OT_FFXIVDisconnect(bpy.types.Operator):
    bl_idname = "aether.ffxiv_disconnect"
    bl_label = "Disconnect from FFXIV"
    bl_description = "Disconnect from FFXIV HTTP server"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        global _timer, _pose_timer
        scene = context.scene
        scene["aether_ffxiv_connected"] = False
        scene["aether_ffxiv_character_count"] = 0
        scene.aether_ffxiv_selected_character_items.clear()
        scene.aether_ffxiv_stream_enabled = False
        
        # Stop auto-refresh timer
        if _timer is not None:
            bpy.app.timers.unregister(_timer)
            _timer = None
        
        # Stop pose streaming timer
        if _pose_timer is not None:
            bpy.app.timers.unregister(_pose_timer)
            _pose_timer = None
        
        self.report({'INFO'}, "Disconnected from FFXIV server")
        return {'FINISHED'}


class AETHER_OT_FFXIVSendPose(bpy.types.Operator):
    bl_idname = "aether.ffxiv_send_pose"
    bl_label = "Send Pose to FFXIV"
    bl_description = "Send current armature pose to assigned FFXIV character"
    bl_options = {'REGISTER'}

    def execute(self, context):
        scene = context.scene
        armature = context.active_object
        
        # Validate connection
        if not scene.get("aether_ffxiv_connected", False):
            self.report({'ERROR'}, "Not connected to FFXIV server")
            return {'CANCELLED'}
        
        # Validate armature
        if not armature or armature.type != 'ARMATURE':
            self.report({'ERROR'}, "No armature selected")
            return {'CANCELLED'}
        
        # Check if character is assigned
        character_id = armature.aether_ffxiv_character_id
        if not character_id:
            self.report({'ERROR'}, "No FFXIV character assigned to this armature")
            return {'CANCELLED'}
        
        # Find root bone
        root_bone = armature.pose.bones.get("n_throw")
        if not root_bone:
            self.report({'ERROR'}, "Origin bone 'n_throw' not found")
            return {'CANCELLED'}
        
        # Build pose data using same format as pose_export_ot.py
        root_matrix_world = armature.matrix_world @ root_bone.matrix
        pose_data = {
            "FileExtension": ".pose",
            "TypeName": "Aetherblend Pose",
            "FileVersion": 2,
            "Bones": {}
        }
        
        # Get bones from FFXIV collection
        ffxiv_col = armature.data.collections.get('FFXIV')
        if not ffxiv_col:
            self.report({'ERROR'}, "FFXIV bone collection not found")
            return {'CANCELLED'}
        
        # Process each bone - use relative transforms like pose_export_ot
        selected_bones = [bone.name for bone in ffxiv_col.bones]
        for bone_name in selected_bones:
            clean_bone_name = re.sub(r"\.\d+$", "", bone_name)
            bone = armature.pose.bones.get(bone_name)
            if bone:
                bone_matrix_world = armature.matrix_world @ bone.matrix
                relative_matrix = root_matrix_world.inverted() @ bone_matrix_world
                
                pose_data["Bones"][clean_bone_name] = {
                    "Position": f"{relative_matrix.translation.x:.6f}, {relative_matrix.translation.y:.6f}, {relative_matrix.translation.z:.6f}",
                    "Rotation": f"{relative_matrix.to_quaternion().x:.6f}, {relative_matrix.to_quaternion().y:.6f}, {relative_matrix.to_quaternion().z:.6f}, {relative_matrix.to_quaternion().w:.6f}",
                    "Scale": f"{relative_matrix.to_scale().x:.8f}, {relative_matrix.to_scale().y:.8f}, {relative_matrix.to_scale().z:.8f}"
                }
        
        # Send to server
        port = scene.aether_ffxiv_port
        try:
            url = f"http://localhost:{port}/character/{character_id}/pose"
            headers = {'Content-Type': 'application/json'}
            
            print(f"\n=== SENDING POSE TO FFXIV ===")
            print(f"URL: {url}")
            print(f"Bone count: {len(pose_data['Bones'])}")
            print(f"First 200 chars of JSON: {json.dumps(pose_data)[:200]}")
            
            response = requests.post(url, json=pose_data, headers=headers, timeout=2)
            
            print(f"Response status: {response.status_code}")
            print(f"Response body: {response.text}")
            print(f"=============================\n")
            
            if response.status_code == 200:
                self.report({'INFO'}, f"Pose sent successfully to character {character_id}")
                return {'FINISHED'}
            else:
                self.report({'ERROR'}, f"Server returned status code: {response.status_code} - {response.text}")
                return {'CANCELLED'}
                
        except requests.exceptions.ConnectionError:
            self.report({'ERROR'}, f"Could not connect to localhost:{port}")
            return {'CANCELLED'}
        except requests.exceptions.Timeout:
            self.report({'ERROR'}, f"Connection timeout")
            return {'CANCELLED'}
        except Exception as e:
            self.report({'ERROR'}, f"Error sending pose: {str(e)}")
            return {'CANCELLED'}


# Property group for character items
class AETHER_PG_FFXIVCharacter(bpy.types.PropertyGroup):
    object_id: bpy.props.StringProperty(name="Object ID")  # type: ignore
    char_name: bpy.props.StringProperty(name="Character Name")  # type: ignore


def get_character_items(self, context):
    """Dynamic enum items for character selection"""
    global _cached_character_items
    # Return cached items for stable dropdown display
    return _cached_character_items


def on_stream_enabled_update(self, context):
    """Called when stream enabled checkbox changes"""
    global _pose_timer
    
    if context.scene.aether_ffxiv_stream_enabled:
        # Start streaming timer
        if _pose_timer is None:
            _pose_timer = bpy.app.timers.register(stream_pose)
    else:
        # Stop streaming timer
        if _pose_timer is not None:
            bpy.app.timers.unregister(_pose_timer)
            _pose_timer = None


def register():
    bpy.utils.register_class(AETHER_PG_FFXIVCharacter)
    bpy.utils.register_class(AETHER_OT_AssignCharacter)
    bpy.utils.register_class(AETHER_MT_CharacterSelect)
    bpy.utils.register_class(AETHER_OT_FFXIVConnect)
    bpy.utils.register_class(AETHER_OT_FFXIVDisconnect)
    bpy.utils.register_class(AETHER_OT_FFXIVSendPose)
    bpy.utils.register_class(AETHER_PT_FFXIVBridgePanel)
    
    # Register properties
    bpy.types.Scene.aether_ffxiv_port = bpy.props.IntProperty(
        name="Port",
        description="HTTP server port for FFXIV connection",
        default=8080,
        min=1,
        max=65535
    )
    
    bpy.types.Scene.aether_ffxiv_stream_enabled = bpy.props.BoolProperty(
        name="Stream Pose",
        description="Continuously stream pose data to FFXIV character",
        default=False,
        update=on_stream_enabled_update
    )
    
    bpy.types.Scene.aether_ffxiv_stream_fps = bpy.props.IntProperty(
        name="Stream FPS",
        description="Frames per second for pose streaming",
        default=10,
        min=1,
        max=60
    )
    
    bpy.types.Scene.aether_ffxiv_selected_character_items = bpy.props.CollectionProperty(
        type=AETHER_PG_FFXIVCharacter
    )
    
    # Store character on armature objects (using StringProperty to avoid enum validation issues)
    bpy.types.Object.aether_ffxiv_character_id = bpy.props.StringProperty(
        name="FFXIV Character ID",
        description="Assigned FFXIV character objectId",
        default=""
    )


def unregister():
    global _timer, _pose_timer
    
    # Stop timers if running
    if _timer is not None:
        bpy.app.timers.unregister(_timer)
        _timer = None
    
    if _pose_timer is not None:
        bpy.app.timers.unregister(_pose_timer)
        _pose_timer = None
    
    bpy.utils.unregister_class(AETHER_PT_FFXIVBridgePanel)
    bpy.utils.unregister_class(AETHER_OT_FFXIVSendPose)
    bpy.utils.unregister_class(AETHER_OT_FFXIVDisconnect)
    bpy.utils.unregister_class(AETHER_OT_FFXIVConnect)
    bpy.utils.unregister_class(AETHER_MT_CharacterSelect)
    bpy.utils.unregister_class(AETHER_OT_AssignCharacter)
    bpy.utils.unregister_class(AETHER_PG_FFXIVCharacter)
    
    # Unregister properties
    del bpy.types.Scene.aether_ffxiv_port
    del bpy.types.Scene.aether_ffxiv_stream_enabled
    del bpy.types.Scene.aether_ffxiv_stream_fps
    del bpy.types.Scene.aether_ffxiv_selected_character_items
    del bpy.types.Object.aether_ffxiv_character_id
