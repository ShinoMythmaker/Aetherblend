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
        color_sets=['Aether Blend', 'Rigify'],
        ui_collections=['Player SFW'],  
        widget_overrides=['Default'],
        bone_groups = ['Player SFW']
    )
}