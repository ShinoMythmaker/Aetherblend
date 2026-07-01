"""Helpers for checking Blender add-on dependencies."""

import addon_utils
from typing import Literal, get_args


FEATURE_SETS: dict[str, str] = {
    "COMMON": "Common",
    "FFXIV": "FFXIV",
    "VRM": "VRM",
}

COMMON_FEATURE_SET_TOKEN = "COMMON"

AddonSourceToken = Literal["BUILTIN", "EXTERNAL"]


# Keep dependency definitions in one place so startup checks and panel gating stay aligned.
REQUIRED_ADDONS = (
    {
        "name": "Rigify",
        "module": "rigify",
        "feature_sets": ("COMMON",),
        "source": "BUILTIN",
    },
    {
        "name": "Meddle Tools",
        "module": "meddle",
        "url": "https://github.com/PassiveModding/MeddleTools",
        "feature_sets": ("FFXIV",),
        "source": "EXTERNAL",
        "link_label": "GitHub",
    },
    {
        "name": "FFGear",
        "module": "ffgear",
        "url": "https://github.com/kajupe/FFGear",
        "feature_sets": ("FFXIV",),
        "source": "EXTERNAL",
        "link_label": "GitHub",
    },
    {
        "name": "VRM format",
        "module": "vrm",
        "url": "https://extensions.blender.org/add-ons/vrm/",
        "feature_sets": ("VRM",),
        "source": "EXTERNAL",
        "link_label": "Blender",
    },
)


def get_feature_set_tokens() -> tuple[str, ...]:
    """Return feature-set tokens in UI order."""
    return tuple(FEATURE_SETS.keys())


def get_feature_set_label(token: str) -> str:
    """Return display label for a feature-set token."""
    return FEATURE_SETS.get(token, token)


def is_common_feature_set(token: str) -> bool:
    """Return whether the token represents the always-on common feature set."""
    return token == COMMON_FEATURE_SET_TOKEN

def get_addon_feature_sets(entry: dict[str, object]) -> tuple[str, ...]:
    """Return feature-set tags for an add-on definition."""
    raw = entry.get("feature_sets")
    if not isinstance(raw, (tuple, list)):
        return (COMMON_FEATURE_SET_TOKEN,)

    values: list[str] = []
    for value in raw:
        if not isinstance(value, str) or value not in FEATURE_SETS:
            continue
        if value and value not in values:
            values.append(value)

    if not values:
        return (COMMON_FEATURE_SET_TOKEN,)

    return tuple(values)


def get_addon_feature_label(entry: dict[str, object]) -> str:
    """Return a human-readable label for an add-on's feature sets."""
    labels: list[str] = []
    for feature_set in get_addon_feature_sets(entry):
        labels.append(get_feature_set_label(feature_set))
    return " + ".join(labels)


def is_addon_required_for_feature_sets(entry: dict[str, object], feature_sets: set[str] | None) -> bool:
    """Return whether an add-on applies to the active feature-set selection."""
    addon_feature_sets = set(get_addon_feature_sets(entry))
    if COMMON_FEATURE_SET_TOKEN in addon_feature_sets:
        return True

    if feature_sets is None:
        return True

    return bool(addon_feature_sets.intersection(feature_sets))


def get_required_addons(feature_sets: set[str] | None = None) -> list[dict[str, object]]:
    """Return dependency entries scoped to selected feature sets."""
    required: list[dict[str, object]] = []
    for entry in REQUIRED_ADDONS:
        if is_addon_required_for_feature_sets(entry, feature_sets):
            required.append(entry)
    return required


def get_addons_for_feature_set(feature_set: str) -> list[dict[str, object]]:
    """Return dependency entries assigned to a specific feature set token."""
    addons: list[dict[str, object]] = []
    for entry in REQUIRED_ADDONS:
        if feature_set in get_addon_feature_sets(entry):
            addons.append(entry)
    return addons


def get_addon_entry(*, module_name: str | None = None, display_name: str | None = None) -> dict[str, object] | None:
    """Return metadata entry for a dependency add-on."""
    if not module_name and not display_name:
        return None

    for entry in REQUIRED_ADDONS:
        if module_name and entry.get("module") == module_name:
            return entry
        if display_name and entry.get("name") == display_name:
            return entry

    return None


def get_addon_source(entry: dict[str, object]) -> str:
    """Return add-on distribution source (built-in or external)."""
    source = entry.get("source")
    if isinstance(source, str) and source in get_args(AddonSourceToken):
        return source
    return "EXTERNAL"


def is_builtin_addon_entry(entry: dict[str, object]) -> bool:
    """Return whether a dependency is a built-in Blender add-on."""
    return get_addon_source(entry) == "BUILTIN"


def get_addon_link_label(entry: dict[str, object]) -> str:
    """Return preferred CTA label for external add-on links."""
    label = entry.get("link_label")
    if isinstance(label, str) and label.strip():
        return label.strip()
    return "Link"


def _normalize_addon_name(value: str) -> str:
    return "".join(ch for ch in value.lower() if ch.isalnum())


def _module_name_for_entry(entry: dict[str, object]) -> str | None:
    module_name = entry.get("module")
    if module_name:
        return module_name

    display_name = entry.get("name")
    if not display_name:
        return None

    target_name = _normalize_addon_name(str(display_name))

    for module in addon_utils.modules():
        bl_info = getattr(module, "bl_info", {})
        module_display_name = bl_info.get("name")
        if not isinstance(module_display_name, str):
            continue

        if _normalize_addon_name(module_display_name) == target_name:
            return module.__name__

    return None


def resolve_addon_module_name(*, module_name: str | None = None, display_name: str | None = None) -> str | None:
    """Resolve an add-on module name from module/display inputs."""
    if module_name:
        return module_name
    if display_name:
        return _module_name_for_entry({"name": display_name})
    return None


def get_addon_support_url(*, module_name: str | None = None, display_name: str | None = None) -> str | None:
    """Return best effort support URL (prefer GitHub/doc links) for an add-on."""
    resolved_module = resolve_addon_module_name(module_name=module_name, display_name=display_name)

    if resolved_module:
        for module in addon_utils.modules():
            if module.__name__ != resolved_module:
                continue

            bl_info = getattr(module, "bl_info", {})
            for key in ("website", "doc_url", "wiki_url", "tracker_url"):
                url = bl_info.get(key)
                if isinstance(url, str) and url.startswith(("http://", "https://")):
                    return url
            break

    for entry in REQUIRED_ADDONS:
        if module_name and entry.get("module") == module_name:
            return entry.get("url")
        if display_name and entry.get("name") == display_name:
            return entry.get("url")

    return None


def is_addon_enabled(*, module_name: str | None = None, display_name: str | None = None) -> bool:
    """Return True when the requested add-on exists and is enabled."""
    if not module_name and not display_name:
        return False

    candidates: list[str] = []
    if module_name:
        candidates.append(_normalize_addon_name(module_name))
    if display_name:
        resolved_module = _module_name_for_entry({"name": display_name})
        # This module name can for example be: bl_ext.raw_githubusercontent_com.FFGear
        if resolved_module and resolved_module not in candidates:
            last_part_of_module_name = resolved_module.split(".")[-1]
            candidates.append(_normalize_addon_name(last_part_of_module_name))
    # candidates is now ["ffgear", "ffgear"] or ["meddle", "meddletools"], etc. Second entry depends on what the module is actually named, and is generally more accurate.

    if not candidates:
        return False

    found_match = False
    for module in addon_utils.modules():
        name: str = module.__name__
        normalized_full_name = _normalize_addon_name(name)
        normalized_last_part = _normalize_addon_name(name.split(".")[-1])
        if normalized_full_name not in candidates and normalized_last_part not in candidates:
            continue

        found_match = True
        try:
            _is_default, is_enabled = addon_utils.check(name)
        except Exception:
            is_enabled = False

        if is_enabled:
            return True

    # Fallback for direct module checks when module list resolution misses the name variant.
    if module_name and not found_match:
        try:
            _is_default, is_enabled = addon_utils.check(module_name)
            return bool(is_enabled)
        except Exception:
            return False

    return False


def get_missing_required_addons(feature_sets: set[str] | None = None) -> list[dict[str, object]]:
    """Return dependency entries that are missing or not enabled."""
    missing: list[dict[str, object]] = []
    for entry in get_required_addons(feature_sets):
        if not is_addon_enabled(
            module_name=entry.get("module"),
            display_name=entry.get("name"),
        ):
            missing.append(entry)

    return missing


def missing_required_addon_names(feature_sets: set[str] | None = None) -> list[str]:
    """Return human readable names for missing required add-ons."""
    names: list[str] = []
    for entry in get_missing_required_addons(feature_sets):
        names.append(entry.get("name") or entry.get("module") or "Unknown add-on")
    return names


def print_missing_required_addons() -> None:
    """Print startup warning for missing required add-ons."""
    missing_names = missing_required_addon_names()
    if not missing_names:
        return

    print(
        "[AetherBlend] Missing required Blender add-ons: "
        + ", ".join(missing_names)
        + ". Enable/install them in Edit > Preferences > Add-ons."
    )
