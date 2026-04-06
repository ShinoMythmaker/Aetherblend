from ...core.shared import AetherRigGenerator
from .templates import AVAILABLE_MODULES, CS_COLORSETS, TEMPLATES


def get_template_items(self, context):
    """Get available templates for dropdown."""
    return [(key, key, "") for key in TEMPLATES.keys()]

def get_colorset_items(self, context):
    """Get available colorsets for dropdown."""
    return [(key, key, "") for key in CS_COLORSETS.keys()]

DEFAULT_TEMPLATE_NAME = 'Player SFW'


def get_module_key(module) -> str:
    """Resolve the registry key for a rig module instance."""
    for key, available_module in AVAILABLE_MODULES.items():
        if available_module is module:
            return key
    return ""


def sync_modules_from_template(aether_rig) -> None:
    """Fill the rig's temporary module selection from the currently selected template."""
    if not aether_rig or not hasattr(aether_rig, 'modules'):
        return

    template = get_active_template(aether_rig)
    aether_rig.modules.clear()

    if not template:
        return

    for module in template.modules:
        item = aether_rig.modules.add()
        item.module_key = get_module_key(module)


def get_active_template(aether_rig):
    """Get the currently selected template."""
    template_name = getattr(aether_rig, 'selected_template', DEFAULT_TEMPLATE_NAME)
    return TEMPLATES.get(template_name)


def get_selected_modules(aether_rig):
    """Return the rig's current temporary module selection, or fall back to the chosen template."""
    if not aether_rig:
        return []

    selected_modules = []
    for item in aether_rig.modules:
        module = AVAILABLE_MODULES.get(item.module_key)
        if module:
            selected_modules.append(module)

    if selected_modules:
        return selected_modules

    template = get_active_template(aether_rig)
    return list(template.modules) if template else []


def get_display_modules(aether_rig):
    """Return UI-friendly module entries from the rig state, or fall back to the active template."""
    if not aether_rig:
        return []

    display_modules = []
    for item in aether_rig.modules:
        module = AVAILABLE_MODULES.get(item.module_key)
        if not module:
            continue
        display_modules.append({
            "key": item.module_key,
            "name": module.name,
            "type": module.type,
        })

    if display_modules:
        return display_modules

    template = get_active_template(aether_rig)
    if not template:
        return []

    return [
        {
            "key": get_module_key(module),
            "name": module.name,
            "type": module.type,
        }
        for module in template.modules
    ]


def on_template_changed(self, context):
    """When the template changes, rebuild the rig's temporary module selection."""
    sync_modules_from_template(self)


def get_rig_generator(aether_rig):
    """Build an AetherRigGenerator from the rig's current temporary module selection."""    
    template = get_active_template(aether_rig)
    if not template:
        return None
    
    colorset_name = getattr(aether_rig, 'selected_colorset', None)
    
    if colorset_name and colorset_name in CS_COLORSETS:
        color_sets = [CS_COLORSETS[colorset_name]]
    else:
        color_sets = template.color_sets
    
    return AetherRigGenerator(
        name=template.name,
        color_sets=color_sets,
        overrides=template.overrides,
        modules=get_selected_modules(aether_rig)
    )

def register():
    pass

def unregister():
    pass
