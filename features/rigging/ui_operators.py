import bpy
import base64
import binascii
import json

from . import template_manager
from .templates import get_modules_by_family


MODULE_TYPE_ICONS = {
    "Generation": 'GROUP_BONE',
    "UI-Addon": 'OUTLINER_COLLECTION',
    "Patch": 'MODIFIER',
}
MODULE_TYPE_ORDER = {
    "Generation": 0,
    "UI-Addon": 1,
    "Patch": 2,
}
_DYNAMIC_ADD_MENU_CLASSES = []
_TEMPLATE_CLIPBOARD_PREFIX = "AetherBlendTemplateV1"


def _encode_template_clipboard_payload(payload: dict) -> str:
    """Encode template payload as a compact, versioned Base64 token."""
    json_payload = json.dumps(payload, separators=(",", ":"), ensure_ascii=False)
    encoded = base64.urlsafe_b64encode(json_payload.encode("utf-8")).decode("ascii")
    return f"{_TEMPLATE_CLIPBOARD_PREFIX}{encoded}"


def _decode_template_clipboard_payload(clipboard_text: str) -> dict:
    """Decode a versioned Base64 token; fallback to legacy raw JSON clipboard content."""
    text = (clipboard_text or "").strip()
    if not text:
        raise ValueError("Clipboard is empty")

    if text.startswith(_TEMPLATE_CLIPBOARD_PREFIX):
        token = text[len(_TEMPLATE_CLIPBOARD_PREFIX):].strip()
        try:
            decoded = base64.urlsafe_b64decode(token.encode("ascii")).decode("utf-8")
            payload = json.loads(decoded)
        except (ValueError, binascii.Error, UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Clipboard template token is invalid") from exc
    else:
        # Support old JSON clipboard exports so users can still paste existing shares.
        try:
            payload = json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Clipboard content is not a valid template token") from exc

    if not isinstance(payload, dict):
        raise ValueError("Clipboard template payload must be a JSON object")

    return payload

def _format_family_name(family_name: str) -> str:
    """Convert a module family key into a UI-friendly label."""
    return (family_name or '').replace('_', ' ').title() or "Misc"

def _get_family_menu_idname(mode: str, family_name: str) -> str:
    """Build a stable menu idname for a family submenu."""
    family_slug = family_name.replace('.', '_').replace('-', '_')
    return f"AETHER_MT_add_{mode.lower()}_{family_slug}_module_menu"

def _draw_family_module_menu(layout, mode: str, family_name: str) -> None:
    """Draw the module entries for a single family, grouped by module type."""
    modules_by_type: dict[str, list[tuple[str, object]]] = {}

    for key, module in get_modules_by_family(family_name).items():
        module_type = getattr(module, 'type', None) or "Other"
        modules_by_type.setdefault(module_type, []).append((key, module))

    for index, (module_type, entries) in enumerate(
        sorted(
            modules_by_type.items(),
            key=lambda item: (MODULE_TYPE_ORDER.get(item[0], 99), item[0]),
        )
    ):
        if index > 0:
            layout.separator()

        layout.label(text=module_type, icon=MODULE_TYPE_ICONS.get(module_type, 'DOT'))
        column = layout.column(align=True)

        for key, module in entries:
            operator = column.operator(
                "aether.add_template_module",
                text=module.name,
                icon='NONE',
            )
            operator.mode = mode
            operator.module_key = key


def _build_family_menu_class(mode: str, family_name: str):
    """Create a dedicated submenu class for one module family."""
    menu_idname = _get_family_menu_idname(mode, family_name)
    class_name = ''.join(part.capitalize() for part in f"{mode}_{family_name}".replace('.', '_').split('_'))

    def draw(self, context):
        _draw_family_module_menu(self.layout, mode, family_name)

    return type(
        f"AETHER_MT_{class_name}_Module_Menu",
        (bpy.types.Menu,),
        {
            "bl_idname": menu_idname,
            "bl_label": _format_family_name(family_name),
            "draw": draw,
        },
    )


def _get_group_bounds(modules, index: int) -> tuple[int, int]:
    """Return the contiguous bounds for the selected fallback group."""
    if index < 0 or index >= len(modules):
        return index, index

    group_index = getattr(modules[index], 'group_index', -1)
    if group_index < 0:
        return index, index + 1

    start = index
    while start > 0 and getattr(modules[start - 1], 'group_index', -1) == group_index:
        start -= 1

    end = index + 1
    while end < len(modules) and getattr(modules[end], 'group_index', -1) == group_index:
        end += 1

    return start, end


def _reindex_module_groups(aether_rig) -> None:
    """Normalize stored group indices so they match the current UI list order."""
    next_group_index = 0
    previous_group_index = None

    for item in aether_rig.modules:
        group_index = getattr(item, 'group_index', -1)
        starts_new_group = (
            previous_group_index is None
            or group_index < 0
            or previous_group_index < 0
            or group_index != previous_group_index
        )

        if starts_new_group:
            item.group_index = next_group_index
            next_group_index += 1
        else:
            item.group_index = next_group_index - 1

        previous_group_index = group_index


def _get_next_group_index(modules) -> int:
    """Return a temporary group index that will not collide with existing groups."""
    return max((getattr(item, 'group_index', -1) for item in modules), default=-1) + 1


def _insert_module_item(aether_rig, module_key: str, insert_index: int, group_index: int) -> int:
    """Insert a module entry at the requested UI position."""
    modules = aether_rig.modules
    item = modules.add()
    item.module_key = module_key
    item.group_index = group_index

    new_index = len(modules) - 1
    insert_index = max(0, min(insert_index, new_index))
    if insert_index != new_index:
        modules.move(new_index, insert_index)

    return insert_index


class AETHER_MT_Add_Group_Module_Menu(bpy.types.Menu):
    bl_idname = "AETHER_MT_add_group_module_menu"
    bl_label = "Add Group"

    def draw(self, context):
        column = self.layout.column(align=True)
        for family_name in get_modules_by_family().keys():
            column.menu(
                _get_family_menu_idname('GROUP', family_name),
                text=_format_family_name(family_name),
                icon='FILE_FOLDER',
            )


class AETHER_MT_Add_Fallback_Module_Menu(bpy.types.Menu):
    bl_idname = "AETHER_MT_add_fallback_module_menu"
    bl_label = "Add Fallback"

    def draw(self, context):
        column = self.layout.column(align=True)
        for family_name in get_modules_by_family().keys():
            column.menu(
                _get_family_menu_idname('FALLBACK', family_name),
                text=_format_family_name(family_name),
                icon='FILE_FOLDER',
            )


class AETHER_MT_Populate_Custom_Template_Menu(bpy.types.Menu):
    bl_idname = "AETHER_MT_populate_custom_template_menu"
    bl_label = "Populate Custom Modules"

    def draw(self, context):
        column = self.layout.column(align=True)
        for template_name in template_manager.get_available_template_names():
            operator = column.operator(
                "aether.populate_custom_template",
                text=template_name,
                icon='PRESET',
            )
            operator.template_name = template_name


class AETHER_OT_Add_Template_Module(bpy.types.Operator):
    bl_idname = "aether.add_template_module"
    bl_label = "Add Template Module"
    bl_description = "Insert a module as a new group or fallback entry"
    bl_options = {'UNDO'}

    mode: bpy.props.EnumProperty(
        name="Insert Mode",
        items=[
            ('GROUP', "Group", "Insert a new standalone priority group after the selected group"),
            ('FALLBACK', "Fallback", "Add a fallback module to the selected group"),
        ],
        options={'HIDDEN'},
    ) # type: ignore

    module_key: bpy.props.StringProperty(
        name="Module Key",
        description="Registered rig module to add",
        options={'HIDDEN'},
    ) # type: ignore

    def execute(self, context):
        armature = context.active_object
        if not armature or armature.type != 'ARMATURE':
            self.report({'ERROR'}, "Select an armature")
            return {'CANCELLED'}

        aether_rig = getattr(armature, 'aether_rig', None)
        if not aether_rig:
            self.report({'ERROR'}, "Armature has no Aether rig settings")
            return {'CANCELLED'}

        if self.module_key not in template_manager.AVAILABLE_MODULES:
            self.report({'WARNING'}, "Choose a valid module to add")
            return {'CANCELLED'}

        modules = aether_rig.modules
        selected_index = aether_rig.module_index
        has_selection = 0 <= selected_index < len(modules)

        if self.mode == 'FALLBACK' and not has_selection:
            self.report({'WARNING'}, "Select a module group first")
            return {'CANCELLED'}

        if not has_selection:
            insert_index = len(modules)
            group_index = _get_next_group_index(modules)
        else:
            start, end = _get_group_bounds(modules, selected_index)
            insert_index = end
            if self.mode == 'FALLBACK':
                group_index = getattr(modules[start], 'group_index', -1)
            else:
                group_index = _get_next_group_index(modules)

        inserted_index = _insert_module_item(aether_rig, self.module_key, insert_index, group_index)
        _reindex_module_groups(aether_rig)
        aether_rig.custom_modules_initialized = True
        aether_rig.module_index = inserted_index
        return {'FINISHED'}


class AETHER_OT_Populate_Custom_Template(bpy.types.Operator):
    bl_idname = "aether.populate_custom_template"
    bl_label = "Populate Custom Template"
    bl_description = "Copy modules from a built-in template into the editable custom list"
    bl_options = {'UNDO'}

    template_name: bpy.props.StringProperty(
        name="Template",
        description="Built-in template used to populate the custom module list",
        options={'HIDDEN'},
    ) # type: ignore

    def execute(self, context):
        armature = context.active_object
        if not armature or armature.type != 'ARMATURE':
            self.report({'ERROR'}, "Select an armature")
            return {'CANCELLED'}

        aether_rig = getattr(armature, 'aether_rig', None)
        if not aether_rig:
            self.report({'ERROR'}, "Armature has no Aether rig settings")
            return {'CANCELLED'}

        if self.template_name not in template_manager.get_available_template_names():
            self.report({'WARNING'}, "Choose a valid template to populate from")
            return {'CANCELLED'}

        aether_rig.selected_template = template_manager.CUSTOM_TEMPLATE_NAME
        template_manager.populate_modules_from_template(aether_rig, self.template_name)
        aether_rig.module_index = 0 if aether_rig.modules else 0
        return {'FINISHED'}


class AETHER_OT_Save_Custom_Template_JSON(bpy.types.Operator):
    bl_idname = "aether.save_custom_template_json"
    bl_label = "Save Custom Template"
    bl_description = "Save the current custom module layout as a JSON template"
    bl_options = {'UNDO'}

    def execute(self, context):
        armature = context.active_object
        if not armature or armature.type != 'ARMATURE':
            self.report({'ERROR'}, "Select an armature")
            return {'CANCELLED'}

        aether_rig = getattr(armature, 'aether_rig', None)
        if not aether_rig:
            self.report({'ERROR'}, "Armature has no Aether rig settings")
            return {'CANCELLED'}

        if len(aether_rig.modules) == 0:
            self.report({'WARNING'}, "Custom template has no modules to save")
            return {'CANCELLED'}

        template_name = (getattr(aether_rig, 'custom_template_name', '') or '').strip()
        if not template_name:
            self.report({'WARNING'}, "Enter a template name before saving")
            return {'CANCELLED'}

        grouped_modules = template_manager.resolve_module_groups(aether_rig)
        module_keys: list[list[str]] = []
        for group in grouped_modules:
            key_group: list[str] = []
            for module in group:
                module_key = template_manager.get_module_key(module)
                if module_key:
                    key_group.append(module_key)
            if key_group:
                module_keys.append(key_group)

        if not module_keys:
            self.report({'WARNING'}, "Could not resolve modules for saving")
            return {'CANCELLED'}

        file_path = template_manager.save_custom_template_json(template_name, module_keys)
        aether_rig.selected_template = template_manager.CUSTOM_TEMPLATE_NAME
        self.report({'INFO'}, f"Saved template JSON: {file_path.name}")
        return {'FINISHED'}


class AETHER_OT_Export_Custom_Template_Clipboard(bpy.types.Operator):
    bl_idname = "aether.export_custom_template_clipboard"
    bl_label = "Export Custom Template to Clipboard"
    bl_description = "Copy the current custom module layout as a Base64 token to the system clipboard"
    bl_options = {'UNDO'}

    def execute(self, context):
        armature = context.active_object
        if not armature or armature.type != 'ARMATURE':
            self.report({'ERROR'}, "Select an armature")
            return {'CANCELLED'}

        aether_rig = getattr(armature, 'aether_rig', None)
        if not aether_rig:
            self.report({'ERROR'}, "Armature has no Aether rig settings")
            return {'CANCELLED'}

        grouped_modules = template_manager.resolve_module_groups(aether_rig)
        module_keys: list[list[str]] = []
        for group in grouped_modules:
            key_group: list[str] = []
            for module in group:
                module_key = template_manager.get_module_key(module)
                if module_key:
                    key_group.append(module_key)
            if key_group:
                module_keys.append(key_group)

        if not module_keys:
            self.report({'WARNING'}, "Custom template has no modules to export")
            return {'CANCELLED'}

        template_name = (getattr(aether_rig, 'custom_template_name', '') or '').strip() or "Custom Template"
        payload = {
            "name": template_name,
            "module_keys": module_keys,
        }
        context.window_manager.clipboard = _encode_template_clipboard_payload(payload)
        self.report({'INFO'}, "Copied custom template token to clipboard")
        return {'FINISHED'}


class AETHER_OT_Import_Custom_Template_Clipboard(bpy.types.Operator):
    bl_idname = "aether.import_custom_template_clipboard"
    bl_label = "Import Custom Template from Clipboard"
    bl_description = "Paste a Base64 template token from clipboard and load it into the editable custom module list"
    bl_options = {'UNDO'}

    def execute(self, context):
        armature = context.active_object
        if not armature or armature.type != 'ARMATURE':
            self.report({'ERROR'}, "Select an armature")
            return {'CANCELLED'}

        aether_rig = getattr(armature, 'aether_rig', None)
        if not aether_rig:
            self.report({'ERROR'}, "Armature has no Aether rig settings")
            return {'CANCELLED'}

        try:
            payload = _decode_template_clipboard_payload(context.window_manager.clipboard)
        except ValueError as exc:
            self.report({'WARNING'}, str(exc))
            return {'CANCELLED'}

        module_keys = payload.get("module_keys") or payload.get("modules")
        if not isinstance(module_keys, list):
            self.report({'WARNING'}, "Template payload must contain a module_keys list")
            return {'CANCELLED'}

        parsed_groups: list[list[str]] = []
        for key_group in module_keys:
            if not isinstance(key_group, list):
                continue

            valid_keys: list[str] = []
            for module_key in key_group:
                if isinstance(module_key, str) and module_key in template_manager.AVAILABLE_MODULES:
                    valid_keys.append(module_key)

            if valid_keys:
                parsed_groups.append(valid_keys)

        if not parsed_groups:
            self.report({'WARNING'}, "No valid module keys found in template payload")
            return {'CANCELLED'}

        aether_rig.selected_template = template_manager.CUSTOM_TEMPLATE_NAME
        aether_rig.modules.clear()

        for group_index, key_group in enumerate(parsed_groups):
            for module_key in key_group:
                item = aether_rig.modules.add()
                item.module_key = module_key
                item.group_index = group_index

        template_name = payload.get("name")
        if isinstance(template_name, str) and template_name.strip():
            aether_rig.custom_template_name = template_name.strip()

        aether_rig.custom_modules_initialized = True
        aether_rig.module_index = 0 if aether_rig.modules else 0
        self.report({'INFO'}, "Imported custom template from clipboard token")
        return {'FINISHED'}


class AETHER_OT_Move_Template_Module(bpy.types.Operator):
    bl_idname = "aether.move_template_module"
    bl_label = "Move Template Module"
    bl_description = "Move the selected group up/down, or reorder a child module within its fallback group"
    bl_options = {'UNDO'}

    direction: bpy.props.EnumProperty(
        name="Direction",
        items=[
            ('UP', "Up", "Move the selected entry upward"),
            ('DOWN', "Down", "Move the selected entry downward"),
        ],
        options={'HIDDEN'},
    ) # type: ignore

    def execute(self, context):
        armature = context.active_object
        if not armature or armature.type != 'ARMATURE':
            self.report({'ERROR'}, "Select an armature")
            return {'CANCELLED'}

        aether_rig = getattr(armature, 'aether_rig', None)
        if not aether_rig:
            self.report({'ERROR'}, "Armature has no Aether rig settings")
            return {'CANCELLED'}

        modules = aether_rig.modules
        index = aether_rig.module_index
        if index < 0 or index >= len(modules):
            self.report({'WARNING'}, "Select a module to move")
            return {'CANCELLED'}

        start, end = _get_group_bounds(modules, index)
        moved_index = index

        if index == start:
            group_size = end - start

            if self.direction == 'UP':
                if start == 0:
                    self.report({'INFO'}, "This group is already at the top")
                    return {'CANCELLED'}

                previous_start, _ = _get_group_bounds(modules, start - 1)
                for offset in range(group_size):
                    modules.move(start + offset, previous_start + offset)
                moved_index = previous_start
            else:
                if end >= len(modules):
                    self.report({'INFO'}, "This group is already at the bottom")
                    return {'CANCELLED'}

                _, next_end = _get_group_bounds(modules, end)
                for _ in range(group_size):
                    modules.move(start, next_end - 1)
                moved_index = next_end - group_size
        else:
            if self.direction == 'UP':
                modules.move(index, index - 1)
                moved_index = index - 1
            else:
                if index >= end - 1:
                    self.report({'INFO'}, "This module is already last in its fallback group")
                    return {'CANCELLED'}

                modules.move(index, index + 1)
                moved_index = index + 1

        _reindex_module_groups(aether_rig)
        aether_rig.custom_modules_initialized = True
        aether_rig.module_index = moved_index
        return {'FINISHED'}


class AETHER_OT_Remove_Template_Module(bpy.types.Operator):
    bl_idname = "aether.remove_template_module"
    bl_label = "Remove Template Module"
    bl_description = "Remove this module from the rig's current temporary module selection"
    bl_options = {'UNDO'}

    module_index: bpy.props.IntProperty(
        name="Module Index",
        default=-1,
    ) # type: ignore

    def execute(self, context):
        armature = context.active_object
        if not armature or armature.type != 'ARMATURE':
            self.report({'ERROR'}, "Select an armature")
            return {'CANCELLED'}

        aether_rig = getattr(armature, 'aether_rig', None)
        if not aether_rig:
            self.report({'ERROR'}, "Armature has no Aether rig settings")
            return {'CANCELLED'}

        if self.module_index < 0 or self.module_index >= len(aether_rig.modules):
            self.report({'WARNING'}, "Invalid module index")
            return {'CANCELLED'}

        aether_rig.modules.remove(self.module_index)
        _reindex_module_groups(aether_rig)
        aether_rig.custom_modules_initialized = True
        aether_rig.module_index = min(self.module_index, len(aether_rig.modules) - 1)

        return {'FINISHED'}


class AETHER_OT_Solo_Bone_Collections(bpy.types.Operator):
    bl_idname = "aether.solo_bone_collections"
    bl_label = "Solo Selected"
    bl_description = "Toggle solo for bone collections."
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        armature = context.active_object
        if not armature or armature.type != 'ARMATURE':
            return {'CANCELLED'}
        
        mode = bpy.context.mode
        if mode not in {'POSE', 'EDIT_ARMATURE'}:
            return {'CANCELLED'}
        
        any_soloed = any(collection.is_solo for collection in armature.data.collections)
        
        if any_soloed:
            for collection in armature.data.collections:
                collection.is_solo = False
        else:
            selected_bones = context.selected_pose_bones if context.mode == 'POSE' else []
            
            if not selected_bones:
                return {'CANCELLED'}
            
            selected_collections = set()
            for pose_bone in selected_bones:
                bone = armature.data.bones.get(pose_bone.name)
                if bone:
                    for collection in bone.collections:
                        selected_collections.add(collection)
            
            if not selected_collections:
                return {'CANCELLED'}
            
            for collection in selected_collections:
                collection.is_solo = True
        
        return {'FINISHED'}


def register():
    global _DYNAMIC_ADD_MENU_CLASSES

    _DYNAMIC_ADD_MENU_CLASSES = [
        _build_family_menu_class(mode, family_name)
        for mode in ('GROUP', 'FALLBACK')
        for family_name in get_modules_by_family().keys()
    ]

    for menu_class in _DYNAMIC_ADD_MENU_CLASSES:
        bpy.utils.register_class(menu_class)

    bpy.utils.register_class(AETHER_MT_Add_Group_Module_Menu)
    bpy.utils.register_class(AETHER_MT_Add_Fallback_Module_Menu)
    bpy.utils.register_class(AETHER_MT_Populate_Custom_Template_Menu)
    bpy.utils.register_class(AETHER_OT_Add_Template_Module)
    bpy.utils.register_class(AETHER_OT_Populate_Custom_Template)
    bpy.utils.register_class(AETHER_OT_Save_Custom_Template_JSON)
    bpy.utils.register_class(AETHER_OT_Export_Custom_Template_Clipboard)
    bpy.utils.register_class(AETHER_OT_Import_Custom_Template_Clipboard)
    bpy.utils.register_class(AETHER_OT_Move_Template_Module)
    bpy.utils.register_class(AETHER_OT_Remove_Template_Module)
    bpy.utils.register_class(AETHER_OT_Solo_Bone_Collections)

def unregister():
    global _DYNAMIC_ADD_MENU_CLASSES

    bpy.utils.unregister_class(AETHER_OT_Solo_Bone_Collections)
    bpy.utils.unregister_class(AETHER_OT_Remove_Template_Module)
    bpy.utils.unregister_class(AETHER_OT_Move_Template_Module)
    bpy.utils.unregister_class(AETHER_OT_Import_Custom_Template_Clipboard)
    bpy.utils.unregister_class(AETHER_OT_Export_Custom_Template_Clipboard)
    bpy.utils.unregister_class(AETHER_OT_Save_Custom_Template_JSON)
    bpy.utils.unregister_class(AETHER_OT_Populate_Custom_Template)
    bpy.utils.unregister_class(AETHER_OT_Add_Template_Module)
    bpy.utils.unregister_class(AETHER_MT_Populate_Custom_Template_Menu)
    bpy.utils.unregister_class(AETHER_MT_Add_Fallback_Module_Menu)
    bpy.utils.unregister_class(AETHER_MT_Add_Group_Module_Menu)

    for menu_class in reversed(_DYNAMIC_ADD_MENU_CLASSES):
        bpy.utils.unregister_class(menu_class)

    _DYNAMIC_ADD_MENU_CLASSES = []
