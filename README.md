# Minesweeper

A classic Minesweeper game built with Python and Tkinter. This desktop application recreates the timeless puzzle game with all the familiar features you know and love.

![Minesweeper](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

## Features

- **Classic Gameplay**: All the traditional Minesweeper mechanics
  - Left-click to reveal cells
  - Right-click to place flags
  - Chording: Click a revealed number with the correct flag count to reveal surrounding cells
  - Flood-fill reveals on empty cells

- **Multiple Difficulty Levels**:
  - Beginner (9×9 grid, 10 mines)
  - Intermediate (16×16 grid, 40 mines)
  - Expert (30×16 grid, 99 mines)

- **Game Statistics**:
  - Real-time timer that starts on your first click
  - Mine counter that decreases as you place flags
  - Win/loss detection with visual feedback

- **Intuitive Controls**:
  - Reset button (face icon) to start a new game
  - Menu bar for difficulty selection
  - Keyboard shortcuts for common actions

## Running from Source

### Prerequisites

- Python 3.8 or higher
- Tkinter (usually included with Python installations)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd minedetector
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

```bash
pip install -r requirements.txt
```

This will install PyInstaller, which is needed to create the executable.

### Build Instructions

#### Option 1: Quick Build (Recommended)

Use the provided build scripts for automated building:

**On Windows (Command Prompt)**:
```bash
build-prod.bat
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
- Output the executable to `dist/Minesweeper.exe`

#### Option 2: Manual Build

If you prefer to build manually or customize the build process:

**Production Build (Single Portable Executable)**:
```bash
python -m PyInstaller --onefile --windowed --name=Minesweeper --clean main.py
```

**Development Build (Faster, Easier to Debug)**:
```bash
python -m PyInstaller --onedir --windowed --name=Minesweeper --clean main.py
```

**Debug Build (Shows Console for Error Messages)**:
```bash
python -m PyInstaller --onefile --console --name=Minesweeper --clean main.py
```

**Note**: Using `python -m PyInstaller` instead of `pyinstaller` directly ensures the command works regardless of your system PATH configuration.

### Build Flags Explained

- `--onefile`: Creates a single portable executable (recommended for distribution)
- `--onedir`: Creates a folder with the executable and all dependencies (faster builds, better for development)
- `--windowed` or `--noconsole`: Hides the console window (required for GUI applications)
- `--console`: Shows the console window (useful for debugging)
- `--clean`: Cleans the build cache before building (ensures fresh output)
- `--name=Minesweeper`: Sets the output executable name

### Output Location

After building, you'll find the executable here:
- **Single-file build**: `dist/Minesweeper.exe`
- **Directory build**: `dist/Minesweeper/Minesweeper.exe`

The single-file executable is typically 5-15 MB in size, as it bundles the entire Python runtime and Tkinter library.

### Testing the Executable

1. Navigate to the `dist` folder
2. Double-click `Minesweeper.exe`
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

**The executable is safe** - it's simply the Minesweeper game with no malicious behavior. If your antivirus blocks it:

1. Check your antivirus quarantine/exclusions settings
2. Add an exception for `Minesweeper.exe`
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
python -m PyInstaller --onefile --console --name=Minesweeper --clean main.py
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
minedetector/
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

```bash
pytest tests/ -v
```

### Building from Scratch

If you want to understand or modify the build process:

1. **First build** (generates `main.spec`):
   ```bash
   python -m PyInstaller --onefile --windowed --name=Minesweeper main.py
   ```

2. **Edit `main.spec`** (if needed):
   - Add data files with `datas=[('src', 'src')]`
   - Add hidden imports with `hiddenimports=['module.name']`
   - Customize EXE options

3. **Rebuild using spec file**:
   ```bash
   python -m PyInstaller --clean main.spec
   ```

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- Original Minesweeper game by Microsoft
- Built with Python and Tkinter
- Packaged with PyInstaller
