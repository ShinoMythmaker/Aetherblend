"""Live pose streaming to AetherBridge."""

from . import panels, properties, stream

modules = (properties, stream, panels)


def register() -> None:
    """Register bridge properties, operators, and panel."""
    for module in modules:
        module.register()


def unregister() -> None:
    """Unregister the bridge in reverse order."""
    for module in reversed(modules):
        module.unregister()
