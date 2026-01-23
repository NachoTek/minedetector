# Minesweeper Clone

A complete Minesweeper clone that replicates the original Windows Minesweeper feature set exactly, built with Python and Tkinter.

## Features

- **Three Difficulty Levels**
  - Beginner: 9×9 grid with 10 mines
  - Intermediate: 16×16 grid with 40 mines
  - Expert: 30×16 grid with 99 mines

- **Core Game Mechanics**
  - Left-click to reveal cells
  - Right-click to place/remove flags
  - Chording: Click revealed numbered cells with correct flag count to reveal neighbors
  - First-click safety: First click is never a mine
  - Flood fill: Blank cells automatically reveal connected regions

- **Game State Management**
  - Win detection when all non-mine cells are revealed
  - Loss detection when a mine is clicked
  - Timer starts on first click and stops on game end
  - Mine counter updates in real-time as flags are placed

- **Authentic Windows UI**
  - Grid-based game board with clickable cells
  - Reset button with reactive face icons (happy, shocked, dead, cool)
  - Mine counter display
  - Game timer

## Project Structure

```
minesweeper/
├── src/
│   ├── models/          # Data models (Cell, GameState)
│   ├── game/            # Game logic (Board, flood fill, chording)
│   └── ui/              # User interface (Main window, grid, timer, counter)
├── tests/               # Unit tests
├── main.py              # Application entry point
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Requirements

- Python 3.7 or higher
- Tkinter (built into Python, no installation required)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd minedetector
```

2. Install testing dependencies:
```bash
pip install -r requirements.txt
```

## Running the Game

```bash
python main.py
```

## Running Tests

Run all tests:
```bash
pytest tests/ -v
```

Run tests with coverage:
```bash
pytest tests/ -v --cov=src --cov-report=term-missing
```

## Gameplay

1. **Select a difficulty** from the Game menu (Beginner, Intermediate, or Expert)
2. **Left-click** any cell to reveal it
   - First click is always safe
   - Blank cells trigger flood fill to reveal connected region
   - Numbers indicate adjacent mine count (1-8)
3. **Right-click** to place flags where you think mines are
4. **Chording**: When a numbered cell has the correct number of flags around it, click it to reveal all remaining neighbors
5. **Win** by revealing all non-mine cells
6. **Click the face button** to reset the game at any time

## Technical Details

- **Framework**: Tkinter (built-in Python GUI library)
- **Testing**: pytest with coverage reporting
- **Architecture**: Modular design with separation of concerns (models, game logic, UI)

### Key Algorithms

- **Flood Fill**: Stack-based iteration to safely reveal large blank regions
- **Mine Placement**: Random placement with first-click safety guarantee
- **Adjacent Counting**: Counts mines in all 8 neighbors for each cell
- **Chording**: Reveals neighbors when flag count matches cell number

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
