# Subtask 5-2: Standalone Execution Verification Guide

## Overview

This document provides comprehensive procedures for verifying that the minedetector.exe executable is truly standalone and portable, requiring no Python installation or external dependencies.

**Critical Test**: This is the **core requirement** of the entire packaging task. The executable must run from any location on any Windows machine without requiring Python or any dependencies.

## Prerequisites

### Build Requirements
- Production executable must exist: `dist/minedetector.exe`
- Build command: `pyinstaller --onefile --windowed --name=minedetector --clean main.py`
- Expected size: 5-15 MB (includes bundled Python interpreter and Tkinter)

### Test Environments
1. **Primary Test Environment** (Required):
   - Clean Windows machine (Windows 10 or 11)
   - NO Python installation
   - NO dependencies installed
   - Fresh system or VM preferred

2. **Secondary Test Environments** (Recommended):
   - Windows machine with Python installed (verify it doesn't use system Python)
   - Different Windows versions (10, 11)
   - Different user profiles (standard user, admin)

3. **Test Locations** (All Required):
   - User Desktop
   - User Downloads folder
   - External drive (USB flash drive)
   - Network share (if available)
   - Different local drive (e.g., D:\ drive if C:\ is system drive)

## Verification Procedures

### Procedure 1: Basic Portability Test

**Objective**: Verify executable runs from different directories without installation.

#### Step 1: Copy to Test Locations
```powershell
# On Windows
copy dist\minedetector.exe %USERPROFILE%\Desktop\
copy dist\minedetector.exe %USERPROFILE%\Downloads\
# If USB available
copy dist\minedetector.exe E:\\
```

#### Step 2: Run from Desktop
1. Navigate to Desktop
2. Double-click `minedetector.exe`
3. **Verification Points**:
   - [ ] Application launches successfully
   - [ ] No error messages about missing Python
   - [ ] No "missing DLL" errors
   - [ ] Game window appears
   - [ ] Game board renders correctly

#### Step 3: Run from Downloads
1. Navigate to Downloads folder
2. Double-click `minedetector.exe`
3. **Verification Points**:
   - [ ] Application launches successfully
   - [ ] No errors about missing dependencies
   - [ ] Game functions identically to Desktop run

#### Step 4: Run from External Drive (if available)
1. Navigate to USB drive
2. Double-click `minedetector.exe`
3. **Verification Points**:
   - [ ] Application launches from external drive
   - [ ] No performance degradation
   - [ ] All features work correctly

**Acceptance Criteria**: All verification points must pass for all test locations.

---

### Procedure 2: Clean Machine Verification (Critical)

**Objective**: Verify executable runs on Windows without Python installed.

#### Test Setup
1. Use a Windows machine or VM that has NEVER had Python installed
2. Or temporarily uninstall Python (not recommended for primary development machine)
3. Verify Python is not in PATH:
   ```powershell
   python --version
   # Expected: 'python' is not recognized as an internal or external command
   ```

#### Test Execution
1. Copy `minedetector.exe` to Desktop
2. Double-click to run
3. **Verification Points**:
   - [ ] Application launches without any Python installation
   - [ ] No error dialogs appear
   - [ ] Task Manager shows only `minedetector.exe` process (no `python.exe`)
   - [ ] Game is fully functional

**Acceptance Criteria**: Application runs perfectly on machine without Python.

---

### Procedure 3: No External Dependencies Test

**Objective**: Verify executable has no external dependencies beyond Windows OS.

#### Step 1: Dependency Walker Analysis (Optional)
1. Download Dependencies Walker (depends.exe) or use Visual Studio's dependency tool
2. Open `minedetector.exe` in Dependency Walker
3. **Verification Points**:
   - [ ] No missing DLL dependencies
   - [ ] Only Windows system DLLs listed (kernel32.dll, user32.dll, etc.)
   - [ ] No Python DLLs in system32 required

#### Step 2: Process Monitor Analysis (Optional)
1. Download Process Monitor from Sysinternals
2. Set filters to Process Name is `minedetector.exe`
3. Run the executable
4. **Verification Points**:
   - [ ] No attempts to load Python DLLs from system paths
   - [ ] No file not found errors for Python libraries
   - [ ] No attempts to access Python installation directories

**Acceptance Criteria**: No external dependencies beyond Windows OS.

---

### Procedure 4: Cross-Drive Portability Test

**Objective**: Verify executable runs from different drive letters.

#### Test Execution
1. If you have multiple drives (C:, D:, etc.) or a USB drive:
2. Copy `minedetector.exe` to each drive:
   ```powershell
   copy dist\minedetector.exe D:\Temp\minedetector.exe
   copy dist\minedetector.exe E:\minedetector.exe
   ```
3. Run from each location
4. **Verification Points**:
   - [ ] Runs from C: drive
   - [ ] Runs from D: drive (if available)
   - [ ] Runs from USB/removable drive (if available)
   - [ ] No path-dependent errors
   - [ ] No "working directory" issues

**Acceptance Criteria**: Application runs from any drive letter.

---

### Procedure 5: Network Share Test (Optional)

**Objective**: Verify executable runs from network share without local installation.

#### Test Execution
1. Copy `minedetector.exe` to a network share:
   ```powershell
   copy dist\minedetector.exe \\server\share\minedetector.exe
   ```
2. Navigate to network share in File Explorer
3. Double-click `minedetector.exe`
4. **Verification Points**:
   - [ ] Application launches from network share
   - [ ] No performance issues
   - [ ] No authentication errors
   - [ ] All features work correctly

**Acceptance Criteria**: Application runs from network share without issues.

---

### Procedure 6: No Installation Required Test

**Objective**: Verify no installation process is needed.

#### Test Execution
1. Copy `minedetector.exe` to a new location
2. Immediately run it (no "installation" steps)
3. **Verification Points**:
   - [ ] No installer required
   - [ ] No configuration needed
   - [ ] No first-time setup wizard
   - [ ] Works immediately after copy
   - [ ] No registry changes required
   - [ ] No administrator privileges required (unless UAC blocks)

**Acceptance Criteria**: Zero-install experience - copy and run.

---

### Procedure 7: Offline Execution Test

**Objective**: Verify executable runs without internet connection.

#### Test Execution
1. Disconnect from network (disable WiFi, unplug ethernet)
2. Run `minedetector.exe`
3. **Verification Points**:
   - [ ] Application launches offline
   - [ ] No attempts to connect to internet
   - [ ] No errors about missing network resources
   - [ ] All game features work offline

**Acceptance Criteria**: Application works completely offline.

---

## Comprehensive Verification Checklist

Complete this checklist after performing all procedures:

### Environment Tests
- [ ] Runs on Windows 10
- [ ] Runs on Windows 11 (if available)
- [ ] Runs on machine WITHOUT Python installed (CRITICAL)
- [ ] Runs on machine WITH Python installed (uses bundled Python)
- [ ] Runs from user profile without admin privileges

### Location Tests
- [ ] Runs from Desktop
- [ ] Runs from Downloads folder
- [ ] Runs from Documents folder
- [ ] Runs from external USB drive
- [ ] Runs from different drive letter (D:, E:, etc.)
- [ ] Runs from network share (optional)

### Independence Tests
- [ ] No Python installation required
- [ ] No dependencies required
- [ ] No installation process needed
- [ ] No internet connection required
- [ ] No configuration files needed
- [ ] No registry changes needed
- [ ] No administrator privileges needed (unless UAC requires)

### Functionality Tests
- [ ] Game launches from all test locations
- [ ] Game features work identically from all locations
- [ ] No performance degradation from different locations
- [ ] No path-dependent errors
- [ ] No "missing file" errors

---

## Debugging Common Issues

### Issue: "Python not found" Error

**Symptom**: Application shows error about Python not being installed.

**Diagnosis**:
1. Check executable was built with `--onefile` flag
2. Verify PyInstaller bundled Python interpreter
3. Check file size (should be 5-15 MB, not < 1 MB)

**Solution**:
- Rebuild with: `pyinstaller --onefile --windowed --name=minedetector --clean main.py`
- Verify PyInstaller version >= 6.0

---

### Issue: "Missing DLL" Error

**Symptom**: Application fails to start due to missing DLL.

**Diagnosis**:
1. Run Dependency Walker on executable
2. Check which DLL is missing
3. Determine if it's Windows system DLL or application dependency

**Solution**:
- If system DLL: Install Windows updates or Visual C++ Redistributable
- If application dependency: Add to spec file with `--hidden-import` or `--add-binary`

---

### Issue: Application Won't Run from External Drive

**Symptom**: Works from C: drive but not from USB drive.

**Diagnosis**:
1. Check if external drive is NTFS formatted (vs FAT32)
2. Check drive permissions
3. Check antivirus software blocking execution from USB

**Solution**:
- Try different USB drive
- Temporarily disable antivirus for testing
- Check Windows security settings for external drive execution

---

### Issue: Windows SmartScreen Warning

**Symptom**: "Windows protected your PC" warning appears.

**Diagnosis**: This is EXPECTED for unsigned executables. Not a bug.

**Solution**:
1. Click "More info"
2. Click "Run anyway"
3. Document this in README.md (already done)

**Note**: This is normal and should be documented for users, not "fixed".

---

### Issue: Antivirus Blocks Execution

**Symptom**: Antivirus software removes or blocks executable.

**Diagnosis**: PyInstaller executables are sometimes flagged as false positives.

**Solution**:
1. Add executable to antivirus exclusions for testing
2. Upload to VirusTotal.com to check if it's a widespread false positive
3. Document this in README.md (already done)

**Note**: This is expected for unsigned PyInstaller executables.

---

### Issue: Application Crashes on Launch

**Symptom**: Application starts but immediately crashes.

**Diagnosis**:
1. Build with `--console` flag to see error messages
2. Check for missing imports or data files
3. Verify all src/ modules are bundled

**Solution**:
- Run debug build: `pyinstaller --onefile --console --name=minedetector main.py`
- Read error messages in console window
- Fix missing imports or data files
- Rebuild with `--windowed` after debugging

---

## Verification Report Template

After completing all verification procedures, document your results:

```markdown
# Standalone Execution Verification Report

**Date**: [Date]
**Tester**: [Name]
**Executable**: dist/minedetector.exe
**Size**: [Size] MB
**Build Command**: pyinstaller --onefile --windowed --name=minedetector --clean main.py

## Test Environments
- Windows 10: [Pass/Fail] - Version [X.X]
- Windows 11: [Pass/Fail] - Version [X.X]
- Clean machine (no Python): [Pass/Fail]
- Machine with Python: [Pass/Fail]

## Location Tests
- Desktop: [Pass/Fail]
- Downloads: [Pass/Fail]
- External USB: [Pass/Fail]
- Different drive: [Pass/Fail]
- Network share: [Pass/Fail]

## Independence Tests
- No Python required: [Pass/Fail]
- No installation needed: [Pass/Fail]
- Works offline: [Pass/Fail]
- No external dependencies: [Pass/Fail]

## Issues Encountered
1. [Issue description]
   - Location: [Where it occurred]
   - Severity: [Critical/Major/Minor]
   - Status: [Fixed/Documented/Open]

## Conclusion
Overall Result: [PASS/FAIL]

Critical Requirements:
- [ ] Runs without Python installed
- [ ] Runs from any location
- [ ] Truly standalone/portable

Notes: [Any additional observations]
```

---

## Acceptance Criteria

Subtask 5-2 is considered **COMPLETE** when:

1. ✅ Executable runs on machine WITHOUT Python installed (CRITICAL)
2. ✅ Executable runs from Desktop
3. ✅ Executable runs from Downloads folder
4. ✅ Executable runs from external drive (USB)
5. ✅ No installation or configuration required
6. ✅ No external dependencies beyond Windows OS
7. ✅ Works offline without internet connection
8. ✅ All game features work identically to running from source

---

## Next Steps

After successful verification:

1. **Document Results**: Fill out Verification Report Template above
2. **Update README.md**: Add verified standalone execution status (if not already present)
3. **Prepare for Distribution**:
   - Consider code signing certificate (future enhancement)
   - Update distribution notes with verification results
   - Document any platform-specific issues found

---

## Troubleshooting Quick Reference

| Symptom | Most Likely Cause | Quick Check |
|---------|------------------|-------------|
| "Python not required" error | Built without bundling | Check file size < 1 MB |
| Missing DLL error | System dependency missing | Install VC++ Redistributable |
| Won't run from USB | Drive format or permissions | Try NTFS drive |
| SmartScreen warning | Unsigned executable | Expected - click "Run anyway" |
| Antivirus blocks it | False positive | Add to exclusions, check VirusTotal |
| Crashes on launch | Missing imports/data | Build with --console to debug |
| Slow startup | Antivirus scanning | Add to exclusions |

---

## Related Documentation

- **TESTING-PROCEDURE.md**: Development build testing (14 test cases, onedir mode)
- **CONSOLE-WINDOW-VERIFICATION.md**: Console hiding verification (subtask-3-2)
- **SUBTASK-5-1-VERIFICATION-GUIDE.md**: Game feature verification (12 E2E steps)
- **README.md**: Distribution notes and user documentation

---

**Document Version**: 1.0
**Last Updated**: 2025-01-22
**Subtask**: 5-2 - Verify standalone execution (no Python required)
**Status**: Documentation complete, awaiting executable build for execution
