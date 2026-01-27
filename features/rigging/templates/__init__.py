from ....core.shared import AetherRigGenerator, WidgetOverride
from ....core.rigify import *


from .colorsets import *
from .ui_collections import *
from .widget_overrides import *
from .bone_groups import *


## Templates
TEMPLATES = {
    'Player SFW':   AetherRigGenerator (
        name = "Player SFW",
        color_sets=[CS_AETHER_BLEND],
        ui_collections=[UI_PLAYER_SFW],  
        widget_overrides=[WO_DEFAULT],
        bone_groups = [BG_PLAYER_SFW]
    ),
    'Player SFW (IVCS)': AetherRigGenerator(
        name= "Player SFW (IVCS)",
        color_sets=[CS_AETHER_BLEND],
        ui_collections=[UI_PLAYER_SFW_IV],  
        widget_overrides=[WO_DEFAULT],
        bone_groups = [BG_PLAYER_SFW_IV]
    ),
}