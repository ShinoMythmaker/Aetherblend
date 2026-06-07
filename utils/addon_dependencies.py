"""Helpers for checking external Blender add-on dependencies."""

import addon_utils


# Keep dependency definitions in one place so startup checks and panel gating stay aligned.
REQUIRED_ADDONS = (
    {"name": "Rigify", "module": "rigify"},
    {"name": "Meddle Tools", "module": "meddle", "url": "https://github.com/PassiveModding/MeddleTools"},
    {"name": "FFGear", "module": "ffgear", "url": "https://github.com/kajupe/FFGear"},
)


def _normalize_addon_name(value: str) -> str:
    return "".join(ch for ch in value.lower() if ch.isalnum())


def _module_name_for_entry(entry: dict[str, str]) -> str | None:
    module_name = entry.get("module")
    if module_name:
        return module_name

    display_name = entry.get("name")
    if not display_name:
        return None

    target_name = _normalize_addon_name(display_name)

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
        candidates.append(module_name)
    if display_name:
        resolved_module = _module_name_for_entry({"name": display_name})
        # This module name can for example be: bl_ext.raw_githubusercontent_com.FFGear
        if resolved_module and resolved_module not in candidates:
            last_part_of_module_name = resolved_module.split(".")[-1]
            candidates.append(_normalize_addon_name(last_part_of_module_name))
    # candidates is now ["ffgear", "ffgear"] or ["meddle", "meddletools"], etc. Second entry depends on what the module is actually named, and is generally more accurate.

    if not candidates:
        return False

    for module in addon_utils.modules():
        name:str = module.__name__
        last_part_of_module_name = name.split(".")[-1]
        if _normalize_addon_name(last_part_of_module_name) in candidates:
            return True

    return False


def get_missing_required_addons() -> list[dict[str, str]]:
    """Return dependency entries that are missing or not enabled."""
    missing: list[dict[str, str]] = []
    for entry in REQUIRED_ADDONS:
        if not is_addon_enabled(
            module_name=entry.get("module"),
            display_name=entry.get("name"),
        ):
            missing.append(entry)

    return missing


def missing_required_addon_names() -> list[str]:
    """Return human readable names for missing required add-ons."""
    names: list[str] = []
    for entry in get_missing_required_addons():
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
