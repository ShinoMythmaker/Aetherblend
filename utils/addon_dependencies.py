"""Check the additional Blender add-ons AetherBlend can use."""

from dataclasses import dataclass
from types import ModuleType
from typing import Literal

import addon_utils

AddonStatus = Literal["ENABLED", "INACTIVE", "MISSING"]


@dataclass(frozen=True)
class Addon:
    """Describe one supported Blender add-on."""

    name: str
    module: str
    required: bool
    purpose: str
    url: str
    builtin: bool = False


ADDONS = (
    Addon(
        name="Rigify",
        module="rigify",
        required=True,
        purpose="Required for rig generation",
        url="https://docs.blender.org/manual/en/latest/addons/rigging/rigify/index.html",
        builtin=True,
    ),
    Addon(
        name="Meddle Tools",
        module="meddle",
        required=False,
        purpose="Optional Meddle shader integration",
        url="https://github.com/PassiveModding/MeddleTools",
    ),
    Addon(
        name="FFGear",
        module="ffgear",
        required=False,
        purpose="Optional FFGear shader integration",
        url="https://github.com/kajupe/FFGear",
    ),
)


def _normalize_addon_name(value: str) -> str:
    return "".join(character for character in value.lower() if character.isalnum())


def _matching_addons(module_name: str | None, display_name: str | None) -> list[ModuleType]:
    names = {_normalize_addon_name(value) for value in (module_name, display_name) if value}
    if not names:
        return []
    matches = []
    for module in addon_utils.modules():
        module_names = {
            _normalize_addon_name(module.__name__),
            _normalize_addon_name(module.__name__.rsplit(".", 1)[-1]),
        }
        name = getattr(module, "bl_info", {}).get("name")
        if isinstance(name, str):
            module_names.add(_normalize_addon_name(name))
        if names.intersection(module_names):
            matches.append(module)
    return matches


def resolve_addon_module_name(*, module_name: str | None = None, display_name: str | None = None) -> str | None:
    """Resolve the installed module name, including Blender extension namespaces."""
    matches = _matching_addons(module_name, display_name)
    for module in matches:
        if addon_utils.check(module.__name__)[1]:
            return module.__name__
    return matches[0].__name__ if matches else None


def is_addon_enabled(*, module_name: str | None = None, display_name: str | None = None) -> bool:
    """Return whether a matching Blender add-on is enabled."""
    matches = _matching_addons(module_name, display_name)
    if matches:
        return any(addon_utils.check(module.__name__)[1] for module in matches)
    return bool(module_name and addon_utils.check(module_name)[1])


def get_addon_status(addon: Addon) -> AddonStatus:
    """Distinguish an enabled add-on from an inactive or missing installation."""
    matches = _matching_addons(addon.module, addon.name)
    if any(addon_utils.check(module.__name__)[1] for module in matches):
        return "ENABLED"
    if matches:
        return "INACTIVE"
    return "ENABLED" if addon_utils.check(addon.module)[1] else "MISSING"


def get_addon_support_url(*, module_name: str | None = None, display_name: str | None = None) -> str | None:
    """Return the supported add-on's documentation or project URL."""
    for addon in ADDONS:
        if module_name == addon.module or display_name == addon.name:
            return addon.url
    return None


def get_required_addons() -> list[Addon]:
    """Return add-ons required for AetherBlend's core rig-generation workflow."""
    return [addon for addon in ADDONS if addon.required]


def get_missing_required_addons() -> list[Addon]:
    """Return required add-ons that are missing or inactive."""
    return [
        addon
        for addon in get_required_addons()
        if not is_addon_enabled(module_name=addon.module, display_name=addon.name)
    ]


def missing_required_addon_names() -> list[str]:
    """Return names of required add-ons that need installation or activation."""
    return [addon.name for addon in get_missing_required_addons()]


def print_missing_required_addons() -> None:
    """Print a startup warning when rig generation's requirements are unavailable."""
    missing = missing_required_addon_names()
    if missing:
        print(
            "[AetherBlend] Required for rig generation but missing or inactive: "
            + ", ".join(missing)
            + ". Install/enable them in Edit > Preferences > Add-ons."
        )
