from ...core.shared import AetherRigGenerator, RigModule
from .templates import AVAILABLE_MODULES, CS_COLORSETS, TEMPLATES, get_module_key


## For Dropdowns
CUSTOM_TEMPLATE_NAME = 'Custom'


def get_template_items(self, context):
    """Get available templates for dropdown."""
    items = [(key, key, "") for key in TEMPLATES.keys()]
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
    """Populate the editable custom module list from one of the built-in templates."""
    if not aether_rig or not hasattr(aether_rig, 'modules'):
        return

    source_name = template_name or getattr(aether_rig, 'custom_template_source', DEFAULT_TEMPLATE_NAME)
    template = TEMPLATES.get(source_name) or TEMPLATES.get(DEFAULT_TEMPLATE_NAME)

    aether_rig.modules.clear()
    aether_rig.custom_template_source = source_name if source_name in TEMPLATES else DEFAULT_TEMPLATE_NAME

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
    return TEMPLATES.get(template_name) or TEMPLATES.get(DEFAULT_TEMPLATE_NAME)


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
