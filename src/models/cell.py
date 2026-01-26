"""
Cell Data Model

Represents a single cell in the Minedetector game board.
Each cell tracks its mine status, revealed state, flag state, and
    adjacent mine count.
"""

from dataclasses import dataclass


@dataclass
class Cell:
    """
    Represents a single cell on the Minedetector game board.

    Attributes:
        mine: Boolean indicating whether this cell contains a mine.
            Defaults to False.
        revealed: Boolean indicating whether this cell has been
            revealed by the player. Defaults to False.
        flagged: Boolean indicating whether this cell has been
            flagged by the player. Defaults to False.
        adjacent_mines: Integer count of mines in the 8 neighboring
            cells (0-8). Defaults to 0.
    """

    mine: bool = False
    """Is this cell a mine?"""

    revealed: bool = False
    """Has the user revealed this cell?"""

    flagged: bool = False
    """Has the user placed a flag on this cell?"""

    adjacent_mines: int = 0
    """Count of mines in the 8 neighboring cells (range: 0-8)."""
