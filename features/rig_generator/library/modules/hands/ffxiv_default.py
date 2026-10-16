"""Hands with two bones per finger."""

from . import _hand


class Module(_hand.Hands):
    name = "XIV-Default"
    requires = [
        "j_oya_a_r",
        "j_oya_b_r",
        "j_hito_a_r",
        "j_hito_b_r",
        "j_naka_a_r",
        "j_naka_b_r",
        "j_kusu_a_r",
        "j_kusu_b_r",
        "j_ko_a_r",
        "j_ko_b_r",
        "j_oya_a_l",
        "j_oya_b_l",
        "j_hito_a_l",
        "j_hito_b_l",
        "j_naka_a_l",
        "j_naka_b_l",
        "j_kusu_a_l",
        "j_kusu_b_l",
        "j_ko_a_l",
        "j_ko_b_l",
    ]
    ui_collections = _hand.ui_collections()
