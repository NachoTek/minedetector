"""
User Interface Package

Contains Tkinter-based UI components including:
- MainWindow: Primary game window with menus
- GameGrid: Interactive grid of cell buttons
- MineCounter: Display showing remaining mines
- Timer: Game timer counting up from first click
"""

from .main_window import MainWindow

__all__ = ['MainWindow']
