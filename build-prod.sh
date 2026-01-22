#!/bin/bash
# Build script for Minedetector production executable (single-file portable)
# This script should be run in an unrestricted environment

echo "Building Minedetector production executable (onefile mode)..."
echo "This creates a single portable .exe file with bundled Python interpreter"

# Check if PyInstaller is installed
if ! python -m PyInstaller --version &> /dev/null; then
    echo "PyInstaller not found. Installing..."
    pip install -r requirements.txt
fi

# Run PyInstaller with onefile mode for portable executable
# --onefile: Creates single executable (vs --onedir for folder)
# --windowed: Hides console window (critical for Tkinter GUI)
# --clean: Clears build cache for fresh output
# --name: Sets output executable name
# NOTE: Using 'python -m PyInstaller' instead of 'pyinstaller' to avoid PATH issues
python -m PyInstaller --onefile --windowed --name=Minedetector --clean main.py

# Check if build was successful
if [ -f "dist/Minedetector.exe" ]; then
    echo "✓ Build successful!"
    echo "✓ Executable: dist/Minedetector.exe"
    echo "✓ Size: $(ls -lh dist/Minedetector.exe | awk '{print $5}')"
    echo ""
    echo "Production executable ready for distribution!"
    echo "This is a portable single-file executable - no installation required."
    ls -lh dist/Minedetector.exe
else
    echo "✗ Build failed"
    exit 1
fi
