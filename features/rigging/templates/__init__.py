import importlib
import pkgutil
from collections import defaultdict

from ....core.shared import AetherRigGenerator, RigModule, Template ,WidgetOverride
from ....core.rigify import *


from .colorsets import *
from .ui_collections import *
from .overrides import *
from . import modules as module_root

from .modules import *


def build_module_registry() -> tuple[dict[str, RigModule], dict[str, dict[str, RigModule]]]:
    """Auto-discover all rig modules from the modules package and group them by type."""
    available_modules: dict[str, RigModule] = {}
    modules_by_type: dict[str, dict[str, RigModule]] = defaultdict(dict)

    for module_info in pkgutil.iter_modules(module_root.__path__):
        if not module_info.ispkg or module_info.name.startswith("_"):
            continue

        family_name = module_info.name
        family = importlib.import_module(f"{module_root.__name__}.{family_name}")

        for attr_name in sorted(dir(family)):
            if attr_name.startswith("_"):
                continue

            value = getattr(family, attr_name)
            if not isinstance(value, RigModule):
                continue

            key = f"{family_name}.{attr_name}"
            available_modules[key] = value
            modules_by_type[value.type][key] = value

    sorted_modules = dict(sorted(available_modules.items()))
    sorted_types = {
        module_type: dict(sorted(entries.items()))
        for module_type, entries in sorted(modules_by_type.items())
    }
    return sorted_modules, sorted_types


def get_modules_by_type(module_type: str | None = None):
    """Return all modules grouped by type, or a single type bucket if requested."""
    if module_type is None:
        return MODULES_BY_TYPE
    return MODULES_BY_TYPE.get(module_type, {})


AVAILABLE_MODULES, MODULES_BY_TYPE = build_module_registry()


## Templates
## About Modules: Each modules is a self-contained rig component. you can add as many modules as you wish and the generator will handle sorting and excution. 
## Each module has a type, wich is important because there can only be one of each type. 
## Should there be multiple of the same type, then the generator will prio the first one and use the second as a fallback in case the first one fails to generate.
TEMPLATES = {
    'Player SFW':   Template(
        name = "Player SFW",
        color_sets=[CS_AETHER_BLEND], 
        overrides=[WO_DEFAULT, PO_DEFAULT],
        modules = [face.detailed, spine.default, arms.default, legs.default, skirt.default, hands.default, tail.default, face.detailed, ears.miqo, ears.viera, hair.default]
    ),
    'Player SFW (IVCS)': Template(
        name= "Player SFW (IVCS)",
        color_sets=[CS_AETHER_BLEND], 
        overrides=[WO_DEFAULT, PO_DEFAULT],
        modules = [spine.default, arms.default, legs.default, skirt.default, hands.ivcs, toes.ivcs, tail.default, face.detailed, ears.miqo, ears.viera, hair.default]
    ),
    'Player NSFW (IVCS)': Template(
        name= "Player NSFW (IVCS)",
        color_sets=[CS_AETHER_BLEND],
        overrides=[WO_NSFW, PO_DEFAULT],
        modules = [spine.default, arms.default, legs.default, skirt.default, hands.ivcs, toes.ivcs, tail.default, face.detailed, ears.miqo, ears.viera, hair.default, genitals.ivcs_both]
    ),
    'Dynamic': Template(
        name= "Dynamic",
        color_sets=[CS_AETHER_BLEND], 
        overrides=[WO_NSFW, PO_DEFAULT],
        modules = [ears.miqo, ears.viera, hair.default, face.detailed, arms.default, spine.default, hands.ivcs, hands.default, legs.default, toes.ivcs, skirt.default, tail.default, genitals.ivcs_both]
    ),
}