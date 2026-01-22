#!/usr/bin/env python3
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
        # Create the main window
        window = MainWindow()

        # Start the game (this blocks until the window is closed)
        window.start()

        return 0
    except KeyboardInterrupt:
        # Allow graceful exit with Ctrl+C
        return 0
    except Exception as e:
        print(f"Error starting game: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
