"""
Game Timer Module

Creates and manages the game timer for the Minesweeper game.
Counts up from 0 starting on the first cell reveal, stops on game end.
"""

import tkinter as tk
from typing import Optional


class GameTimer:
    """
    Manages the game timer display for the Minesweeper game.

    This timer counts up from 0 seconds, starting when the player makes
    their first cell reveal, and stopping when the game is won or lost.
    The timer follows the classic Windows Minesweeper appearance with
    LCD-style digits matching the mine counter.

    The timer shows:
    - Elapsed time in seconds (0-999)
    - Clamps at 999 for games longer than 999 seconds

    Attributes:
        parent: The parent Tkinter widget (usually the main window).
        elapsed_seconds: The number of seconds elapsed since timer started.
        is_running: Whether the timer is currently running.
        timer_id: The Tkinter after() callback ID (for canceling updates).

    Example:
        >>> timer = GameTimer(parent_window)
        >>> timer.start()  # Starts counting up from 0
        >>> timer.stop()   # Stops the timer
        >>> timer.reset()  # Resets to 0
    """

    # Maximum display value (timer shows max 999 seconds like Windows Minesweeper)
    MAX_DISPLAY = 999
    """Maximum value that can be displayed on the timer (16.65 minutes)."""

    # Timer update interval in milliseconds
    UPDATE_INTERVAL = 1000
    """Number of milliseconds between timer updates (1 second)."""

    def __init__(self, parent: tk.Widget):
        """
        Initialize the game timer display.

        Creates a label widget with LCD-style appearance showing the
        elapsed time in seconds. The timer starts at 0 and is not
        running until start() is called.

        Args:
            parent: The parent Tkinter widget to contain the timer.

        Raises:
            ValueError: If parent is None.
        """
        if parent is None:
            raise ValueError("Parent cannot be None")

        self.parent = parent
        """The parent Tkinter widget containing this timer."""

        # Initialize timer state
        self.elapsed_seconds = 0
        """The number of seconds elapsed since the timer started."""

        self.is_running = False
        """Whether the timer is currently counting up."""

        self.timer_id: Optional[str] = None
        """The Tkinter after() callback ID, used to cancel scheduled updates."""

        # Create the timer label with LCD-style appearance
        self.label = tk.Label(
            parent,
            text=self._format_display(self.elapsed_seconds),
            font=("Courier", 20, "bold"),
            width=4,
            relief="sunken",
            bd=2,
            fg="black",
            bg="#ff0000"
        )
        """The Tkinter label widget displaying the elapsed time."""

    def _format_display(self, seconds: int) -> str:
        """
        Format the elapsed time for display, clamping to maximum value.

        The timer can only display values between 0 and 999 seconds.
        Values above 999 are clamped to 999 (the Windows Minesweeper limit).

        Args:
            seconds: The raw elapsed time in seconds to format.

        Returns:
            The formatted time as a string (clamped to display range).
        """
        # Clamp to maximum display value
        clamped = min(self.MAX_DISPLAY, seconds)
        return f"{clamped:03d}"  # Zero-padded to 3 digits

    def start(self) -> None:
        """
        Start the timer.

        Begins counting up from the current elapsed_seconds value.
        If the timer is already running, this method does nothing
        (prevents multiple simultaneous update loops).

        Note:
            The timer updates every 1 second using Tkinter's after()
            method, which schedules the _update_timer method to run
            after UPDATE_INTERVAL milliseconds.
        """
        if self.is_running:
            # Already running, don't start another loop
            return

        self.is_running = True
        self._schedule_next_update()

    def stop(self) -> None:
        """
        Stop the timer.

        Stops counting up at the current elapsed_seconds value.
        Cancels any pending update callbacks scheduled by Tkinter.

        Note:
            This method cancels the scheduled after() callback to
            prevent the timer from continuing to count up.
        """
        if not self.is_running:
            # Already stopped
            return

        self.is_running = False

        # Cancel the scheduled update if it exists
        if self.timer_id is not None:
            self.parent.after_cancel(self.timer_id)
            self.timer_id = None

    def reset(self) -> None:
        """
        Reset the timer to 0.

        Resets the elapsed time to 0 and stops the timer if it is running.
        This is typically called when starting a new game.

        Note:
            The timer must be explicitly started again after reset
            by calling start(). This ensures the timer doesn't begin
            counting until the first cell is revealed.
        """
        # Stop the timer if running
        self.stop()

        # Reset elapsed time to 0
        self.elapsed_seconds = 0

        # Update the display
        self._update_display()

    def _schedule_next_update(self) -> None:
        """
        Schedule the next timer update.

        Schedules the _update_timer method to run after UPDATE_INTERVAL
        milliseconds (1 second). This creates the recurring 1-second
        update loop for the timer.
        """
        if self.is_running:
            self.timer_id = self.parent.after(
                self.UPDATE_INTERVAL,
                self._update_timer
            )

    def _update_timer(self) -> None:
        """
        Update the timer display and schedule the next update.

        Increments the elapsed_seconds counter, updates the display,
        and schedules the next update if the timer is still running.

        This method is called automatically every 1 second by the
        Tkinter after() mechanism.
        """
        if not self.is_running:
            # Timer was stopped, don't continue
            return

        # Increment elapsed time
        self.elapsed_seconds += 1

        # Update the display
        self._update_display()

        # Schedule next update if we haven't reached max
        if self.elapsed_seconds < self.MAX_DISPLAY:
            self._schedule_next_update()
        else:
            # Reached maximum display value, stop counting
            self.stop()

    def _update_display(self) -> None:
        """
        Update the timer display.

        Refreshes the label text with the current elapsed time.
        The time is formatted as a 3-digit zero-padded number.
        """
        self.label.config(text=self._format_display(self.elapsed_seconds))

    def get_elapsed_time(self) -> int:
        """
        Get the current elapsed time in seconds.

        Returns the current elapsed time value, useful for saving
        game state or displaying the time in other formats.

        Returns:
            The current elapsed time in seconds (0-999).
        """
        return self.elapsed_seconds

    def pack(self, **kwargs) -> None:
        """
        Pack the timer label into the parent widget.

        This is a convenience method that delegates to the label's pack method,
        allowing the timer to be easily positioned in the main window.

        Args:
            **kwargs: Keyword arguments to pass to label.pack().
        """
        self.label.pack(**kwargs)

    def grid(self, **kwargs) -> None:
        """
        Grid the timer label into the parent widget.

        This is a convenience method that delegates to the label's grid method,
        allowing the timer to be easily positioned in the main window.

        Args:
            **kwargs: Keyword arguments to pass to label.grid().
        """
        self.label.grid(**kwargs)
