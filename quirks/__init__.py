"""Eglo remote ZHA custom quirk package."""

from .eglo_ercu_3groups import EgloERCU3Groups
# Use 3-bank quirk with debug logging
from .eglo_ercu_awox_3banks import Awox99099Remote3Banks

__all__ = ["EgloERCU3Groups", "Awox99099Remote3Banks"]

