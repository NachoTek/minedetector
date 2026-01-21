"""
Flood Fill Module

Implements an iterative flood fill algorithm to reveal connected blank regions
when a cell with 0 adjacent mines is clicked.
"""

from typing import List, Tuple
from src.models.cell import Cell


def reveal_cell(grid: List[List[Cell]], row: int, col: int, rows: int, cols: int) -> None:
    """
    Reveal a cell and perform flood fill if it has 0 adjacent mines.

    When a cell with 0 adjacent mines is revealed, this function automatically
    reveals all its neighbors. If any of those neighbors also have 0 adjacent
    mines, the flood fill continues recursively through those cells. This process
    uses an iterative stack-based approach to avoid stack overflow on large boards.

    The flood fill stops at cells with adjacent mines > 0, revealing them but
    not continuing past them.

    Args:
        grid: 2D list of Cell objects representing the game board.
        row: Row index of the cell to reveal (0-based).
        col: Column index of the cell to reveal (0-based).
        rows: Number of rows in the grid.
        cols: Number of columns in the grid.

    Raises:
        IndexError: If coordinates are out of bounds.

    Example:
        >>> board = Board(9, 9, 10)
        >>> board.place_mines(4, 4)
        >>> reveal_cell(board.grid, 4, 4, board.rows, board.cols)
        >>> # If cell (4,4) has 0 adjacent mines, flood fill reveals connected region
    """
    # Validate coordinates
    if not (0 <= row < rows and 0 <= col < cols):
        raise IndexError(
            f"Coordinates ({row}, {col}) out of bounds "
            f"for board size ({rows}x{cols})"
        )

    # If cell is already revealed or flagged, do nothing
    if grid[row][col].revealed or grid[row][col].flagged:
        return

    # Use stack-based iteration to avoid recursion depth issues
    stack: List[Tuple[int, int]] = [(row, col)]

    while stack:
        current_row, current_col = stack.pop()

        # Skip if out of bounds (safety check)
        if not (0 <= current_row < rows and 0 <= current_col < cols):
            continue

        current_cell = grid[current_row][current_col]

        # Skip if already revealed or flagged
        if current_cell.revealed or current_cell.flagged:
            continue

        # Reveal the current cell
        current_cell.revealed = True

        # If cell has adjacent mines, stop here (don't add neighbors to stack)
        if current_cell.adjacent_mines > 0:
            continue

        # Cell has 0 adjacent mines, add all 8 neighbors to stack
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                # Skip the cell itself
                if dr == 0 and dc == 0:
                    continue

                neighbor_row = current_row + dr
                neighbor_col = current_col + dc

                # Only add valid neighbors within bounds
                if 0 <= neighbor_row < rows and 0 <= neighbor_col < cols:
                    neighbor_cell = grid[neighbor_row][neighbor_col]

                    # Only add unrevealed, unflagged cells to stack
                    if not neighbor_cell.revealed and not neighbor_cell.flagged:
                        stack.append((neighbor_row, neighbor_col))
