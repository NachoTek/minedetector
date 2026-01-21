"""
Game State Enumeration

Defines the three possible states of a Minesweeper game:
- PLAYING: Game is in progress, timer running, user can interact
- WON: All non-mine cells revealed, game won, timer stopped
- LOST: Mine clicked, game lost, timer stopped
"""

from enum import Enum


class GameState(Enum):
    """Enumeration representing the current state of a Minesweeper game."""

    PLAYING = "playing"
    """Game is in progress and accepting user input."""

    WON = "won"
    """Game has been won by revealing all non-mine cells."""

    LOST = "lost"
    """Game has been lost by clicking on a mine."""
