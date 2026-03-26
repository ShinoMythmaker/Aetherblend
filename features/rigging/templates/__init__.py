from ....core.shared import AetherRigGenerator, WidgetOverride
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
    'Player SFW':   AetherRigGenerator (
        name = "Player SFW",
        color_sets=[CS_AETHER_BLEND],
        ui_collections=[UI_PLAYER_SFW],  
        overrides=[WO_DEFAULT, PO_DEFAULT],
        modules = [spine.default, arms.default, legs.default, skirt.default, hands.default, tail.default, face.detailed, ears.miqo, ears.viera, hair.default]
    ),
    'Player SFW (IVCS)': AetherRigGenerator(
        name= "Player SFW (IVCS)",
        color_sets=[CS_AETHER_BLEND],
        ui_collections=[UI_PLAYER_SFW_IV],  
        overrides=[WO_DEFAULT, PO_DEFAULT],
        modules = [spine.default, arms.default, legs.default, skirt.default, hands.ivcs, toes.ivcs, tail.default, face.detailed, ears.miqo, ears.viera, hair.default]
    ),
    'Player NSFW (IVCS)': AetherRigGenerator(
        name= "Player NSFW (IVCS)",
        color_sets=[CS_AETHER_BLEND],
        ui_collections=[UI_PLAYER_NSFW_IV],  
        overrides=[WO_NSFW, PO_DEFAULT],
        modules = [spine.default, arms.default, legs.default, skirt.default, hands.ivcs, toes.ivcs, tail.default, face.detailed, ears.miqo, ears.viera, hair.default, genitals.ivcs_both]
    ),
}