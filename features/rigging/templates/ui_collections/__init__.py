from .ui_player_sfw import UI_PLAYER_SFW
from .ui_player_sfw_ivcs import UI_PLAYER_SFW_IV

UI_COLLECTIONS = {
    "Player SFW": UI_PLAYER_SFW,
    "Player SFW (IVCS)": UI_PLAYER_SFW_IV
    }


__all__ = ['UI_COLLECTIONS', 'UI_PLAYER_SFW', 'UI_PLAYER_SFW_IV']