"""
Minesweeper Game - Entry Point

This is the main entry point for the Minesweeper desktop application.
It creates the main game window and starts the Tkinter event loop.

The application uses Tkinter for the UI and implements a complete
Minesweeper clone with three difficulty levels (Beginner, Intermediate,
Expert), first-click safety, flood fill revealing, and chording mechanics.

Usage:
    python main.py

Features:
    - Three difficulty levels matching Windows Minesweeper
    - First-click safety (first click is never a mine)
    - Flood fill algorithm for revealing connected blank regions
    - Chording mechanic for efficient gameplay
    - Mine counter and game timer
    - Reset button with reactive face icons
    - Win/loss state detection

Author: Minesweeper Clone Project
"""

import sys
from src.ui.main_window import MainWindow


def main() -> None:
    """
    Main function to launch the Minesweeper application.

    Creates an instance of MainWindow and starts the Tkinter event loop.
    This is a blocking call that will not return until the application
    window is closed.

    The function includes error handling to catch and report any
    unexpected exceptions during application startup.

    Returns:
        None

    Raises:
        Exception: If any error occurs during application initialization.
    """
    try:
        # Create the main game window
        game_window = MainWindow()

        # Start the Tkinter event loop (blocks until window is closed)
        game_window.start()

    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("\nGame interrupted by user.")
        sys.exit(0)
    except Exception as e:
        # Catch and report any unexpected errors
        print(f"Error starting Minesweeper: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
