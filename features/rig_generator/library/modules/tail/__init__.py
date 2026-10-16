"""Rig module 'tail' and its variants."""

from .ffxiv_fk import Module as ffxiv_fk
from .ffxiv_spline import Module as ffxiv_spline

__all__ = ["ffxiv_fk", "ffxiv_spline"]
