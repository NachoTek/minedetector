"""
Mine Counter Module

Creates and manages the mine counter display for the Mine Detector game.
Shows the number of remaining mines (total mines minus placed flags).
"""

import tkinter as tk
from typing import Optional
from src.game.board import Board


class MineCounter:
    """
    Manages the mine counter display for the Mine Detector game.

    This counter displays the number of remaining mines to be found,
    calculated as: total_mines - flags_placed. The counter follows
    the classic Windows Mine Detector appearance with LCD-style digits
    that change color based on the value.

    The counter shows:
    - Positive values (0-999): Black text on red background
    - Negative values: Red text on black background (indicates too many flags)

    Attributes:
        parent: The parent Tkinter widget (usually the main window).
        board: The game Board object containing mine and flag data.
        total_mines: The total number of mines on the board.
        current_count: The current remaining mine count being displayed.

    Example:
        >>> counter = MineCounter(parent_window, board, total_mines=10)
        >>> counter.decrement()  # Flag placed, shows 9
        >>> counter.increment()  # Flag removed, shows 10
    """

    # Maximum display value (counter shows max 999)
    MAX_DISPLAY = 999
    """Maximum value that can be displayed on the counter."""

    # Minimum display value (counter shows min -999)
    MIN_DISPLAY = -999
    """Minimum value that can be displayed on the counter."""

    def __init__(
        self,
        parent: tk.Widget,
        board: Board,
        total_mines: Optional[int] = None
    ):
        """
        Initialize the mine counter display.

        Creates a label widget with LCD-style appearance showing the
        remaining mine count. The count is initialized to total_mines
        (since no flags are placed at game start).

        Args:
            parent: The parent Tkinter widget to contain the counter.
            board: The game Board object with cell data.
            total_mines: Override total mine count (defaults to board.mine_count).

        Raises:
            ValueError: If board is None.
        """
        if board is None:
            raise ValueError("Board cannot be None")

        self.parent = parent
        """The parent Tkinter widget containing this counter."""

        self.board = board
        """The game Board object containing cell data."""

        # Use provided total_mines or default to board's mine_count
        self.total_mines = total_mines if total_mines is not None else board.mine_count
        """The total number of mines on the board."""

        # Initialize current count to total mines (no flags placed yet)
        self.current_count = self.total_mines
        """The current remaining mine count being displayed."""

        # Create the counter label with LCD-style appearance
        self.label = tk.Label(
            parent,
            text=str(self._format_display(self.current_count)),
            font=("Courier", 20, "bold"),
            width=4,
            relief="sunken",
            bd=2
        )
        """The Tkinter label widget displaying the count."""

        # Set initial colors based on count
        self._update_colors()

    def _format_display(self, count: int) -> str:
        """
        Format the count for display, clamping to valid range.

        The counter can only display values between -999 and 999.
        Values outside this range are clamped to the nearest bound.

        Args:
            count: The raw count value to format.

        Returns:
            The formatted count as a string (clamped to display range).
        """
        # Clamp to display range
        clamped = max(self.MIN_DISPLAY, min(self.MAX_DISPLAY, count))
        return f"{clamped:03d}"  # Zero-padded to 3 digits

    def _update_colors(self) -> None:
        """
        Update the label colors based on current count value.

        Positive counts (normal): Black text on red background
        Negative counts (too many flags): Red text on black background
        """
        if self.current_count >= 0:
            # Normal: black on red
            self.label.config(
                fg="black",
                bg="#ff0000"
            )
        else:
            # Too many flags: red on black
            self.label.config(
                fg="red",
                bg="black"
            )

    def decrement(self) -> None:
        """
        Decrement the counter (called when a flag is placed).

        Decrements the remaining mine count by 1, indicating that a flag
        has been placed on a cell. Updates the display and colors.

        The display will show negative values if more flags are placed
        than there are mines (indicating incorrect flagging).
        """
        self.current_count -= 1
        self._update_display()

    def increment(self) -> None:
        """
        Increment the counter (called when a flag is removed).

        Increments the remaining mine count by 1, indicating that a flag
        has been removed from a cell. Updates the display and colors.
        """
        self.current_count += 1
        self._update_display()

    def reset(self, new_total: Optional[int] = None) -> None:
        """
        Reset the counter to initial mine count.

        Resets the counter display to show the total number of mines,
        typically called when starting a new game. Optionally updates
        the total mine count if the difficulty has changed.

        Args:
            new_total: Optional new total mine count (for difficulty changes).
        """
        if new_total is not None:
            self.total_mines = new_total

        self.current_count = self.total_mines
        self._update_display()

    def _update_display(self) -> None:
        """
        Update the counter display and colors.

        Refreshes the label text with the current count and updates
        the foreground/background colors based on whether the count
        is positive or negative.
        """
        # Update text with formatted count
        self.label.config(text=str(self._format_display(self.current_count)))

        # Update colors based on new count
        self._update_colors()

    def set_count(self, count: int) -> None:
        """
        Set the counter to a specific value.

        Directly sets the counter to the specified value. This can be
        used to synchronize the counter with the actual flag count on
        the board.

        Args:
            count: The new count value to display.
        """
        self.current_count = count
        self._update_display()

    def pack(self, **kwargs) -> None:
        """
        Pack the counter label into the parent widget.

        This is a convenience method that delegates to the label's pack method,
        allowing the counter to be easily positioned in the main window.

        Args:
            **kwargs: Keyword arguments to pass to label.pack().
        """
        self.label.pack(**kwargs)

    def grid(self, **kwargs) -> None:
        """
        Grid the counter label into the parent widget.

        This is a convenience method that delegates to the label's grid method,
        allowing the counter to be easily positioned in the main window.

        Args:
            **kwargs: Keyword arguments to pass to label.grid().
        """
        self.label.grid(**kwargs)
