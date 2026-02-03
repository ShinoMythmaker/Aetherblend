from .cs_aetherblend import CS_AETHER_BLEND
from .cs_rigify import CS_RIGIFY
from  .cs_autorigpro import CS_ARG

CS_COLORSETS = {
    "AetherBlend": CS_AETHER_BLEND, 
    "Rigify": CS_RIGIFY,
    "Autorig Pro": CS_ARG
    }

__all__ = ['CS_COLORSETS','CS_AETHER_BLEND', 'CS_RIGIFY', 'CS_ARG']