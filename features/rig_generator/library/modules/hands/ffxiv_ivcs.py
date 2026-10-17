"""Hands whose fingers have an additional IVCS tip bone."""

from . import _hand


class Module(_hand.Hands):
    name = "XIV-IVCS"
    requires = [
        "j_oya_a_r",
        "j_oya_b_r",
        "j_hito_a_r",
        "j_hito_b_r",
        "iv_hito_c_r",
        "j_naka_a_r",
        "j_naka_b_r",
        "iv_naka_c_r",
        "j_kusu_a_r",
        "j_kusu_b_r",
        "iv_kusu_c_r",
        "j_ko_a_r",
        "j_ko_b_r",
        "iv_ko_c_r",
        "j_oya_a_l",
        "j_oya_b_l",
        "j_hito_a_l",
        "j_hito_b_l",
        "iv_hito_c_l",
        "j_naka_a_l",
        "j_naka_b_l",
        "iv_naka_c_l",
        "j_kusu_a_l",
        "j_kusu_b_l",
        "iv_kusu_c_l",
        "j_ko_a_l",
        "j_ko_b_l",
        "iv_ko_c_l",
    ]
    has_tip_bones = True
