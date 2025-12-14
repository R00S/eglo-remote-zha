"""Eglo remote ZHA custom quirk package."""

from .eglo_ercu_3groups import EgloERCU3Groups
# Testing 3-bank with enhanced debug logging
from .eglo_ercu_awox_3banks import Awox99099Remote3Banks

__all__ = ["EgloERCU3Groups", "Awox99099Remote3Banks"]


