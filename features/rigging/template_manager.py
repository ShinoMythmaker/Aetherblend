from ...core.shared import AetherRigGenerator, RigModule
from .templates import AVAILABLE_MODULES, CS_COLORSETS, TEMPLATES, get_module_key


## For Dropdowns
def get_template_items(self, context):
    """Get available templates for dropdown."""
    return [(key, key, "") for key in TEMPLATES.keys()]

def get_colorset_items(self, context):
    """Get available colorsets for dropdown."""
    return [(key, key, "") for key in CS_COLORSETS.keys()]

## Defaults 
DEFAULT_TEMPLATE_NAME = 'Player SFW'
DEFAULT_COLORSET_NAME = 'AetherBlend'

## Translators
def resolve_module_groups(aether_rig) -> list[list[RigModule]]:
    """Module Prop to Template"""
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


def sync_modules_from_template(aether_rig) -> None:
    """Template to Module Prop"""
    if not aether_rig or not hasattr(aether_rig, 'modules'):
        return

    template = get_selected_template(aether_rig)
    aether_rig.modules.clear()

    if not template:
        return

    for group_index, module_group in enumerate(template.modules):
        for module in module_group:
            item = aether_rig.modules.add()
            item.module_key = get_module_key(module)
            item.group_index = group_index

## Get selections 
def get_selected_template(aether_rig):
    """Get the currently selected template."""
    template_name = getattr(aether_rig, 'selected_template', DEFAULT_TEMPLATE_NAME)
    return TEMPLATES.get(template_name)

def get_selected_colorset(aether_rig):
    """Get the currently selected colorset override, if any."""
    colorset_name = getattr(aether_rig, 'selected_colorset', DEFAULT_COLORSET_NAME)
    return CS_COLORSETS.get(colorset_name)

def get_selected_modules(aether_rig):
    """Return ordered module priority groups, or fall back to the chosen template."""
    selected_groups = resolve_module_groups(aether_rig)
    if selected_groups:
        return selected_groups

    template = get_selected_template(aether_rig)
    return template.modules if template else []

## Handlers
def on_template_changed(self, context):
    """When the template changes, rebuild the rig's temporary module selection."""
    sync_modules_from_template(self)

## Rig Generator
def get_rig_generator(aether_rig):
    """Build an AetherRigGenerator from the rig's current template settings."""
    template = get_selected_template(aether_rig)
    color_sets = get_selected_colorset(aether_rig)
    modules = get_selected_modules(aether_rig)

    if not template or not color_sets or not modules:
        return None

    return AetherRigGenerator(
        name=template.name,
        color_sets=color_sets,
        overrides=template.overrides,
        modules=modules,
    )

def register():
    pass

def unregister():
    pass
