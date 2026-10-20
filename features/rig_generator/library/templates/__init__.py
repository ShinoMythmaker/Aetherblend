from .ffxiv import FFXIV

DEFAULT_TEMPLATE_NAME = FFXIV.name

TEMPLATES = {template.name: template for template in (FFXIV,)}

__all__ = ["TEMPLATES", "DEFAULT_TEMPLATE_NAME", "FFXIV"]
