from ....core.shared import AetherRigGenerator, Template ,WidgetOverride
from ....core.rigify import *


from .colorsets import *
from .ui_collections import *
from .overrides import *

from .modules import *


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