from . import panels, stream, properties

"""Customize+ feature: parse, apply, and revert character bone transforms."""

__all__ = ["panels", "properties", "stream"]

modules = (panels, stream, properties)


def register() -> None:
    """Register the C+ feature."""
    for mod in modules:
        mod.register()

def unregister() -> None:
    """Unregister the C+ feature."""
    for mod in reversed(modules):
        mod.unregister()