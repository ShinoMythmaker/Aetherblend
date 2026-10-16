"""Rig module 'hands' and its variants."""

from .ffxiv_default import Module as ffxiv_default
from .ffxiv_ivcs import Module as ffxiv_ivcs

__all__ = ["ffxiv_default", "ffxiv_ivcs"]
