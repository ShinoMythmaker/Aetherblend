from ...core.aether_rig_generator import AetherRigGenerator
from ...core.shared import RigModule, Template
from ...preferences import get_default_custom_template_path, get_preferences
from .templates import AVAILABLE_MODULES, CS_COLORSETS, get_module_key
from .templates.overrides import WO_DEFAULT, WO_NSFW, PO_DEFAULT
from pathlib import Path
import bpy
import json
import re


## For Dropdowns
CUSTOM_TEMPLATE_NAME = 'Custom'
_TEMPLATE_JSON_DIR = Path(__file__).resolve().parent / "templates" / "json"
_DEFAULT_OVERRIDE_KEYS = ["WO_DEFAULT", "PO_DEFAULT"]
_OVERRIDES_BY_KEY = {
    "WO_DEFAULT": WO_DEFAULT,
    "WO_NSFW": WO_NSFW,
    "PO_DEFAULT": PO_DEFAULT,
}


def get_custom_template_json_dir() -> Path:
    """Resolve the active custom template folder from preferences."""
    custom_path = ""

    try:
        prefs = get_preferences()
        custom_path = (getattr(prefs, "custom_template_path", "") or "").strip()
    except Exception:
        custom_path = ""

    if custom_path:
        return Path(bpy.path.abspath(custom_path))

    return Path(get_default_custom_template_path())


def _iter_template_json_files():
    """Yield template json files from builtin and custom folders."""
    for root_dir in (_TEMPLATE_JSON_DIR, get_custom_template_json_dir()):
        if not root_dir.exists():
            continue
        for file_path in sorted(root_dir.glob("*.json")):
            yield file_path


def _load_template_definitions() -> dict[str, dict]:
    """Load template definitions from JSON files on disk."""
    templates: dict[str, dict] = {}

    for file_path in _iter_template_json_files():
        try:
            with file_path.open("r", encoding="utf-8") as f:
                data = json.load(f)

            template_name = (data.get("name") or file_path.stem).strip()
            module_keys = data.get("module_keys") or data.get("modules") or []

            if not template_name or not isinstance(module_keys, list):
                continue

            templates[template_name] = {
                "name": template_name,
                "override_keys": data.get("override_keys"),
                "module_keys": module_keys,
                "path": str(file_path),
            }
        except Exception:
            # Keep loading the remaining files even if one file is malformed.
            continue

    return templates


def get_available_template_names() -> list[str]:
    """Return template names discovered from JSON files."""
    return sorted(_load_template_definitions().keys())


def _resolve_overrides(definition: dict) -> list | None:
    """Resolve override objects declared in template JSON."""
    override_keys = definition.get("override_keys")
    if not isinstance(override_keys, list):
        override_keys = _DEFAULT_OVERRIDE_KEYS

    resolved: list = []
    for override_key in override_keys:
        override = _OVERRIDES_BY_KEY.get(override_key)
        if override is not None:
            resolved.append(override)

    return resolved or None


def _template_from_definition(template_name: str, definition: dict) -> Template | None:
    """Build a runtime Template object from one JSON definition."""
    module_groups: list[list[RigModule]] = []

    for key_group in definition.get("module_keys", []):
        if not isinstance(key_group, list):
            continue

        runtime_group: list[RigModule] = []
        for module_key in key_group:
            module = AVAILABLE_MODULES.get(module_key)
            if module:
                runtime_group.append(module)
        if runtime_group:
            module_groups.append(runtime_group)

    if not module_groups:
        return None

    overrides = _resolve_overrides(definition)
    return Template(name=template_name, overrides=overrides, modules=module_groups)


def _get_template_from_json(template_name: str) -> Template | None:
    """Resolve one template from JSON definitions."""
    definition = _load_template_definitions().get(template_name)
    if not definition:
        return None
    return _template_from_definition(template_name, definition)


def save_custom_template_json(template_name: str, module_keys: list[list[str]]) -> Path:
    """Save a custom template definition to the custom JSON folder."""
    custom_dir = get_custom_template_json_dir()
    custom_dir.mkdir(parents=True, exist_ok=True)

    safe_stem = re.sub(r"[^a-zA-Z0-9_-]+", "_", template_name.strip()).strip("_").lower()
    if not safe_stem:
        safe_stem = "custom_template"

    file_path = custom_dir / f"{safe_stem}.json"
    payload = {
        "name": template_name,
        "module_keys": module_keys,
    }

    with file_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    return file_path


def get_template_items(self, context):
    """Get available templates for dropdown."""
    items = [(name, name, "") for name in get_available_template_names()]
    items.append((CUSTOM_TEMPLATE_NAME, CUSTOM_TEMPLATE_NAME, "Use the editable custom module list"))
    return items


def get_colorset_items(self, context):
    """Get available colorsets for dropdown."""
    return [(key, key, "") for key in CS_COLORSETS.keys()]


## Defaults 
DEFAULT_TEMPLATE_NAME = 'Player SFW'
DEFAULT_COLORSET_NAME = 'AetherBlend'


## Translators
def is_custom_template_selected(aether_rig) -> bool:
    """Return whether the rig is currently using the editable custom module list."""
    return getattr(aether_rig, 'selected_template', DEFAULT_TEMPLATE_NAME) == CUSTOM_TEMPLATE_NAME


def resolve_module_groups(aether_rig) -> list[list[RigModule]]:
    """Convert the stored module UI collection back into grouped runtime modules."""
    if not aether_rig or not hasattr(aether_rig, 'modules'):
        return []

    grouped_modules: list[list[RigModule]] = []

    for item in aether_rig.modules:
        module = AVAILABLE_MODULES.get(item.module_key)
        if not module:
            continue

        group_index = getattr(item, 'group_index', -1)
        if group_index < 0:
            grouped_modules.append([module])
            continue

        while len(grouped_modules) <= group_index:
            grouped_modules.append([])
        grouped_modules[group_index].append(module)

    return [group for group in grouped_modules if group]


def populate_modules_from_template(aether_rig, template_name: str | None = None) -> None:
    """Populate the editable custom module list from a JSON template definition."""
    if not aether_rig or not hasattr(aether_rig, 'modules'):
        return

    available_names = get_available_template_names()
    source_name = template_name or getattr(aether_rig, 'custom_template_source', DEFAULT_TEMPLATE_NAME)
    template = _get_template_from_json(source_name) or _get_template_from_json(DEFAULT_TEMPLATE_NAME)

    aether_rig.modules.clear()
    aether_rig.custom_template_source = source_name if source_name in available_names else DEFAULT_TEMPLATE_NAME

    if not template:
        aether_rig.custom_modules_initialized = True
        aether_rig.module_index = 0
        return

    for group_index, module_group in enumerate(template.modules):
        for module in module_group:
            item = aether_rig.modules.add()
            item.module_key = get_module_key(module)
            item.group_index = group_index

    aether_rig.custom_modules_initialized = True
    aether_rig.module_index = 0 if aether_rig.modules else 0


## Get selections 
def get_selected_template(aether_rig):
    """Get the template data currently driving generation."""
    template_name = getattr(aether_rig, 'selected_template', DEFAULT_TEMPLATE_NAME)
    if template_name == CUSTOM_TEMPLATE_NAME:
        template_name = getattr(aether_rig, 'custom_template_source', DEFAULT_TEMPLATE_NAME)
    return _get_template_from_json(template_name) or _get_template_from_json(DEFAULT_TEMPLATE_NAME)


def get_selected_colorset(aether_rig):
    """Get the currently selected colorset override, if any."""
    colorset_name = getattr(aether_rig, 'selected_colorset', DEFAULT_COLORSET_NAME)
    return CS_COLORSETS.get(colorset_name)


def get_selected_modules(aether_rig):
    """Return the module groups that should be used for generation."""
    if is_custom_template_selected(aether_rig):
        return resolve_module_groups(aether_rig)

    template = get_selected_template(aether_rig)
    return template.modules if template else []


## Handlers
def on_template_changed(self, context):
    """Initialize the custom module editor the first time Custom is selected."""
    if not is_custom_template_selected(self):
        return

    if not getattr(self, 'custom_modules_initialized', False):
        self.modules.clear()
        self.module_index = 0


## Rig Generator
def get_rig_generator(aether_rig):
    """Build an AetherRigGenerator from the rig's current template settings."""
    template = get_selected_template(aether_rig)
    color_sets = get_selected_colorset(aether_rig)
    modules = get_selected_modules(aether_rig)

    if not template or not color_sets or not modules:
        return None

    generator_name = CUSTOM_TEMPLATE_NAME if is_custom_template_selected(aether_rig) else template.name

    return AetherRigGenerator(
        name=generator_name,
        color_sets=color_sets,
        overrides=template.overrides,
        modules=modules,
    )

def register():
    pass

def unregister():
    pass
