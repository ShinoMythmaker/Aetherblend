from ...core.shared import AetherRigGenerator
from .templates import CS_COLORSETS, TEMPLATES


def get_template_items(self, context):
    """Get available templates for dropdown."""
    return [(key, key, "") for key in TEMPLATES.keys()]

def get_colorset_items(self, context):
    """Get available colorsets for dropdown."""
    return [(key, key, "") for key in CS_COLORSETS.keys()]

DEFAULT_TEMPLATE_NAME = 'Player SFW'

def get_active_template(aether_rig):
    """Get the currently selected template."""
    template_name = getattr(aether_rig, 'selected_template', DEFAULT_TEMPLATE_NAME)
    return TEMPLATES.get(template_name)

def get_rig_generator(aether_rig):
    """Build an AetherRigGenerator based on template and colorset override."""    
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
        ui_collections=template.ui_collections,
        overrides=template.overrides,
        bone_groups=template.bone_groups
    )

def register():
    pass

def unregister():
    pass
