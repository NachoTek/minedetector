@echo off
REM Build script for minedetector development executable (Windows)
REM This script should be run in an unrestricted environment

echo Building minedetector development executable (onedir mode)...

REM Check if PyInstaller is installed
python -m PyInstaller --version >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo PyInstaller not found. Installing...
    pip install -r requirements.txt
)

REM Run PyInstaller with onedir mode for faster development builds
REM NOTE: Using 'python -m PyInstaller' instead of 'pyinstaller' to avoid PATH issues
python -m PyInstaller --onedir --windowed --name=minedetector main.py

REM Check if build was successful
if exist "dist\minedetector\minedetector.exe" (
    echo ✓ Build successful!
    echo ✓ Executable: dist\minedetector\minedetector.exe
    echo ✓ Spec file: main.spec
    dir dist\minedetector\minedetector.exe
    dir main.spec
) else (
    echo ✗ Build failed
    exit /b 1
)
