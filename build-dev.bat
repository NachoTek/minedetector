@echo off
REM Build script for Minedetector development executable (Windows)
REM This script should be run in an unrestricted environment

echo Building Minedetector development executable (onedir mode)...

REM Check if PyInstaller is installed
python -m PyInstaller --version >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo PyInstaller not found. Installing...
    pip install -r requirements.txt
)

REM Run PyInstaller with onedir mode for faster development builds
REM NOTE: Using 'python -m PyInstaller' instead of 'pyinstaller' to avoid PATH issues
python -m PyInstaller --onedir --windowed --name=Minedetector main.py

REM Check if build was successful
if exist "dist\Minedetector\Minedetector.exe" (
    echo ✓ Build successful!
    echo ✓ Executable: dist\Minedetector\Minedetector.exe
    echo ✓ Spec file: main.spec
    dir dist\Minedetector\Minedetector.exe
    dir main.spec
) else (
    echo ✗ Build failed
    exit /b 1
)
