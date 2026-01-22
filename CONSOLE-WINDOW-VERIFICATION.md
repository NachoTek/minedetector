# Console Window Verification - Production Build

## Subtask: 3-2 - Verify Console Window is Hidden

## Status: Configuration Verified, Execution Blocked by Environment

---

## Build Configuration Verification ✅

### Production Build Script (build-prod.bat)

**Line 20**: Contains the critical `--windowed` flag
```batch
pyinstaller --onefile --windowed --name=minedetector --clean main.py
```

**What this does:**
- `--windowed`: Hides the console window for GUI applications (Tkinter)
- `--onefile`: Creates a single portable executable
- `--clean`: Clears build cache for fresh output
- `--name=minedetector`: Sets output executable name

### Spec File Configuration (main.spec)

**Line 65**: Sets `console=False`
```python
console=False,  # Critical: Hide console window for Tkinter GUI application
```

**What this does:**
- Prevents the black console/command prompt window from appearing
- Application runs as a pure GUI application
- Standard output/error messages are suppressed

---

## Verification Required After Build

Since the production executable (`dist/minedetector.exe`) cannot be created in this restricted environment, the following verification must be performed when the build is executed in an unrestricted environment.

### Manual Verification Steps

1. **Build the executable:**
   ```cmd
   build-prod.bat
   # or
   pyinstaller --onefile --windowed --name=minedetector --clean main.py
   ```

2. **Run the executable:**
   ```cmd
   cd dist
   minedetector.exe
   ```
   Or simply double-click `dist/minedetector.exe` in File Explorer

3. **Observe the application launch:**
   - ✅ **PASS**: Only the game window appears
   - ❌ **FAIL**: A black console window also appears

### Expected Results

#### What You SHOULD See (✅ PASS):
- One window: The Mine Detector game window
- Window title: "Mine Detector"
- Game board with grid, menu bar, mine counter, timer
- No black console/command prompt window
- Clean GUI-only application

#### What You SHOULD NOT See (❌ FAIL):
- Black command prompt window behind or beside the game window
- Console window with text or error messages
- Multiple windows in taskbar (should be only one)
- Any console-based output

---

## Technical Background

### Why --windowed is Critical for Tkinter

Tkinter is a GUI toolkit that creates its own windows. When a Tkinter application is bundled with PyInstaller:

1. **Without --windowed** (or with `console=True`):
   - Windows creates a console window for stdin/stdout/stderr
   - The black console appears behind or beside the GUI
   - Unprofessional appearance for a GUI application
   - User may think something is wrong

2. **With --windowed** (or `console=False`):
   - Windows runs the application as a GUI-only subsystem
   - No console window is created
   - Application appears as a professional GUI application
   - stdin/stdout/stderr are suppressed (no console output)

### How the --windowed Flag Works

The `--windowed` flag tells PyInstaller to:
1. Set the Windows subsystem to `WINDOWS` (not `CONSOLE`)
2. Set `console=False` in the generated .spec file
3. Suppress the console window creation at OS level

This is equivalent to the Windows PE header setting:
```
Subsystem: 0x0002 (WINDOWS_GUI)
```

---

## Debugging If Console Appears

If the console window appears when running the executable:

### Solution 1: Verify Build Command

Ensure the build command includes `--windowed`:
```bash
pyinstaller --onefile --windowed --name=minedetector --clean main.py
```

### Solution 2: Check main.spec

Verify line 65 of `main.spec` has:
```python
console=False,
```

If it shows `console=True`, change it to `False` and rebuild:
```bash
pyinstaller --clean main.spec
```

### Solution 3: Rebuild from Scratch

Sometimes the build cache retains old settings:
```bash
# Clean build directories
rmdir /s /q build dist
# Rebuild with --windowed flag
pyinstaller --onefile --windowed --name=minedetector --clean main.py
```

### Solution 4: Temporary Debug Build

If you need to see error messages, build with console:
```bash
pyinstaller --onefile --console --name=minedetector --clean main.py
```
This will show the console and allow you to see any error output. Fix the errors, then rebuild with `--windowed`.

---

## Verification Checklist

After building `dist/minedetector.exe`, verify:

- [ ] Executable exists: `dist/minedetector.exe` (> 5MB)
- [ ] Double-clicking the executable launches the game
- [ ] **Only one window appears** (the game window)
- [ ] **No black console window is visible**
- [ ] Task Manager shows only "minedetector.exe" (no console subprocess)
- [ ] Application behaves identically to `python main.py`
- [ ] No error messages or crash dialogs appear

---

## Test Environment Notes

### Recommended Testing Environments

1. **Primary Development Machine**
   - Where Python and PyInstaller are installed
   - First verification of console hiding

2. **Clean Windows Machine**
   - No Python installation
   - Verifies true standalone execution
   - Most realistic end-user environment

3. **Different Windows Versions**
   - Windows 10 (multiple builds if possible)
   - Windows 11 (latest)
   - Ensures compatibility across versions

### Task Manager Verification

1. Launch minedetector.exe
2. Open Task Manager (Ctrl+Shift+Esc)
3. Go to "Details" tab
4. Look for processes:
   - ✅ **PASS**: Only `minedetector.exe` is present
   - ❌ **FAIL**: `minedetector.exe` + `conhost.exe` (console host)

### PowerShell Verification

```powershell
# Check for console-associated processes
Get-Process | Where-Object {$_.ProcessName -like "*mine*"} | Select-Object ProcessName, MainWindowTitle
```

**Expected Output:**
```
ProcessName    MainWindowTitle
-----------    ---------------
Mine Detector    Mine Detector
```

If `MainWindowTitle` is empty or you see multiple processes, the console may be present.

---

## Acceptance Criteria

**✅ Subtask 3-2 is COMPLETE when:**

1. Build configuration is verified (✅ DONE)
   - `build-prod.bat` contains `--windowed` flag
   - `main.spec` contains `console=False`
   - Both files are correctly configured

2. Executable is built in unrestricted environment
   - `dist/minedetector.exe` exists
   - File size is > 5MB (includes bundled Python)

3. Manual verification confirms console is hidden
   - Running executable shows only game window
   - No black console window appears
   - Task Manager shows only minedetector.exe process

**Current Status:**
- ✅ Configuration verified and correct
- ⏳ Executable build requires unrestricted environment
- ⏳ Manual verification requires executable to be built

---

## Next Steps

1. **When in unrestricted environment:**
   ```bash
   build-prod.bat
   ```

2. **Verify console window:**
   - Run `dist/minedetector.exe`
   - Confirm only game window appears
   - Check Task Manager for single process

3. **If console appears:**
   - Review "Debugging If Console Appears" section
   - Fix configuration
   - Rebuild and re-verify

4. **When verification passes:**
   - Mark subtask-3-2 as completed
   - Proceed to subtask-4-1 (Update README.md)

---

## Related Documentation

- **Build Script**: `build-prod.bat` - Production build command with `--windowed`
- **Spec File**: `main.spec` - PyInstaller configuration with `console=False`
- **Test Procedure**: `TESTING-PROCEDURE.md` - Comprehensive testing guide
  - Test Case 1: Launch Verification (includes console check)
  - Test Case 12: No Console Window Verification (dedicated console test)
- **Spec**: `./.auto-claude/specs/003-package-the-application-as-a-portable-single-windo/spec.md`
  - Lines 126-127: `console=False` (or `--windowed`) is critical for Tkinter

---

**Document Version:** 1.0
**Created:** 2025-01-22
**Purpose:** Verification procedure for subtask-3-2 (console window hiding in production build)
**Status:** Configuration verified, awaiting executable build for final verification
