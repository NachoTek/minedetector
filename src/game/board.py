"""
Board Game Module

Manages the game board for Minesweeper, including the 2D grid of cells,
mine placement, and board-level operations.
"""

from typing import List
from src.models.cell import Cell
from src.models.game_state import GameState
from src.game import mine_placement
from src.game import adjacent_counter
from src.game import flood_fill
from src.game import chording


class Board:
    """
    Represents the Minesweeper game board as a 2D grid of Cell objects.

    The board manages all cells, handles coordinate validation, and provides
    access to individual cells for game logic operations.

    Attributes:
        rows: Integer number of rows in the grid (e.g., 9 for Beginner).
        cols: Integer number of columns in the grid (e.g., 9 for Beginner).
        mine_count: Total number of mines to be placed on the board.
        grid: 2D list (list of lists) of Cell objects. Access via grid[row][col].

    Example:
        >>> board = Board(9, 9, 10)  # Beginner difficulty
        >>> cell = board.grid[0][0]  # Access top-left cell
        >>> print(cell.mine, cell.revealed, cell.flagged)
        False False False
    """

    def __init__(self, rows: int, cols: int, mine_count: int):
        """
        Initialize a new Minesweeper board with the specified dimensions.

        Creates a 2D grid of Cell objects with all cells in their initial state:
        - mine: False (no mines placed yet)
        - revealed: False (all cells hidden)
        - flagged: False (no flags placed)
        - adjacent_mines: 0 (calculated after mine placement)

        Args:
            rows: Number of rows in the grid (must be positive).
            cols: Number of columns in the grid (must be positive).
            mine_count: Total number of mines to place on the board.

        Raises:
            ValueError: If rows, cols, or mine_count are negative.
        """
        if rows <= 0:
            raise ValueError(f"Rows must be positive, got {rows}")
        if cols <= 0:
            raise ValueError(f"Columns must be positive, got {cols}")
        if mine_count < 0:
            raise ValueError(f"Mine count must be non-negative, got {mine_count}")

        self.rows = rows
        """Number of rows in the game grid."""

        self.cols = cols
        """Number of columns in the game grid."""

        self.mine_count = mine_count
        """Total number of mines to be placed on the board."""

        # Initialize 2D grid with Cell objects
        # Using list comprehension for clean, efficient creation
        self.grid: List[List[Cell]] = [
            [Cell() for _ in range(cols)]
            for _ in range(rows)
        ]
        """2D list of Cell objects. Access via grid[row][col]."""

        # Initialize game state
        self.game_state = GameState.PLAYING
        """Current state of the game (PLAYING, WON, or LOST)."""

    def is_valid_coordinate(self, row: int, col: int) -> bool:
        """
        Check if the given coordinates are within the board boundaries.

        Args:
            row: Row index to check (0-based).
            col: Column index to check (0-based).

        Returns:
            True if coordinates are valid (within bounds), False otherwise.
        """
        return 0 <= row < self.rows and 0 <= col < self.cols

    def get_cell(self, row: int, col: int) -> Cell:
        """
        Get the cell at the specified coordinates.

        Args:
            row: Row index (0-based).
            col: Column index (0-based).

        Returns:
            The Cell object at the specified coordinates.

        Raises:
            IndexError: If coordinates are out of bounds.
        """
        if not self.is_valid_coordinate(row, col):
            raise IndexError(
                f"Coordinates ({row}, {col}) out of bounds "
                f"for board size ({self.rows}x{self.cols})"
            )
        return self.grid[row][col]

    def place_mines(self, first_click_row: int, first_click_col: int) -> None:
        """
        Place mines on the board, ensuring first-click safety.

        This method distributes mines randomly across the board while guaranteeing
        that the first-click cell and all 8 of its neighbors remain mine-free.
        This prevents the player from losing on their first click.

        The mine placement happens AFTER the first click, which is a key
        requirement for first-click safety. Mines are not placed during
        board initialization.

        Args:
            first_click_row: Row index of the first-click cell (0-based).
            first_click_col: Column index of the first-click cell (0-based).

        Raises:
            ValueError: If the first-click coordinates are out of bounds.
            ValueError: If mine_count exceeds available cells (accounting for protected zone).

        Example:
            >>> board = Board(9, 9, 10)
            >>> board.place_mines(4, 4)  # First click at center of board
            >>> # Cell (4,4) and its neighbors are guaranteed to be mine-free
        """
        # Validate first-click coordinates
        if not self.is_valid_coordinate(first_click_row, first_click_col):
            raise ValueError(
                f"First-click coordinates ({first_click_row}, {first_click_col}) "
                f"out of bounds for board size ({self.rows}x{self.cols})"
            )

        # Delegate to mine_placement module
        mine_placement.place_mines(
            self.grid,
            self.rows,
            self.cols,
            self.mine_count,
            first_click_row,
            first_click_col
        )

        # Calculate adjacent mine counts for all cells
        adjacent_counter.calculate_adjacent_mines(self.grid, self.rows, self.cols)

    def reveal_cell(self, row: int, col: int) -> None:
        """
        Reveal a cell and perform flood fill if it has 0 adjacent mines.

        When a cell with 0 adjacent mines is revealed, this method automatically
        reveals all its neighbors. If any of those neighbors also have 0 adjacent
        mines, the flood fill continues recursively through those cells.

        The flood fill stops at cells with adjacent mines > 0, revealing them but
        not continuing past them. This uses an iterative stack-based approach to
        avoid stack overflow on large boards (e.g., Expert with 480 cells).

        Args:
            row: Row index of the cell to reveal (0-based).
            col: Column index of the cell to reveal (0-based).

        Raises:
            IndexError: If coordinates are out of bounds.

        Example:
            >>> board = Board(9, 9, 10)
            >>> board.place_mines(4, 4)
            >>> board.reveal_cell(4, 4)
            >>> # If cell (4,4) has 0 adjacent mines, flood fill reveals connected region
        """
        # Delegate to flood_fill module
        flood_fill.reveal_cell(self.grid, row, col, self.rows, self.cols)

    def chord_cell(self, row: int, col: int) -> None:
        """
        Perform chording on a revealed numbered cell.

        Chording is a Minesweeper mechanic where clicking on a revealed numbered cell
        will automatically reveal all its unflagged neighbors, but only if the number
        of flagged neighbors exactly equals the cell's adjacent mine count.

        This allows experienced players to quickly reveal regions they've already
        solved logically. If the flag count doesn't match, nothing happens.

        Args:
            row: Row index of the cell to chord (0-based).
            col: Column index of the cell to chord (0-based).

        Raises:
            IndexError: If coordinates are out of bounds.

        Example:
            >>> board = Board(9, 9, 10)
            >>> board.place_mines(4, 4)
            >>> board.reveal_cell(4, 4)  # Reveal a cell with number '2'
            >>> board.grid[3][3].flagged = True  # Flag 2 neighbors
            >>> board.grid[3][4].flagged = True
            >>> board.chord_cell(4, 4)  # Reveal remaining neighbors
        """
        # Delegate to chording module
        chording.chord_cell(self.grid, row, col, self.rows, self.cols)

    def is_won(self) -> bool:
        """
        Check if the game has been won.

        A game is won when all non-mine cells have been revealed. This method
        counts the number of revealed cells and compares it to the total number
        of non-mine cells (total cells - mine_count).

        Returns:
            True if all non-mine cells are revealed (game is won), False otherwise.

        Example:
            >>> board = Board(9, 9, 10)  # 81 cells, 10 mines = 71 safe cells
            >>> board.place_mines(4, 4)
            >>> # Reveal all 71 safe cells...
            >>> board.is_won()
            True
        """
        # Count total cells that should be revealed to win
        total_cells = self.rows * self.cols
        safe_cells = total_cells - self.mine_count

        # Count currently revealed cells
        revealed_count = sum(
            1 for row in self.grid
            for cell in row
            if cell.revealed
        )

        # Win condition: all safe cells are revealed
        return revealed_count == safe_cells

    def is_lost(self) -> bool:
        """
        Check if the game has been lost.

        A game is lost when any mine cell has been revealed. This method checks
        all mine cells to see if any of them have been revealed by the player.

        Returns:
            True if any mine has been revealed (game is lost), False otherwise.

        Example:
            >>> board = Board(9, 9, 10)
            >>> board.place_mines(4, 4)
            >>> board.reveal_cell(0, 0)  # Accidentally reveal a mine
            >>> board.is_lost()
            True
        """
        # Check if any mine cell has been revealed
        return any(
            cell.mine and cell.revealed
            for row in self.grid
            for cell in row
        )

    def update_game_state(self) -> None:
        """
        Update the game state based on current board conditions.

        This method checks for win or loss conditions and updates the game_state
        attribute accordingly. If the game is already in a terminal state (WON or
        LOST), this method does nothing to prevent changing the state back to
        PLAYING.

        The checks are performed in this order:
        1. Loss: If any mine is revealed, set state to LOST
        2. Win: If all non-mine cells are revealed, set state to WON
        3. Otherwise: Keep state as PLAYING

        Once the game enters a terminal state (WON or LOST), it cannot return to
        PLAYING. A new board must be created to play again.

        Example:
            >>> board = Board(9, 9, 10)
            >>> board.place_mines(4, 4)
            >>> board.reveal_cell(4, 4)
            >>> board.update_game_state()
            >>> print(board.game_state)
            GameState.PLAYING
            >>> # Reveal all remaining safe cells...
            >>> board.update_game_state()
            >>> print(board.game_state)
            GameState.WON
        """
        # If already in terminal state, don't change it
        if self.game_state == GameState.WON or self.game_state == GameState.LOST:
            return

        # Check for loss first (mine revealed)
        if self.is_lost():
            self.game_state = GameState.LOST
            return

        # Check for win (all safe cells revealed)
        if self.is_won():
            self.game_state = GameState.WON
            return

        # Game continues
        self.game_state = GameState.PLAYING
