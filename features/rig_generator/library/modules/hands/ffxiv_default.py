"""Hands with two bones per finger."""

from ._hand import Hands, required_bones, ui_collections


class Module(Hands):
    name = "XIV-Default"
    requires = required_bones(has_tip_bones=False)
    ui_collections = ui_collections()
