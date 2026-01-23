"""
Minedetector Game - Main Entry Point

This is the main entry point for the Minedetector game application.
It creates and starts the main game window.
"""

import sys
from src.ui.main_window import MainWindow


def main():
    """Main entry point for the Minedetector game."""
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
