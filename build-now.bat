@echo off
REM Immediate build script for QA fix session 10
REM This script builds the required onefile executable

echo ===================================================
echo Building Minedetector portable executable
echo ===================================================
echo.

REM Use full path to Python to avoid PATH issues
set PYTHON_EXE=C:\Program Files\Python311\python.exe

echo Step 1: Checking Python...
"%PYTHON_EXE%" --version
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python not found
    exit /b 1
)

echo.
echo Step 2: Installing/Checking PyInstaller...
"%PYTHON_EXE%" -m pip install -r requirements.txt --quiet
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to install dependencies
    exit /b 1
)

echo.
echo Step 3: Building portable executable (onefile mode)...
"%PYTHON_EXE%" -m PyInstaller --onefile --windowed --name=Minedetector --clean main.py
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Build failed
    exit /b 1
)

echo.
echo ===================================================
echo Step 4: Verifying build output...
echo ===================================================
if exist "dist\Minedetector.exe" (
    echo SUCCESS: dist\Minedetector.exe created
    dir "dist\Minedetector.exe"
    echo.
    echo Build complete! Executable is ready for testing.
) else (
    echo ERROR: dist\Minedetector.exe was not created
    exit /b 1
)

echo.
echo ===================================================
echo Next steps:
echo 1. Test the executable: dist\Minedetector.exe
echo 2. Verify no console window appears
echo 3. Test all game features
echo 4. Test on machine without Python
echo ===================================================
