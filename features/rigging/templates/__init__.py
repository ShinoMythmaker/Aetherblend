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


def build_module_registry() -> tuple[
    dict[str, RigModule],
    dict[str, dict[str, RigModule]],
    dict[str, dict[str, RigModule]],
]:
    """Auto-discover all rig modules from the modules package and group them by category and family."""
    available_modules: dict[str, RigModule] = {}
    modules_by_type: dict[str, dict[str, RigModule]] = defaultdict(dict)
    modules_by_family: dict[str, dict[str, RigModule]] = defaultdict(dict)

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
            modules_by_family[family_name][key] = value

    sorted_modules = dict(sorted(available_modules.items()))
    sorted_types = {
        module_type: dict(sorted(entries.items()))
        for module_type, entries in sorted(modules_by_type.items())
    }
    sorted_families = {
        family_name: dict(sorted(entries.items()))
        for family_name, entries in sorted(modules_by_family.items())
    }
    return sorted_modules, sorted_types, sorted_families


def get_modules_by_type(module_type: str | None = None):
    """Return all modules grouped by type, or a single type bucket if requested."""
    if module_type is None:
        return MODULES_BY_TYPE
    return MODULES_BY_TYPE.get(module_type, {})


def get_modules_by_family(family_name: str | None = None):
    """Return all modules grouped by family, or a single family bucket if requested."""
    if family_name is None:
        return MODULES_BY_FAMILY
    return MODULES_BY_FAMILY.get(family_name, {})


AVAILABLE_MODULES, MODULES_BY_TYPE, MODULES_BY_FAMILY = build_module_registry()
MODULE_KEYS_BY_ID = {id(module): key for key, module in AVAILABLE_MODULES.items()}


def get_module_key(module: RigModule) -> str:
    """Resolve the registry key for a rig module instance."""
    return MODULE_KEYS_BY_ID.get(id(module), "")


## Templates
## About Modules: Each entry in `modules` is an ordered priority group.
## Use `[module]` for a standalone module, or `[primary, fallback, ...]` when several modules should compete for the same slot.
## `RigModule.type` now describes behavior category: `Generation`, `UI-Addon`, or `Patch`.
## Only modules inside the same inner list will fight for priority; every other group is always evaluated in order.
TEMPLATES = {
    'Player SFW':   Template(
        name = "Player SFW",
        overrides=[WO_DEFAULT, PO_DEFAULT],
        modules = [
            [face.detailed],
            [spine.default],
            [arms.default],
            [legs.default],
            [skirt.default],
            [hands.default],
            [tail.default],
            [ears.miqo, ears.viera],
            [hair.default],
            [base.base],
            [base.base],
        ]
    ),
    'Player SFW (IVCS)': Template(
        name= "Player SFW (IVCS)",
        overrides=[WO_DEFAULT, PO_DEFAULT],
        modules = [
            [spine.default],
            [arms.default],
            [legs.default],
            [skirt.default],
            [hands.ivcs],
            [toes.ivcs],
            [tail.default],
            [face.detailed],
            [ears.miqo, ears.viera],
            [hair.default],
            [base.base],
        ]
    ),
    'Player NSFW (IVCS)': Template(
        name= "Player NSFW (IVCS)",
        overrides=[WO_NSFW, PO_DEFAULT],
        modules = [
            [spine.default],
            [arms.default],
            [legs.default],
            [skirt.default],
            [hands.ivcs],
            [toes.ivcs],
            [tail.default],
            [face.detailed],
            [ears.miqo, ears.viera],
            [hair.default],
            [genitals.ivcs_both],
            [base.base],
        ]
    ),
    'Dynamic': Template(
        name= "Dynamic",
        overrides=[WO_NSFW, PO_DEFAULT],
        modules = [
            [ears.miqo, ears.viera],
            [hair.default],
            [face.detailed],
            [arms.default],
            [spine.default],
            [hands.ivcs, hands.default],
            [legs.default],
            [toes.ivcs],
            [skirt.default],
            [tail.default],
            [genitals.ivcs_both],
            [base.base],
        ]
    ),
}