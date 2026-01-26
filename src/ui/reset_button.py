"""
Reset Button Module

Creates and manages the reset button with reactive face icons for
the Mine Detector game.
Changes expression based on game state and resets the game when clicked.
"""

import tkinter as tk
from typing import Callable, Optional


class ResetButton:
    """
    Manages the reset button with reactive face icons for the Mine Detector game.

    The reset button displays different face icons based on the current game state:
    - Happy (🙂): Game is in progress, normal playing state
    - Shocked (😮): Player is clicking a cell (momentary state during click)
    - Dead (😵): Game was lost (mine clicked)
    - Cool (😎): Game was won (all non-mine cells revealed)

    Clicking the button at any time resets the game to the initial state,
    regenerating the mine positions and resetting the timer and counter.

    Attributes:
        parent: The parent Tkinter widget (usually the main window).
        on_reset: Optional callback function invoked when button is clicked.
        current_state: The current face state being displayed.

    Example:
        >>> def reset_handler():
        ...     print("Game reset!")
        >>> button = ResetButton(parent_window, on_reset=reset_handler)
        >>> button.set_happy()  # Show playing face
        >>> button.set_dead()   # Show loss face
    """

    # Face icon constants using Unicode emoji
    FACE_HAPPY = "🙂"
    """Happy face icon for normal playing state."""

    FACE_SHOCKED = "😮"
    """Shocked face icon for clicking state."""

    FACE_DEAD = "😵"
    """Dead face icon for game lost state."""

    FACE_COOL = "😎"
    """Cool face icon for game won state."""

    # Face state names for validation
    VALID_STATES = {"happy", "shocked", "dead", "cool"}
    """Set of valid face state names."""

    def __init__(
        self, parent: tk.Widget, on_reset: Optional[Callable[[], None]] = None
    ):
        """
        Initialize the reset button with reactive face icons.

        Creates a button widget with the happy face icon (default playing state).
        The button is sized to display emoji clearly and is configured with
        standard Windows Mine Detector button styling.

        Args:
            parent: The parent Tkinter widget to contain the button.
            on_reset: Optional callback function invoked when button is clicked.

        Raises:
            ValueError: If parent is None.
        """
        if parent is None:
            raise ValueError("Parent cannot be None")

        self.parent = parent
        """The parent Tkinter widget containing this button."""

        self.on_reset = on_reset
        """Optional callback function invoked when button is clicked."""

        # Track current face state
        self.current_state = "happy"
        """The current face state being displayed."""

        # Create the button with happy face as default
        self.button = tk.Button(
            parent,
            text=self.FACE_HAPPY,
            font=("Segoe UI Emoji", 24),
            width=3,
            height=1,
            relief="raised",
            bd=2,
            command=self._handle_click,
        )
        """The Tkinter button widget displaying the face icon."""

    def _handle_click(self) -> None:
        """
        Handle button click event.

        This method is called when the reset button is clicked. It temporarily
        changes the face to shocked, then invokes the on_reset callback if one
        was provided, and finally resets the face to happy.

        The shocked state provides visual feedback during the click action,
        mimicking the classic Windows Mine Detector behavior.
        """
        # Show shocked face momentarily
        self.set_shocked()

        # Invoke reset callback if provided
        if self.on_reset:
            self.on_reset()

        # Reset to happy face after click
        self.set_happy()

    def set_happy(self) -> None:
        """
        Set the button to show the happy face.

        The happy face (🙂) is displayed during normal gameplay when the game
        is in progress and the player is not currently clicking a cell.
        """
        self.current_state = "happy"
        self.button.config(text=self.FACE_HAPPY)

    def set_shocked(self) -> None:
        """
        Set the button to show the shocked face.

        The shocked face (😮) is displayed momentarily when the player clicks
        on a cell, providing visual feedback for the click action. This state
        is typically shown during mouse button press and reverted after release.
        """
        self.current_state = "shocked"
        self.button.config(text=self.FACE_SHOCKED)

    def set_dead(self) -> None:
        """
        Set the button to show the dead face.

        The dead face (😵) is displayed when the game is lost (a mine was
        clicked). This state persists until the game is reset.
        """
        self.current_state = "dead"
        self.button.config(text=self.FACE_DEAD)

    def set_cool(self) -> None:
        """
        Set the button to show the cool face.

        The cool face (😎) is displayed when the game is won (all non-mine
        cells have been revealed). This state persists until the game is reset.
        """
        self.current_state = "cool"
        self.button.config(text=self.FACE_COOL)

    def set_state(self, state: str) -> None:
        """
        Set the button face state by name.

        This is a convenience method to set the face state using a string
        name instead of calling the specific set_* methods. Useful for
        programmatic state updates based on game state enums.

        Args:
            state: The face state to set ("happy", "shocked", "dead", or "cool").

        Raises:
            ValueError: If the state name is not recognized.
        """
        if state not in self.VALID_STATES:
            raise ValueError(
                f"Invalid face state: {state}. "
                f"Must be one of {list(self.VALID_STATES)}"
            )

        if state == "happy":
            self.set_happy()
        elif state == "shocked":
            self.set_shocked()
        elif state == "dead":
            self.set_dead()
        elif state == "cool":
            self.set_cool()

    def get_state(self) -> str:
        """
        Get the current face state.

        Returns the name of the currently displayed face state.

        Returns:
            The current face state name ("happy", "shocked", "dead", or "cool").
        """
        return self.current_state

    def pack(self, **kwargs) -> None:
        """
        Pack the button into the parent widget.

        This is a convenience method that delegates to the button's pack method,
        allowing the reset button to be easily positioned in the main window.

        Args:
            **kwargs: Keyword arguments to pass to button.pack().
        """
        self.button.pack(**kwargs)

    def grid(self, **kwargs) -> None:
        """
        Grid the button into the parent widget.

        This is a convenience method that delegates to the button's grid method,
        allowing the reset button to be easily positioned in the main window.

        Args:
            **kwargs: Keyword arguments to pass to button.grid().
        """
        self.button.grid(**kwargs)
