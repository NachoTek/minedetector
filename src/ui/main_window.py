"""
Main Window Module

Creates and manages the primary Mine Detector game window using Tkinter.
Provides difficulty selection via Game menu and sets up the main application structure.
"""

import tkinter as tk
from typing import Dict, Tuple, Optional
from src.game.board import Board
from src.models.game_state import GameState
from src.ui.game_grid import GameGrid
from src.ui.mine_counter import MineCounter
from src.ui.timer import GameTimer
from src.ui.reset_button import ResetButton


class MainWindow:
    """
    The main application window for the Mine Detector game.

    This class creates the primary Tkinter window, sets up the Game menu
    with difficulty selection options (Beginner, Intermediate, Expert), and
    manages the overall application structure.

    The window follows the classic Windows Mine Detector layout with a menu bar
    at the top for difficulty selection.

    Attributes:
        root: The Tkinter root window object.
        current_difficulty: The currently selected difficulty level (default: "Beginner").
        board: The game Board object containing cell data and game logic.
        game_grid: The GameGrid UI component for displaying cells.
        mine_counter: The MineCounter UI component for displaying remaining mines.
        timer: The GameTimer UI component for displaying elapsed time.
        reset_button: The ResetButton UI component with reactive face icons.
        first_click_made: Whether the first cell has been revealed (starts timer).

    Difficulty Configurations:
        Beginner: 9 rows × 9 columns, 10 mines
        Intermediate: 16 rows × 16 columns, 40 mines
        Expert: 16 rows × 30 columns, 99 mines

    Example:
        >>> window = MainWindow()
        >>> window.start()  # Displays the window and starts the event loop
    """

    # Difficulty configurations as class constants
    # Following Windows Mine Detector standard difficulties
    DIFFICULTIES: Dict[str, Dict[str, int]] = {
        "Beginner": {
            "rows": 9,
            "cols": 9,
            "mines": 10
        },
        "Intermediate": {
            "rows": 16,
            "cols": 16,
            "mines": 40
        },
        "Expert": {
            "rows": 16,
            "cols": 30,
            "mines": 99
        }
    }
    """Dictionary mapping difficulty names to their grid configurations."""

    def __init__(self):
        """
        Initialize the main game window.

        Creates the Tkinter root window, sets the window title, and initializes
        the difficulty selection menu. The default difficulty is set to Beginner.
        """
        # Create the main Tkinter window
        self.root = tk.Tk()
        """The root Tkinter window object."""

        # Set window title
        self.root.title("Mine Detector")

        # Disable window resizing
        self.root.resizable(False, False)

        # Initialize current difficulty
        self.current_difficulty = "Beginner"
        """The currently selected difficulty level."""

        # Create the menu bar
        self._create_menu()

        # Initialize game board
        config = self.get_difficulty_config()
        self.board = Board(
            config["rows"],
            config["cols"],
            config["mines"]
        )
        """The game Board object containing cell data and game logic."""

        # Initialize game grid UI
        self.game_grid: Optional[GameGrid] = None
        """The GameGrid UI component for displaying cells (created after menu)."""

        # Initialize mine counter UI
        self.mine_counter: Optional[MineCounter] = None
        """The MineCounter UI component for displaying remaining mines (created after menu)."""

        # Initialize timer UI
        self.timer: Optional[GameTimer] = None
        """The GameTimer UI component for displaying elapsed time (created after menu)."""

        # Initialize reset button UI
        self.reset_button: Optional[ResetButton] = None
        """The ResetButton UI component for game reset (created after menu)."""

        # Track if first click has been made (starts the timer)
        self.first_click_made = False
        """Whether the first cell has been revealed (timer starts on first click)."""

        # Create the top frame for mine counter, reset button, and timer
        self._create_top_frame()

        # Create the game grid
        self._create_game_grid()

    def _create_menu(self) -> None:
        """
        Create the Game menu with difficulty selection options.

        This method creates a menu bar with a single "Game" menu that contains
        three difficulty options: Beginner, Intermediate, and Expert. Each option
        calls the corresponding difficulty selection method when clicked.

        The menu structure:
        - Game
            - Beginner
            - Intermediate
            - Expert
        """
        # Create menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # Create Game menu
        game_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Game", menu=game_menu)

        # Add difficulty options
        game_menu.add_command(
            label="Beginner",
            command=lambda: self._set_difficulty("Beginner")
        )
        game_menu.add_command(
            label="Intermediate",
            command=lambda: self._set_difficulty("Intermediate")
        )
        game_menu.add_command(
            label="Expert",
            command=lambda: self._set_difficulty("Expert")
        )

        # Add separator
        game_menu.add_separator()

        # Add exit option
        game_menu.add_command(label="Exit", command=self.root.quit)

    def _create_top_frame(self) -> None:
        """
        Create the top frame containing mine counter, reset button, and timer.

        This method creates a horizontal frame that holds the three top UI components:
        - Mine counter (left side)
        - Reset button with face icon (centered)
        - Game timer (right side)

        The frame is packed at the top of the window below the menu bar.
        """
        # Create a frame to hold the top components
        top_frame = tk.Frame(self.root)
        top_frame.pack(padx=10, pady=(10, 5), fill="x")

        # Create mine counter (left side)
        self.mine_counter = MineCounter(
            top_frame,
            self.board,
            total_mines=self.board.mine_count
        )
        self.mine_counter.pack(side="left", anchor='center')

        # Create reset button (centered)
        self.reset_button = ResetButton(
            top_frame,
            on_reset=self._reset_game
        )
        self.reset_button.pack(anchor='center')

        # Create timer (right side)
        self.timer = GameTimer(top_frame)
        self.timer.pack(side="right", anchor='center')

    def _create_game_grid(self) -> None:
        """
        Create the game grid UI component.

        Initializes the GameGrid with the current board and sets up
        click event handlers for cell interactions. The grid is
        packed into the main window below the menu bar.
        """
        self.game_grid = GameGrid(
            self.root,
            self.board,
            on_cell_click=self._on_cell_click,
            on_cell_right_click=self._on_cell_right_click
        )

        # Pack the grid into the window
        self.game_grid.pack(padx=10, pady=10)

    def _on_cell_click(self, row: int, col: int) -> None:
        """
        Handle left-click event on a cell.

        This callback is invoked when a cell button is left-clicked. It handles
        three scenarios:
        1. First click: Places mines (with first-click safety), then reveals cell
        2. Clicking revealed numbered cell: Attempts chording if flags match number
        3. Clicking unrevealed cell: Reveals the cell (triggers flood fill if blank)

        After each reveal, checks for win/loss conditions and updates the UI.

        Args:
            row: Row index of the clicked cell (0-based).
            col: Column index of the clicked cell (0-based).
        """
        # Don't allow input after game is over
        if not self._is_input_allowed():
            return

        # Show shocked face while clicking
        self._set_face_shocked()

        cell = self.board.get_cell(row, col)

        # Handle first click (mine placement with first-click safety)
        if not self.first_click_made:
            self.first_click_made = True
            if self.timer:
                self.timer.start()
            # Place mines after first click to ensure safety
            self.board.place_mines(row, col)
            # Re-fetch the cell after mine placement (adjacent_mines may have changed)
            cell = self.board.get_cell(row, col)

        # Handle chording on revealed numbered cells
        if cell.revealed and cell.adjacent_mines > 0:
            # Attempt chording
            self.board.chord_cell(row, col)
        # Handle revealing unrevealed cells
        elif not cell.revealed:
            # Don't reveal flagged cells
            if not cell.flagged:
                self.board.reveal_cell(row, col)

        # Update all cell displays (flood fill may have revealed many cells)
        if self.game_grid:
            self.game_grid.update_all_cells()

        # Check game state and update UI
        self._check_game_state()

        # Reset face to happy if game is still playing
        if self.board.game_state == GameState.PLAYING:
            self._set_face_happy()

    def _on_cell_right_click(self, row: int, col: int) -> None:
        """
        Handle right-click event on a cell.

        This callback is invoked when a cell button is right-clicked.
        Toggles the flag state of the cell and updates the mine counter
        accordingly. If a flag is placed, the counter decrements; if a
        flag is removed, the counter increments.

        Args:
            row: Row index of the clicked cell (0-based).
            col: Column index of the clicked cell (0-based).
        """
        # Don't allow input after game is over
        if not self._is_input_allowed():
            return

        # Get the cell
        cell = self.board.get_cell(row, col)

        # Don't allow flagging revealed cells
        if cell.revealed:
            return

        # Toggle flag state
        if cell.flagged:
            # Remove flag
            cell.flagged = False
            if self.mine_counter:
                self.mine_counter.increment()
        else:
            # Place flag
            cell.flagged = True
            if self.mine_counter:
                self.mine_counter.decrement()

        # Update the cell display
        if self.game_grid:
            self.game_grid.update_cell(row, col)

    def _is_input_allowed(self) -> bool:
        """
        Check if user input is currently allowed.

        Input is only allowed when the game is in the PLAYING state.
        Once the game transitions to WON or LOST, all input is disabled
        until the game is reset.

        Returns:
            True if input is allowed (game is playing), False otherwise.
        """
        return self.board.game_state == GameState.PLAYING

    def _check_game_state(self) -> None:
        """
        Check and handle game state changes.

        This method updates the game state based on current board conditions
        and handles the UI updates for win/loss states:
        - Stops the timer
        - Updates the reset button face icon
        - Reveals all mines on loss

        The method checks for loss first (mine revealed), then win (all safe
        cells revealed), following the priority order from the spec.
        """
        # Update game state based on current board
        self.board.update_game_state()

        # Handle loss state
        if self.board.game_state == GameState.LOST:
            self._handle_game_over(won=False)
        # Handle win state
        elif self.board.game_state == GameState.WON:
            self._handle_game_over(won=True)

    def _handle_game_over(self, won: bool) -> None:
        """
        Handle game over state (win or loss).

        This method performs all necessary UI updates when the game ends:
        - Stops the timer
        - Updates the reset button face icon (cool for win, dead for loss)
        - Reveals all mine positions on loss

        Args:
            won: True if the game was won, False if lost.
        """
        # Stop the timer
        if self.timer:
            self.timer.stop()

        # Update face icon
        if won:
            self._set_face_cool()
        else:
            self._set_face_dead()
            # Reveal all mines on loss
            self._reveal_all_mines()

    def _reveal_all_mines(self) -> None:
        """
        Reveal all mine positions on the board.

        This method is called when the game is lost to show the player
        where all the mines were located. It updates the visual display
        of all mine cells.
        """
        # Reveal all mine cells
        for row in range(self.board.rows):
            for col in range(self.board.cols):
                cell = self.board.get_cell(row, col)
                if cell.mine:
                    cell.revealed = True

        # Update the grid display
        if self.game_grid:
            self.game_grid.update_all_cells()

    def _set_difficulty(self, difficulty: str) -> None:
        """
        Set the current game difficulty.

        Updates the current_difficulty attribute and triggers any necessary
        UI updates to reflect the new difficulty level. In this initial
        implementation, the difficulty is stored and will be used by
        subsequent UI components (game grid, mine counter, etc.).

        Args:
            difficulty: The difficulty level to set ("Beginner", "Intermediate", or "Expert").

        Raises:
            ValueError: If the difficulty name is not recognized.

        Example:
            >>> window = MainWindow()
            >>> window._set_difficulty("Expert")
            >>> print(window.current_difficulty)
            'Expert'
        """
        if difficulty not in self.DIFFICULTIES:
            raise ValueError(
                f"Invalid difficulty: {difficulty}. "
                f"Must be one of {list(self.DIFFICULTIES.keys())}"
            )

        self.current_difficulty = difficulty

        # Reset the game with new difficulty settings
        self._reset_game()

    def _reset_game(self) -> None:
        """
        Reset the game to initial state.

        Creates a new board with fresh mine positions, resets the mine counter
        and timer, and refreshes the game grid display. This method is called
        when the reset button is clicked or when the difficulty is changed.

        The reset maintains the current difficulty level but regenerates all
        mine positions and resets all game state.
        """
        # Create new board with same difficulty settings
        config = self.get_difficulty_config()
        self.board = Board(
            config["rows"],
            config["cols"],
            config["mines"]
        )

        # Resize the game grid to match new board
        if self.game_grid:
            self.game_grid.resize(self.board)

        # Reset mine counter to total mines
        if self.mine_counter:
            self.mine_counter.reset(new_total=config["mines"])

        # Reset timer to 0
        if self.timer:
            self.timer.reset()

        # Reset first click flag
        self.first_click_made = False

        # Reset button face to happy
        if self.reset_button:
            self.reset_button.set_happy()

    def _set_face_happy(self) -> None:
        """
        Set the reset button face to happy (playing state).

        The happy face is displayed during normal gameplay when the game
        is in progress.
        """
        if self.reset_button:
            self.reset_button.set_happy()

    def _set_face_shocked(self) -> None:
        """
        Set the reset button face to shocked (clicking state).

        The shocked face is displayed momentarily when the player is
        clicking on a cell, providing visual feedback.
        """
        if self.reset_button:
            self.reset_button.set_shocked()

    def _set_face_dead(self) -> None:
        """
        Set the reset button face to dead (lost state).

        The dead face is displayed when the game is lost (a mine was
        clicked). This state persists until the game is reset.
        """
        if self.reset_button:
            self.reset_button.set_dead()

    def _set_face_cool(self) -> None:
        """
        Set the reset button face to cool (won state).

        The cool face is displayed when the game is won (all non-mine
        cells have been revealed). This state persists until the game
        is reset.
        """
        if self.reset_button:
            self.reset_button.set_cool()

    def get_difficulty_config(self) -> Dict[str, int]:
        """
        Get the configuration for the current difficulty level.

        Returns a dictionary containing the rows, columns, and mine count
        for the currently selected difficulty.

        Returns:
            Dictionary with keys 'rows', 'cols', and 'mines' representing
            the current difficulty configuration.

        Example:
            >>> window = MainWindow()
            >>> window._set_difficulty("Intermediate")
            >>> config = window.get_difficulty_config()
            >>> print(config['rows'], config['cols'], config['mines'])
            16 16 40
        """
        return self.DIFFICULTIES[self.current_difficulty]

    def start(self) -> None:
        """
        Start the Tkinter event loop and display the window.

        This method blocks and runs the main Tkinter event loop, processing
        events and updating the UI until the window is closed. This should
        be called after all UI components have been initialized.

        Note:
            This is a blocking call that will not return until the window
            is closed. Any code after this call will not execute until
            the application exits.

        Example:
            >>> window = MainWindow()
            >>> window.start()  # Blocks until window is closed
        """
        # Display the window
        self.root.mainloop()
