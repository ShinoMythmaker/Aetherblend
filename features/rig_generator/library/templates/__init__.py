from .ffxiv_default import FFXIV_DEFAULT
from .ffxiv_pre_dt import FFXIV_PRE_DT

DEFAULT_TEMPLATE_NAME = FFXIV_DEFAULT.name

TEMPLATES = {template.name: template for template in (FFXIV_DEFAULT, FFXIV_PRE_DT)}

__all__ = ['TEMPLATES', 'DEFAULT_TEMPLATE_NAME', 'FFXIV_DEFAULT', 'FFXIV_PRE_DT']
