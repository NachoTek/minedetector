"""
Adjacent Mine Counter Module

Calculates the number of mines in the 8 neighboring cells for each cell
on the game board. This information is displayed to the player as numbers 1-8.
"""

from typing import List

from src.models.cell import Cell


def calculate_adjacent_mines(grid: List[List[Cell]], rows: int, cols: int) -> None:
    """
    Calculate and store the adjacent mine count for every cell on the board.

    For each cell in the grid, this function counts how many mines are present
    in its 8 neighboring cells (horizontal, vertical, and diagonal). The count
    is stored in the cell's adjacent_mines attribute, which is later displayed
    to the player when the cell is revealed.

    Edge and corner cells have fewer than 8 neighbors, so their maximum
    possible count is lower (e.g., corner cells max is 3, edge cells max is 5).

    This function modifies the grid in-place by updating each cell's
    adjacent_mines attribute.

    Args:
        grid: 2D list of Cell objects representing the game board.
        rows: Number of rows in the grid.
        cols: Number of columns in the grid.

    Example:
        >>> board = Board(9, 9, 10)
        >>> board.place_mines(4, 4)  # Place mines
        >>> calculate_adjacent_mines(board.grid, board.rows, board.cols)
        >>> # Now each cell has its adjacent mine count calculated
    """
    # Iterate through every cell in the grid
    for row in range(rows):
        for col in range(cols):
            # Count mines in the 8 neighbors of this cell
            adjacent_count = _count_neighbor_mines(grid, row, col, rows, cols)

            # Store the count in the cell
            grid[row][col].adjacent_mines = adjacent_count


def _count_neighbor_mines(
    grid: List[List[Cell]], row: int, col: int, rows: int, cols: int
) -> int:
    """
    Count the number of mines in the 8 neighboring cells.

    Checks all 8 cells surrounding the given cell (horizontal, vertical,
    and diagonal neighbors). Only counts mines in cells that are within
    the board boundaries.

    Args:
        grid: 2D list of Cell objects representing the game board.
        row: Row index of the cell to check neighbors for (0-based).
        col: Column index of the cell to check neighbors for (0-based).
        rows: Number of rows in the grid.
        cols: Number of columns in the grid.

    Returns:
        Integer count of mines in the 8 neighboring cells (range: 0-8).

    Example:
        >>> # For a cell at (4, 4) with mines at (4, 3) and (5, 5)
        >>> _count_neighbor_mines(grid, 4, 4, 9, 9)
        2
    """
    mine_count = 0

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
                if grid[neighbor_row][neighbor_col].mine:
                    mine_count += 1

    return mine_count
