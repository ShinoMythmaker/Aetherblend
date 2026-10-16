"""Hands whose fingers have an additional IVCS tip bone."""
from ._hand import Hands, required_bones, ui_collections


class Module(Hands):
    name = "XIV-IVCS"
    requires = required_bones(has_tip_bones=True)
    has_tip_bones = True
    ui_collections = ui_collections()
