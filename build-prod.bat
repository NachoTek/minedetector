@echo off
REM Build script for minedetector production executable (Windows - single-file portable)
REM This script should be run in an unrestricted environment

echo Building minedetector production executable (onefile mode)...
echo This creates a single portable .exe file with bundled Python interpreter

REM Check if PyInstaller is installed
python -m PyInstaller --version >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo PyInstaller not found. Installing...
    pip install -r requirements.txt
)

REM Run PyInstaller with onefile mode for portable executable
REM --onefile: Creates single executable (vs --onedir for folder)
REM --windowed: Hides console window (critical for Tkinter GUI)
REM --clean: Clears build cache for fresh output
REM --name: Sets output executable name
REM NOTE: Using 'python -m PyInstaller' instead of 'pyinstaller' to avoid PATH issues
python -m PyInstaller --onefile --windowed --name=minedetector --clean main.py

REM Check if build was successful
if exist "dist\minedetector.exe" (
    echo ✓ Build successful!
    echo ✓ Executable: dist\minedetector.exe
    dir dist\minedetector.exe
    echo.
    echo Production executable ready for distribution!
    echo This is a portable single-file executable - no installation required.
) else (
    echo ✗ Build failed
    exit /b 1
)
