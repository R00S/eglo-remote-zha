"""Eglo remote ZHA custom quirk package."""

from .eglo_ercu_3groups import EgloERCU3Groups
# Use basic quirk - 3-bank via multiple automations
from .eglo_ercu_awox import Awox99099Remote

__all__ = ["EgloERCU3Groups", "Awox99099Remote"]


