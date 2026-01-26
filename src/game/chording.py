"""
Chording Module

Implements the chording mechanic where clicking a revealed numbered cell
reveals all unflagged neighbors when the flag count matches the cell's number.
"""

from typing import List

from src.game import flood_fill
from src.models.cell import Cell


def chord_cell(
    grid: List[List[Cell]], row: int, col: int, rows: int, cols: int
) -> None:
    """
    Perform chording on a revealed numbered cell.

    Chording is a Minedetector mechanic where clicking on a revealed numbered cell
    will automatically reveal all its unflagged neighbors, but only if the number
    of flagged neighbors exactly equals the cell's adjacent mine count. This allows
    experienced players to quickly reveal regions they've already solved logically.

    If the flag count doesn't match the cell's number, this function does nothing,
    allowing the player to continue playing without penalty for incorrect attempts.

    Args:
        grid: 2D list of Cell objects representing the game board.
        row: Row index of the cell to chord (0-based).
        col: Column index of the cell to chord (0-based).
        rows: Number of rows in the grid.
        cols: Number of columns in the grid.

    Raises:
        IndexError: If coordinates are out of bounds.

    Example:
        >>> board = Board(9, 9, 10)
        >>> board.place_mines(4, 4)
        >>> # Reveal a cell with number '2', flag 2 neighbors
        >>> board.grid[4][4].revealed = True
        >>> board.grid[3][3].flagged = True
        >>> board.grid[3][4].flagged = True
        >>> # Chording reveals remaining unflagged neighbors
        >>> chord_cell(board.grid, 4, 4, board.rows, board.cols)
    """
    # Validate coordinates
    if not (0 <= row < rows and 0 <= col < cols):
        raise IndexError(
            f"Coordinates ({row}, {col}) out of bounds "
            f"for board size ({rows}x{cols})"
        )

    cell = grid[row][col]

    # Chording only works on revealed numbered cells
    # Must be revealed AND have adjacent mines > 0
    if not cell.revealed or cell.adjacent_mines == 0:
        return

    # Count flagged neighbors
    flag_count = _count_flagged_neighbors(grid, row, col, rows, cols)

    # Only reveal neighbors if flag count matches the cell's number
    if flag_count != cell.adjacent_mines:
        return

    # Reveal all unflagged neighbors
    _reveal_unflagged_neighbors(grid, row, col, rows, cols)


def _count_flagged_neighbors(
    grid: List[List[Cell]], row: int, col: int, rows: int, cols: int
) -> int:
    """
    Count the number of flagged cells in the 8 neighboring cells.

    Args:
        grid: 2D list of Cell objects representing the game board.
        row: Row index of the cell to check neighbors for (0-based).
        col: Column index of the cell to check neighbors for (0-based).
        rows: Number of rows in the grid.
        cols: Number of columns in the grid.

    Returns:
        Integer count of flagged cells in the 8 neighboring cells (range: 0-8).

    Example:
        >>> # For a cell at (4, 4) with 2 flagged neighbors
        >>> _count_flagged_neighbors(grid, 4, 4, 9, 9)
        2
    """
    flag_count = 0

    # Check all 8 directions around the cell
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            # Skip the cell itself (dr=0, dc=0)
            if dr == 0 and dc == 0:
                continue

            # Calculate neighbor coordinates
            neighbor_row = row + dr
            neighbor_col = col + dc

            # Only count if neighbor is within bounds
            if 0 <= neighbor_row < rows and 0 <= neighbor_col < cols:
                if grid[neighbor_row][neighbor_col].flagged:
                    flag_count += 1

    return flag_count


def _reveal_unflagged_neighbors(
    grid: List[List[Cell]], row: int, col: int, rows: int, cols: int
) -> None:
    """
    Reveal all unflagged neighbors of a cell.

    This function iterates through all 8 neighbors of the given cell and
    reveals any that are not flagged. It uses the flood_fill module to
    reveal each neighbor, which handles the flood fill mechanic for cells
    with 0 adjacent mines.

    Args:
        grid: 2D list of Cell objects representing the game board.
        row: Row index of the cell whose neighbors should be revealed (0-based).
        col: Column index of the cell whose neighbors should be revealed (0-based).
        rows: Number of rows in the grid.
        cols: Number of columns in the grid.

    Example:
        >>> # Reveal all unflagged neighbors of cell (4, 4)
        >>> _reveal_unflagged_neighbors(grid, 4, 4, 9, 9)
    """
    # Check all 8 directions around the cell
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            # Skip the cell itself (dr=0, dc=0)
            if dr == 0 and dc == 0:
                continue

            # Calculate neighbor coordinates
            neighbor_row = row + dr
            neighbor_col = col + dc

            # Only reveal if neighbor is within bounds
            if 0 <= neighbor_row < rows and 0 <= neighbor_col < cols:
                neighbor_cell = grid[neighbor_row][neighbor_col]

                # Only reveal unflagged cells
                if not neighbor_cell.flagged:
                    # Use flood_fill to handle flood fill for blank cells
                    # and simple reveal for numbered cells
                    flood_fill.reveal_cell(grid, neighbor_row, neighbor_col, rows, cols)
