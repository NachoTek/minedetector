#!/bin/bash
# Build script for Minesweeper production executable (single-file portable)
# This script should be run in an unrestricted environment

echo "Building Minesweeper production executable (onefile mode)..."
echo "This creates a single portable .exe file with bundled Python interpreter"

# Check if PyInstaller is installed
if ! command -v pyinstaller &> /dev/null; then
    echo "PyInstaller not found. Installing..."
    pip install -r requirements.txt
fi

# Run PyInstaller with onefile mode for portable executable
# --onefile: Creates single executable (vs --onedir for folder)
# --windowed: Hides console window (critical for Tkinter GUI)
# --clean: Clears build cache for fresh output
# --name: Sets output executable name
pyinstaller --onefile --windowed --name=Minesweeper --clean main.py

# Check if build was successful
if [ -f "dist/Minesweeper.exe" ]; then
    echo "✓ Build successful!"
    echo "✓ Executable: dist/Minesweeper.exe"
    echo "✓ Size: $(ls -lh dist/Minesweeper.exe | awk '{print $5}')"
    echo ""
    echo "Production executable ready for distribution!"
    echo "This is a portable single-file executable - no installation required."
    ls -lh dist/Minesweeper.exe
else
    echo "✗ Build failed"
    exit 1
fi
