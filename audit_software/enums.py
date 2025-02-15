"""Enumerators used across the modules."""
from enum import Enum


class KeyAction(Enum):
    NONE = 0
    QUIT = 1
    CLEAR_LABELS = 2
    SAVE_IMAGE = 3
