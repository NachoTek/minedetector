#!/bin/bash
# Build script for minedetector development executable
# This script should be run in an unrestricted environment

echo "Building minedetector development executable (onedir mode)..."

# Check if PyInstaller is installed
if ! python -m PyInstaller --version &> /dev/null; then
    echo "PyInstaller not found. Installing..."
    pip install -r requirements.txt
fi

# Run PyInstaller with onedir mode for faster development builds
# NOTE: Using 'python -m PyInstaller' instead of 'pyinstaller' to avoid PATH issues
python -m PyInstaller --onedir --windowed --name=minedetector main.py

# Check if build was successful
if [ -f "dist/minedetector/minedetector.exe" ]; then
    echo "✓ Build successful!"
    echo "✓ Executable: dist/minedetector/minedetector.exe"
    echo "✓ Spec file: main.spec"
    ls -lh dist/minedetector/minedetector.exe
    ls -lh main.spec
else
    echo "✗ Build failed"
    exit 1
fi
