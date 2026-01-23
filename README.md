# Minedetector

A classic Minedetector game built with Python and Tkinter. This desktop application recreates the timeless puzzle game with all the familiar features you know and love.

![Minedetector](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

## Features

- **Classic Gameplay**: All the traditional Minedetector mechanics
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
   cd Minedetector
   ```

2. No additional dependencies are required! The game uses only Python's standard library.

3. Run the game:
   ```bash
   python main.py
   ```

## Building the Windows Executable

This application can be packaged as a standalone Windows executable that requires no Python installation. The executable is completely portable and self-contained.

### Prerequisites

- **Python 3.8+** installed on your system
- **PyInstaller** 6.0.0 or later

### Install Build Dependencies

2. Install testing dependencies:
```bash
pip install -r requirements.txt
```

## Running the Game

```bash
python main.py
```

**On Git Bash or Linux/macOS**:
```bash
chmod +x build-prod.sh
./build-prod.sh
```

These scripts will:
- Clean any previous build artifacts
- Create a single-file executable with `--onefile` mode
- Hide the console window (GUI-only mode)
- Output the executable to `dist/Minedetector.exe`

#### Option 2: Manual Build

If you prefer to build manually or customize the build process:

**Production Build (Single Portable Executable)**:
```bash
python -m PyInstaller --onefile --windowed --name=Minedetector --clean main.py
```

**Development Build (Faster, Easier to Debug)**:
```bash
python -m PyInstaller --onedir --windowed --name=Minedetector --clean main.py
```

**Debug Build (Shows Console for Error Messages)**:
```bash
python -m PyInstaller --onefile --console --name=Minedetector --clean main.py
```

**Note**: Using `python -m PyInstaller` instead of `pyinstaller` directly ensures the command works regardless of your system PATH configuration.

### Build Flags Explained

- `--onefile`: Creates a single portable executable (recommended for distribution)
- `--onedir`: Creates a folder with the executable and all dependencies (faster builds, better for development)
- `--windowed` or `--noconsole`: Hides the console window (required for GUI applications)
- `--console`: Shows the console window (useful for debugging)
- `--clean`: Cleans the build cache before building (ensures fresh output)
- `--name=Minedetector`: Sets the output executable name

### Output Location

After building, you'll find the executable here:
- **Single-file build**: `dist/Minedetector.exe`
- **Directory build**: `dist/Minedetector/Minedetector.exe`

The single-file executable is typically 5-15 MB in size, as it bundles the entire Python runtime and Tkinter library.

### Testing the Executable

1. Navigate to the `dist` folder
2. Double-click `Minedetector.exe`
3. Verify the game launches without a console window
4. Test all game features to ensure everything works correctly

## Distribution Notes

### Windows SmartScreen Warning

When you run the executable for the first time on Windows, you may see a "Windows protected your PC" warning:

> "Windows Defender SmartScreen prevented an unrecognized app from starting. Running this app might put your PC at risk."

**This is expected behavior** for unsigned executables. To proceed:

1. Click "More info"
2. Click "Run anyway"

This warning appears because the executable is not digitally signed. Code signing is a future enhancement that would prevent this warning.

### Antivirus False Positives

Some antivirus software may flag PyInstaller-generated executables as suspicious. This is a **false positive** and occurs because:

- PyInstaller bundles Python into the executable, which some antivirus heuristics flag
- The executable is not signed with a digital certificate
- New or unrecognized executables are often treated with caution

**The executable is safe** - it's simply the Minedetector game with no malicious behavior. If your antivirus blocks it:

1. Check your antivirus quarantine/exclusions settings
2. Add an exception for `Minedetector.exe`
3. Report it as a false positive to your antivirus vendor

### Verification

To verify the executable is legitimate:

- The source code is available in this repository
- You can build it yourself from source
- It uses only standard Python libraries (Tkinter)
- It makes no network connections
- It doesn't access sensitive system files

## Troubleshooting

### Build Issues

**Problem**: `ModuleNotFoundError: No module named 'tkinter'`

**Solution**: Tkinter is usually included with Python, but on some Linux distributions you need to install it separately:
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter
```

**Problem**: PyInstaller fails with "UPX is not available"

**Solution**: This is just a warning. UPX is an optional compression tool. The build will still succeed, just with a slightly larger executable. You can ignore this warning or install UPX if desired.

**Problem**: Build succeeds but executable crashes on startup

**Solution**: Try building with `--console` flag to see error messages:
```bash
python -m PyInstaller --onefile --console --name=Minedetector --clean main.py
```
Run the executable from a command prompt to see any error messages.

**Problem**: Executable is very large (> 50 MB)

**Solution**: This is normal for PyInstaller single-file builds. The entire Python runtime is bundled. To reduce size:
- Use `--onedir` mode (creates folder with shared dependencies)
- Exclude unused modules with `--exclude-module` flag
- Enable UPX compression (if UPX is installed)

### Runtime Issues

**Problem**: Console window appears briefly when launching

**Solution**: Make sure you're using `--windowed` flag (or `console=False` in .spec file). The build scripts already include this.

**Problem**: Game window appears blank or doesn't render correctly

**Solution**: This can happen on Windows with dark mode enabled. Try running from command line first to check for errors. If the issue persists, it may be a Tkinter/dark mode interaction.

**Problem**: Timer doesn't start or count incorrectly

**Solution**: Make sure you're clicking on a cell first - the timer starts on your first click, not when the window opens.

## Development

### Project Structure

```
Minedetector/
├── main.py              # Application entry point
├── src/
│   ├── game/           # Game logic modules
│   ├── ui/             # UI components
│   └── models/         # Data models
├── tests/              # Test suite
├── requirements.txt    # Development dependencies
├── build-prod.sh       # Production build script (Unix/Linux)
├── build-prod.bat      # Production build script (Windows)
├── build-dev.sh        # Development build script (Unix/Linux)
├── build-dev.bat       # Development build script (Windows)
└── main.spec           # PyInstaller configuration (auto-generated)
```

### Running Tests

Run all tests:
```bash
pytest tests/ -v
```

Run tests with coverage:
```bash
pytest tests/ -v --cov=src --cov-report=term-missing
```

## Gameplay

1. **First build** (generates `main.spec`):
   ```bash
   python -m PyInstaller --onefile --windowed --name=Minedetector main.py
   ```

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

## Acknowledgments

- Original Minedetector game by Microsoft
- Built with Python and Tkinter
- Packaged with PyInstaller
