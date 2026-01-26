from ....core.shared import AetherRigGenerator, WidgetOverride
from ....core.rigify import *


from .colorsets import *
from .ui_collections import *
from .widget_overrides import *
from .bone_groups import *

## UI Selections
UI_COLLECTIONS = {"Player SFW": UI_PLAYER_SFW}
WO_OVERRIDES = {"Default": WO_DEFAULT}
BG_GROUPS = {"Player SFW": BG_PLAYER_SFW}


HUMAN = AetherRigGenerator (
    name = "Human Rig",
    color_sets=[CS_AETHER_BLEND],
    ui_collections=[UI_PLAYER_SFW],  
    widget_overrides=[WO_DEFAULT],
    bone_groups = [BG_PLAYER_SFW]
)