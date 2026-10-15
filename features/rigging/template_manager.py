"""Backend template lookup and rig generator construction."""
from ...core.aether_rig_generator import AetherRigGenerator
from .library import CS_COLORSETS, DEFAULT_TEMPLATE_NAME, TEMPLATES

DEFAULT_COLORSET_NAME = 'AetherBlend'


def get_template_items(self, context):
    """Dropdown items for the per-rig template property."""
    return [(name, name, "") for name in TEMPLATES]


def get_colorset_items(self, context):
    """Dropdown items for the colorset override."""
    return [(key, key, "") for key in CS_COLORSETS]


def get_rig_generator(aether_rig):
    """Build an AetherRigGenerator from the rig's template and colorset, or None if either is missing."""
    template = TEMPLATES.get(getattr(aether_rig, 'template', DEFAULT_TEMPLATE_NAME)) or TEMPLATES[DEFAULT_TEMPLATE_NAME]
    color_sets = CS_COLORSETS.get(getattr(aether_rig, 'selected_colorset', DEFAULT_COLORSET_NAME))

    if not color_sets:
        return None

    return AetherRigGenerator(name=template.name, color_sets=color_sets, modules=template.modules)


def register():
    pass


def unregister():
    pass
