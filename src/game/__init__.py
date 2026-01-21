"""
Game Logic Package

Contains core game mechanics including:
- Board: Game board management
- Flood fill algorithm for revealing cells
- Chording mechanic for fast revealing
- Mine placement with first-click safety
- Adjacent mine counting
"""

from .board import Board

__all__ = ['Board']
