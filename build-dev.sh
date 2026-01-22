#!/bin/bash
# Build script for Minesweeper development executable
# This script should be run in an unrestricted environment

echo "Building Minesweeper development executable (onedir mode)..."

# Check if PyInstaller is installed
if ! python -m PyInstaller --version &> /dev/null; then
    echo "PyInstaller not found. Installing..."
    pip install -r requirements.txt
fi

# Run PyInstaller with onedir mode for faster development builds
# NOTE: Using 'python -m PyInstaller' instead of 'pyinstaller' to avoid PATH issues
python -m PyInstaller --onedir --windowed --name=Minesweeper main.py

# Check if build was successful
if [ -f "dist/Minesweeper/Minesweeper.exe" ]; then
    echo "✓ Build successful!"
    echo "✓ Executable: dist/Minesweeper/Minesweeper.exe"
    echo "✓ Spec file: main.spec"
    ls -lh dist/Minesweeper/Minesweeper.exe
    ls -lh main.spec
else
    echo "✗ Build failed"
    exit 1
fi
