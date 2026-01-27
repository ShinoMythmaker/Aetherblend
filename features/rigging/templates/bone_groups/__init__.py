from .bg_player_sfw import BG_PLAYER_SFW
from .bg_player_sfw_iv import BG_PLAYER_SFW_IV

BG_GROUPS = {
    "Player SFW": BG_PLAYER_SFW,
    "Player SFW (IVCS)": BG_PLAYER_SFW_IV
}


__all__ = ['BG_GROUPS', 'BG_PLAYER_SFW', 'BG_PLAYER_SFW_IV']