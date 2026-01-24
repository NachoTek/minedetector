# Minedetector v0.1.0 Release Notes

## Overview

Minedetector v0.1.0 is a complete, playable implementation of the classic Minesweeper puzzle game built with Python and Tkinter. This release features all core gameplay mechanics, an authentic Windows-style interface, and a standalone Windows executable for easy distribution.

## What's New in v0.1.0

This is the initial stable release of Minedetector, featuring:

### Gameplay Features
- **Classic Minesweeper mechanics** - Left-click to reveal, right-click to flag
- **Chording** - Click revealed numbers with correct flag count to reveal neighbors
- **First-click safety** - Your first click is guaranteed not to be a mine
- **Flood fill** - Blank cells automatically reveal connected regions
- **Win/loss detection** - Automatic game end detection
- **Timer** - Starts on first click, stops on game end
- **Mine counter** - Updates in real-time as flags are placed

### User Interface
- **Responsive face button** - Reacts to game state:
  - 🙂 Happy - Game in progress
  - 😮 Shocked - Mouse button held on tile
  - 😎 Cool - You won!
  - 😵 Dead - Game over
- **Clean grid layout** - 9×9 game board with instant visual feedback
- **Fixed window size** - Non-resizable for consistent gameplay

### Technical Features
- **Modular architecture** - Clean separation between models, game logic, and UI
- **No runtime dependencies** - Uses only Python standard library
- **Windows executable** - Standalone `.exe` with bundled Python runtime
- **Automated builds** - GitHub Actions workflow for future releases

## Installation

### Windows (Executable)
Download `Minedetector.exe` from the [Assets](#assets) section below and run. No installation required.

### From Source
```bash
git clone https://github.com/NachoTek/minedetector.git
cd minedetector
python main.py
```

Requires Python 3.7+.

## Known Issues

- Windows may show a SmartScreen warning when running the executable (click "More info" → "Run anyway"). This occurs because the executable is not digitally signed.
- Some antivirus software may flag PyInstaller executables as suspicious. This is a false positive—the source code is available for verification.

## Development Notes

Built with:
- Python 3.x
- Tkinter (standard library)
- PyInstaller for executable packaging

## Contributors

This project was developed by NachoTek.

## Next Release

Future versions may include:
- Difficulty levels (Beginner, Intermediate, Expert)
- Custom grid sizes and mine counts
- UI themes and customization
- Code signing to eliminate SmartScreen warnings

---

**Full Changelog**: https://github.com/NachoTek/minedetector/commits/v0.1.0
