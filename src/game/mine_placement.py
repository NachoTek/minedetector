"""
Mine Placement Module

Handles the random placement of mines on the game board with first-click safety.
The first-click cell and its neighbors are guaranteed to be mine-free.
"""

import random
from typing import List, Tuple

from src.models.cell import Cell


def place_mines(
    grid: List[List[Cell]],
    rows: int,
    cols: int,
    mine_count: int,
    first_click_row: int,
    first_click_col: int,
) -> None:
    """
    Place mines randomly on the board, ensuring the first-click cell is safe.

    This function randomly distributes mines across the board while guaranteeing
    that the first-click cell and all 8 of its neighbors remain mine-free. This
    implements the first-click safety feature that prevents the player from
    losing on their very first click.

    The function uses a while loop to randomly select coordinates and place mines,
    skipping cells that already have mines or are in the protected zone around
    the first-click cell.

    Args:
        grid: 2D list of Cell objects representing the game board.
        rows: Number of rows in the grid.
        cols: Number of columns in the grid.
        mine_count: Total number of mines to place on the board.
        first_click_row: Row index of the first-click cell (0-based).
        first_click_col: Column index of the first-click cell (0-based).

    Raises:
        ValueError: If mine_count exceeds the number of available cells (excluding
                    the protected zone around first-click).

    Example:
        >>> board = Board(9, 9, 10)
        >>> place_mines(
        >>>     board.grid, board.rows, board.cols, board.mine_count, 4, 4
        >>> )
        >>> # Now board has 10 mines placed, with cell (4,4) and
        >>> # neighbors guaranteed safe
    """
    # Validate that we have enough space to place mines
    # Protected zone includes first-click cell and its 8 neighbors
    protected_cells = _get_protected_zone(first_click_row, first_click_col, rows, cols)
    available_cells = (rows * cols) - len(protected_cells)

    if mine_count > available_cells:
        raise ValueError(
            f"Cannot place {mine_count} mines with only {available_cells} "
            f"available cells (protected zone: {len(protected_cells)} cells)"
        )

    mines_placed = 0

    # Continue placing mines until we reach the required count
    while mines_placed < mine_count:
        # Generate random coordinates
        row = random.randint(0, rows - 1)
        col = random.randint(0, cols - 1)

        # Skip if this cell already has a mine
        if grid[row][col].mine:
            continue

        # Skip if this cell is in the protected zone (first-click or neighbors)
        if (row, col) in protected_cells:
            continue

        # Place mine at this location
        grid[row][col].mine = True
        mines_placed += 1


def _get_protected_zone(
    first_click_row: int, first_click_col: int, rows: int, cols: int
) -> List[Tuple[int, int]]:
    """
    Get the list of cells that must be kept mine-free (first-click and neighbors).

    The protected zone consists of the first-click cell and all 8 of its
    neighboring cells. Neighbors are defined using the 8-directional movement
    pattern (horizontal, vertical, and diagonal).

    Args:
        first_click_row: Row index of the first-click cell (0-based).
        first_click_col: Column index of the first-click cell (0-based).
        rows: Number of rows in the grid.
        cols: Number of columns in the grid.

    Returns:
        List of (row, col) tuples representing all protected cells.
        All coordinates are within board bounds.

    Example:
        >>> _get_protected_zone(4, 4, 9, 9)
        [(3, 3), (3, 4), (3, 5), (4, 3), (4, 4), (4, 5), (5, 3), (5, 4), (5, 5)]
    """
    protected = []

    # Check all 8 directions around the first-click cell
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            row = first_click_row + dr
            col = first_click_col + dc

            # Only add coordinates that are within bounds
            if 0 <= row < rows and 0 <= col < cols:
                protected.append((row, col))

    return protected
