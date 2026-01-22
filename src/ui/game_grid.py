"""
Game Grid Module

Creates and manages the grid of clickable cell buttons for the Minesweeper game.
Handles mouse interactions and updates cell display based on game state.
"""

import tkinter as tk
from typing import Callable, Optional
from src.game.board import Board


class GameGrid:
    """
    Manages the visual grid of cell buttons for the Minesweeper game.

    This class creates a 2D grid of Tkinter buttons representing each cell
    in the game board. It handles left-click (reveal) and right-click (flag)
    interactions, and updates the visual appearance of cells based on their
    state.

    The grid uses Tkinter's grid layout manager for perfect alignment of cells.
    Each cell button is sized to be square with the standard Windows Minesweeper
    appearance (raised border for unrevealed, sunken for revealed).

    Attributes:
        parent: The parent Tkinter widget (usually the main window).
        board: The game Board object containing cell data.
        cell_size: The size of each cell button in pixels (default: 30).
        buttons: 2D list of Tkinter button widgets indexed by [row][col].
        on_cell_click: Optional callback function for left-click events.
        on_cell_right_click: Optional callback function for right-click events.

    Example:
        >>> grid = GameGrid(parent_window, board, on_cell_click=my_callback)
        >>> grid.update_all_cells()  # Refresh display after board state changes
    """

    # Windows Minesweeper number colors (1-8)
    NUMBER_COLORS = {
        1: "blue",
        2: "green",
        3: "red",
        4: "dark blue",
        5: "#800000",  # Dark brown/maroon
        6: "teal",
        7: "black",
        8: "gray"
    }
    """Colors for numbers 1-8 matching the classic Windows Minesweeper appearance."""

    def __init__(
        self,
        parent: tk.Widget,
        board: Board,
        cell_size: int = 30,
        on_cell_click: Optional[Callable[[int, int], None]] = None,
        on_cell_right_click: Optional[Callable[[int, int], None]] = None
    ):
        """
        Initialize the game grid with clickable cell buttons.

        Creates a grid of Tkinter buttons matching the board dimensions.
        Each button is configured with square dimensions and bound to
        mouse click event handlers.

        Args:
            parent: The parent Tkinter widget to contain the grid.
            board: The game Board object with cell data to display.
            cell_size: Size of each cell button in pixels (default: 30).
            on_cell_click: Optional callback for left-click, receives (row, col).
            on_cell_right_click: Optional callback for right-click, receives (row, col).

        Raises:
            ValueError: If board is None or cell_size is not positive.
        """
        if board is None:
            raise ValueError("Board cannot be None")
        if cell_size <= 0:
            raise ValueError(f"Cell size must be positive, got {cell_size}")

        self.parent = parent
        """The parent Tkinter widget containing this grid."""

        self.board = board
        """The game Board object containing cell data."""

        self.cell_size = cell_size
        """The size of each cell button in pixels."""

        self.on_cell_click = on_cell_click
        """Optional callback function for left-click events on cells."""

        self.on_cell_right_click = on_cell_right_click
        """Optional callback function for right-click events on cells."""

        # Get root window for scheduling deferred updates
        self.root = parent.winfo_toplevel()
        """The root Tkinter window for scheduling deferred updates."""

        # Create frame to hold the grid
        self.frame = tk.Frame(parent, relief="sunken", bd=2)
        """The frame widget containing the grid of cell buttons."""

        # Initialize buttons storage
        self.buttons: list[list[tk.Button]] = []
        """2D list of Tkinter button widgets indexed by [row][col]."""

        # Create the grid of buttons
        self._create_grid()

    def _create_grid(self) -> None:
        """
        Create the 2D grid of clickable cell buttons.

        This method generates a button for each cell in the board using
        Tkinter's grid layout manager. Each button is configured with:
        - Square dimensions (cell_size x cell_size)
        - Raised relief for unrevealed appearance
        - Event bindings for left-click and right-click
        - Closure to capture row/col coordinates for callbacks

        The buttons are stored in a 2D list for efficient access during updates.
        """
        # Clear existing buttons if any
        self.buttons = []

        # Create buttons for each cell
        for row in range(self.board.rows):
            button_row = []
            for col in range(self.board.cols):
                # Create button with closure to capture row/col
                button = tk.Button(
                    self.frame,
                    width=2,
                    height=1,
                    relief="raised",
                    bd=2,
                    font=("Arial", 10, "bold")
                )

                # Bind mouse events
                # Use ButtonRelease-1 to allow button to show depressed state before updating
                button.bind(
                    "<ButtonRelease-1>",
                    lambda event, r=row, c=col: self._handle_left_click(r, c)
                )
                button.bind(
                    "<ButtonRelease-3>",
                    lambda event, r=row, c=col: self._handle_right_click(r, c)
                )

                # Position button in grid
                button.grid(row=row, column=col, padx=0, pady=0)

                button_row.append(button)
            self.buttons.append(button_row)

    def _handle_left_click(self, row: int, col: int) -> None:
        """
        Handle left-click event on a cell button.

        This method is called when a cell button is left-clicked. It invokes
        the on_cell_click callback if one was provided during initialization.

        Args:
            row: Row index of the clicked cell (0-based).
            col: Column index of the clicked cell (0-based).
        """
        if self.on_cell_click:
            self.on_cell_click(row, col)

    def _handle_right_click(self, row: int, col: int) -> None:
        """
        Handle right-click event on a cell button.

        This method is called when a cell button is right-clicked. It invokes
        the on_cell_right_click callback if one was provided during initialization.
        Right-click is used to place/remove flags on cells.

        Args:
            row: Row index of the clicked cell (0-based).
            col: Column index of the clicked cell (0-based).
        """
        if self.on_cell_right_click:
            self.on_cell_right_click(row, col)

    def update_cell(self, row: int, col: int) -> None:
        """
        Update the visual appearance of a single cell.

        Refreshes the display of the specified cell button based on its current
        state in the board. This handles all possible cell states:
        - Unrevealed: Raised button with no text
        - Revealed mine: Sunken button with mine symbol
        - Revealed numbered: Sunken button with number (1-8) in appropriate color
        - Flagged: Raised button with flag symbol

        Args:
            row: Row index of the cell to update (0-based).
            col: Column index of the cell to update (0-based).

        Raises:
            IndexError: If coordinates are out of bounds.
        """
        if not self.board.is_valid_coordinate(row, col):
            raise IndexError(
                f"Cannot update cell ({row}, {col}): "
                f"out of bounds for board size ({self.board.rows}x{self.board.cols})"
            )

        cell = self.board.get_cell(row, col)
        button = self.buttons[row][col]

        if cell.flagged:
            # Show flag
            button.config(
                text="🚩",
                relief="raised",
                bg="lightgray"
            )
        elif cell.revealed:
            if cell.mine:
                # Revealed mine - show mine symbol
                button.config(
                    text="💣",
                    relief="sunken",
                    bg="#c0c0c0"
                )
            elif cell.adjacent_mines > 0:
                # Revealed numbered cell - show number with color
                button.config(
                    text=str(cell.adjacent_mines),
                    relief="sunken",
                    bg="#c0c0c0",
                    fg=self.NUMBER_COLORS.get(cell.adjacent_mines, "black")
                )
            else:
                # Revealed blank cell (0 adjacent mines)
                button.config(
                    text="",
                    relief="sunken",
                    bg="#c0c0c0"
                )
        else:
            # Unrevealed cell
            button.config(
                text="",
                relief="raised",
                bg="lightgray"
            )

    def update_cell_deferred(self, row: int, col: int) -> None:
        """
        Update the visual appearance of a single cell after event processing completes.

        This method schedules a cell update to happen after Tkinter finishes processing
        the current event. This is necessary to ensure that the button's visual state
        (e.g., sunken relief for revealed cells) is applied AFTER Tkinter's default
        button event handling completes, which would otherwise reset the button state.

        Use this method for clicked cells to ensure their "sunken" state persists
        after button release events.

        Args:
            row: Row index of the cell to update (0-based).
            col: Column index of the cell to update (0-based).

        Raises:
            IndexError: If coordinates are out of bounds.
        """
        if not self.board.is_valid_coordinate(row, col):
            raise IndexError(
                f"Cannot update cell ({row}, {col}): "
                f"out of bounds for board size ({self.board.rows}x{self.board.cols})"
            )

        # Schedule the update to happen after Tkinter finishes processing
        # the current button release event. This ensures our visual state
        # (sunken relief for revealed cells) is applied AFTER Tkinter's
        # default button behavior tries to reset it to raised.
        self.root.after(0, lambda: self.update_cell(row, col))

    def update_all_cells(self) -> None:
        """
        Update the visual appearance of all cells in the grid.

        This method iterates through all cells and refreshes their display
        based on the current board state. Use this after batch operations
        that affect multiple cells (e.g., flood fill reveal, game over).
        """
        for row in range(self.board.rows):
            for col in range(self.board.cols):
                self.update_cell(row, col)

    def resize(self, new_board: Board) -> None:
        """
        Resize the grid to match a new board configuration.

        This method destroys all existing buttons and recreates the grid
        with the dimensions of the new board. Use this when switching
        difficulty levels or starting a new game.

        Args:
            new_board: The new Board object with updated dimensions.

        Raises:
            ValueError: If new_board is None.
        """
        if new_board is None:
            raise ValueError("New board cannot be None")

        # Update board reference
        self.board = new_board

        # Clear existing buttons
        for row in self.buttons:
            for button in row:
                button.destroy()

        # Recreate grid with new dimensions
        self._create_grid()

    def pack(self, **kwargs) -> None:
        """
        Pack the grid frame into the parent widget.

        This is a convenience method that delegates to the frame's pack method,
        allowing the grid to be easily positioned in the main window.

        Args:
            **kwargs: Keyword arguments to pass to frame.pack().
        """
        self.frame.pack(**kwargs)

    def grid(self, **kwargs) -> None:
        """
        Grid the grid frame into the parent widget.

        This is a convenience method that delegates to the frame's grid method,
        allowing the grid to be easily positioned in the main window.

        Args:
            **kwargs: Keyword arguments to pass to frame.grid().
        """
        self.frame.grid(**kwargs)
