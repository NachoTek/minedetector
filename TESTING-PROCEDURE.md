# Testing Procedure for Minesweeper Development Build Executable

## Current Status

⚠️ **Environment Limitation**: The development build executable (`dist/minedetector/minedetector.exe`) could not be created in this worktree environment due to security restrictions that prevent running Python/pip commands.

### What Was Completed
- ✅ `main.spec` file created with proper PyInstaller configuration
- ✅ Build scripts created (`build-dev.sh` and `build-dev.bat`)
- ✅ All application modules documented in spec file
- ✅ `console=False` configured for windowed mode

### What Requires External Execution
The actual PyInstaller build must be executed in an unrestricted environment:
```bash
pyinstaller --onedir --windowed --name=minedetector main.py
```

This will create: `dist/minedetector/minedetector.exe`

---

## Testing Procedure (To Be Executed After Build)

### Prerequisites
1. PyInstaller must be installed: `pip install -r requirements.txt`
2. Build command executed: `pyinstaller --onedir --windowed --name=minedetector main.py`
3. Executable created: `dist/minedetector/minedetector.exe`

### Test Environment
- **Operating System**: Windows 10 or 11
- **Required**: No Python installation needed (testing standalone execution)
- **Optional**: Test on machine without Python installed to verify portability

---

## Manual Verification Checklist

### 1. Launch Verification

**Test Case**: Application launches correctly
**Steps**:
1. Navigate to `dist/minedetector/` directory
2. Double-click `minedetector.exe`
3. Observe the application startup

**Expected Results**:
- ✅ Application window opens within 2-3 seconds
- ✅ No console window appears (black command prompt window)
- ✅ Only the game window is visible
- ✅ Window title displays "Minesweeper"
- ✅ No error messages or crash dialogs

**Failure Indicators**:
- ❌ Console window visible → `console=False` not working
- ❌ Application crashes → Missing dependencies or imports
- ❌ Error dialogs → Review with `--console` flag for debugging

---

### 2. Game Board Rendering

**Test Case**: Game board renders correctly on startup
**Steps**:
1. Launch the application
2. Visually inspect the game window

**Expected Results**:
- ✅ Game grid visible with cells (default: 9x9 for Beginner difficulty)
- ✅ Top menu bar visible with "Game" menu
- ✅ Mine counter displays "010" (10 mines for Beginner)
- ✅ Timer displays "000"
- ✅ Reset button (face icon) visible in center top
- ✅ All cells are covered/unrevealed
- ✅ Window size appropriate for board (no excessive scrolling)

**Visual Verification**:
```
┌─────────────────────────────┐
│ Game                        │
├─────┬───┬─────┬─────────────┤
│ 010 │ 🙂 │ 000 │             │
├─────┴───┴─────┴─────────────┤
│ ▢ ▢ ▢ ▢ ▢ ▢ ▢ ▢ ▢         │
│ ▢ ▢ ▢ ▢ ▢ ▢ ▢ ▢ ▢         │
│ ▢ ▢ ▢ ▢ ▢ ▢ ▢ ▢ ▢         │
│ ▢ ▢ ▢ ▢ ▢ ▢ ▢ ▢ ▢         │
│ ▢ ▢ ▢ ▢ ▢ ▢ ▢ ▢ ▢         │
│ ▢ ▢ ▢ ▢ ▢ ▢ ▢ ▢ ▢         │
│ ▢ ▢ ▢ ▢ ▢ ▢ ▢ ▢ ▢         │
│ ▢ ▢ ▢ ▢ ▢ ▢ ▢ ▢ ▢         │
│ ▢ ▢ ▢ ▢ ▢ ▢ ▢ ▢ ▢         │
└─────────────────────────────┘
```

---

### 3. Menu Bar Functionality

**Test Case**: Menu bar works correctly
**Steps**:
1. Click "Game" menu
2. Verify menu options appear
3. Test each difficulty level

**Expected Results**:
- ✅ Clicking "Game" shows dropdown menu
- ✅ Menu items visible:
  - Beginner (default, 9x9, 10 mines)
  - Intermediate (16x16, 40 mines)
  - Expert (16x30, 99 mines)
  - Separator line
  - Exit
- ✅ Selecting different difficulties changes board size
- ✅ Selecting "Exit" closes application cleanly

**Test Each Difficulty**:
- **Beginner**: 9x9 grid, mine counter shows "010"
- **Intermediate**: 16x16 grid, mine counter shows "040"
- **Expert**: 30x16 grid, mine counter shows "099"

---

### 4. Cell Interaction - Left Click (Reveal)

**Test Case**: Left-clicking reveals cells
**Steps**:
1. Start a new game (Beginner difficulty)
2. Left-click on various cells
3. Observe cell behavior

**Expected Results**:
- ✅ Clicking a cell reveals its content
- ✅ Numbered cells (1-8) show mine count correctly
- ✅ Empty cells (0) trigger flood-fill reveal
- ✅ Flood-fill stops at numbered cells and edges
- ✅ First click is never a mine (safe start)
- ✅ Timer starts on first click
- ✅ Revealed cells have different appearance (sunken/flat)

**Test Scenarios**:
1. Click a numbered cell → Shows number (1-8)
2. Click an empty cell → Flood-fill reveals multiple cells
3. Click a mine → Game over state (all mines revealed)

---

### 5. Cell Interaction - Right Click (Flag)

**Test Case**: Right-clicking places flags
**Steps**:
1. Right-click on covered cells
2. Observe flag placement and counter

**Expected Results**:
- ✅ Right-click places a red flag 🚩
- ✅ Flag cannot be placed on revealed cell
- ✅ Mine counter decrements by 1 for each flag
- ✅ Right-clicking a flag removes it
- ✅ Mine counter increments when flag removed
- ✅ Multiple flags can be placed

**Counter Test**:
- Start: "010"
- Place 1 flag: "009"
- Place 3 more flags: "006"
- Remove 1 flag: "007"

---

### 6. Cell Interaction - Chording (Both Buttons)

**Test Case**: Chording reveals adjacent cells
**Steps**:
1. Reveal a numbered cell
2. Place flags equal to the number around it
3. Left-click the numbered cell (or use both buttons)

**Expected Results**:
- ✅ When flag count equals cell number, chording works
- ✅ Clicking numbered cell reveals all adjacent unflagged cells
- ✅ If flags are incorrect, chording triggers mine (game over)
- ✅ Chording doesn't work if flag count doesn't match

**Example**:
1. Reveal a cell showing "3"
2. Place exactly 3 flags around it
3. Click the "3" cell
4. All other adjacent cells reveal automatically

---

### 7. Timer Functionality

**Test Case**: Timer operates correctly
**Steps**:
1. Start a new game
2. Make first click (starts timer)
3. Watch timer count
4. Win or lose game
5. Start new game

**Expected Results**:
- ✅ Timer displays "000" before first click
- ✅ Timer starts on first click
- ✅ Timer increments every second (001, 002, 003...)
- ✅ Timer stops when game is won
- ✅ Timer stops when game is lost
- ✅ Timer resets to "000" on new game
- ✅ Timer maxes out at "999"

**Test Sequence**:
```
First click → Timer starts: 001, 002, 003...
Win game → Timer stops at final time
Click reset → Timer resets to 000
```

---

### 8. Win Condition

**Test Case**: Winning the game
**Steps**:
1. Start a game on Beginner difficulty
2. Reveal all non-mine cells (or flag all mines)
3. Achieve win condition

**Expected Results**:
- ✅ Timer stops when last non-mine cell revealed
- ✅ All mines automatically flagged
- ✅ Reset button changes to sunglasses emoji 😎
- ✅ Game doesn't allow further interaction
- ✅ Winning feels rewarding (visual feedback)

**How to Win Quickly**:
- Use Beginner difficulty (fewer cells)
- Reveal all cells except mines
- Or flag all 10 mines correctly

---

### 9. Loss Condition

**Test Case**: Losing the game
**Steps**:
1. Start a game
2. Click on a mine
3. Observe loss state

**Expected Results**:
- ✅ Clicked mine shown in red
- ✅ All other mines revealed on board
- ✅ Incorrect flags shown with X through them
- ✅ Reset button changes to dead face emoji 😵
- ✅ Game doesn't allow further interaction
- ✅ Timer stops

**Visual Indicators**:
- Clicked mine: 💣 (red background)
- Other mines: 💣 (revealed)
- Wrong flag: 🚩 with ❌

---

### 10. Reset Functionality

**Test Case**: Reset button starts new game
**Steps**:
1. Complete or lose a game
2. Click the face button (reset button)
3. Observe new game state

**Expected Results**:
- ✅ Clicking face button starts new game immediately
- ✅ Timer resets to "000"
- ✅ Mine counter resets to difficulty default
- ✅ New board generates (different mine placement)
- ✅ All cells covered again
- ✅ Face button returns to normal 🙂
- ✅ Works after win or loss

**Test After Win**:
- Win game (face shows 😎)
- Click face button
- New game starts (face returns to 🙂)

**Test After Loss**:
- Lose game (face shows 😵)
- Click face button
- New game starts (face returns to 🙂)

---

### 11. Window Management

**Test Case**: Window controls work
**Steps**:
1. Test window minimize/maximize/close
2. Test window resizing (if allowed)

**Expected Results**:
- ✅ Minimize button hides window
- ✅ Maximize button expands window (if supported)
- ✅ Close button exits application cleanly
- ✅ Window can be moved by dragging title bar
- ✅ Window position is remembered (if applicable)

---

### 12. No Console Window Verification

**Test Case**: Console window is hidden
**Steps**:
1. Launch the executable
2. Open Task Manager (Ctrl+Shift+Esc)
3. Look for minedetector.exe process
4. Check for associated console windows

**Expected Results**:
- ✅ Only one window visible (the game window)
- ✅ No black console/command prompt window
- ✅ Task Manager shows minedetector.exe as main process
- ✅ No python.exe or pythonw.exe processes (should be bundled)

**Additional Verification**:
```powershell
# In PowerShell, check for console processes
Get-Process | Where-Object {$_.ProcessName -like "*mine*"}
# Should show: Minesweeper (not python or console)
```

---

### 13. Performance Check

**Test Case**: Application performs well
**Steps**:
1. Start the application
2. Play through a complete game
3. Switch to Expert difficulty (largest board)
4. Make multiple rapid clicks

**Expected Results**:
- ✅ Application launches in < 3 seconds
- ✅ No noticeable lag when clicking cells
- ✅ Flood-fill reveals cells instantly
- ✅ Timer updates smoothly every second
- ✅ No freezing or hanging
- ✅ Memory usage is reasonable (< 100MB)

**Expert Board Test**:
- Switch to Expert (30x16 = 480 cells)
- Test rapid clicking
- Test flood-fill on large empty areas
- Should remain responsive

---

### 14. Standalone Execution Test

**Test Case**: Runs without Python installed
**Steps**:
1. Copy entire `dist/minedetector/` folder to a different location
2. **Critical Test**: Copy to a machine WITHOUT Python installed
3. Run `minedetector.exe` from new location
4. Test basic functionality

**Expected Results**:
- ✅ Application launches successfully
- ✅ No "Python not found" errors
- ✅ No missing DLL errors
- ✅ All features work identically
- ✅ No external dependencies required

**Test Locations**:
- Desktop
- Downloads folder
- USB drive (true portability test)
- Different Windows machine

---

## Debugging Failed Tests

### If Application Won't Launch

1. **Rebuild with console for error messages**:
   ```bash
   pyinstaller --onedir --console --name=minedetector main.py
   ```

2. **Run from command line to see errors**:
   ```cmd
   cd dist\Minesweeper
   minedetector.exe
   ```

3. **Check for common issues**:
   - Missing imports → Add to `hiddenimports` in main.spec
   - Missing data files → Add to `datas` in main.spec
   - Tkinter not found → Ensure Python includes tkinter

### If Console Window Appears

1. **Check main.spec**: Verify `console=False`
2. **Rebuild with windowed flag**:
   ```bash
   pyinstaller --onedir --windowed --name=minedetector --clean main.py
   ```

### If Features Don't Work

1. **Compare to Python version**: Run `python main.py` and test same feature
2. **If Python version works but .exe doesn't**:
   - Missing module in hiddenimports
   - Missing data file in datas
   - Check PyInstaller warnings during build

3. **Enable debug mode**:
   ```bash
   pyinstaller --onedir --windowed --debug=all --name=minedetector main.py
   ```

---

## Test Report Template

After testing, complete this report:

```
Minesweeper Development Build Test Report
===========================================

Build Information:
- Build Date: [DATE]
- Build Command: pyinstaller --onedir --windowed --name=minedetector main.py
- Executable Location: dist/minedetector/minedetector.exe
- Executable Size: [SIZE] MB
- Test Environment: Windows [VERSION]

Test Results:

1. Launch Verification: [PASS/FAIL] - [NOTES]
2. Game Board Rendering: [PASS/FAIL] - [NOTES]
3. Menu Bar Functionality: [PASS/FAIL] - [NOTES]
4. Cell Reveal (Left Click): [PASS/FAIL] - [NOTES]
5. Cell Flagging (Right Click): [PASS/FAIL] - [NOTES]
6. Chording: [PASS/FAIL] - [NOTES]
7. Timer Functionality: [PASS/FAIL] - [NOTES]
8. Win Condition: [PASS/FAIL] - [NOTES]
9. Loss Condition: [PASS/FAIL] - [NOTES]
10. Reset Functionality: [PASS/FAIL] - [NOTES]
11. Window Management: [PASS/FAIL] - [NOTES]
12. No Console Window: [PASS/FAIL] - [NOTES]
13. Performance: [PASS/FAIL] - [NOTES]
14. Standalone Execution: [PASS/FAIL] - [NOTES]

Overall Status: [PASS/FAIL]

Issues Found:
- [List any issues or bugs]

Recommendations:
- [Any suggestions for improvements]

Next Steps:
- [Ready for production build? Need fixes?]
```

---

## Sign-off Criteria

The development build is considered **PASSING** when:
- ✅ All 14 test cases pass
- ✅ No crashes or error messages during normal use
- ✅ All game features work identically to Python version
- ✅ No console window visible
- ✅ Application runs standalone without Python installed

**Failure Criteria**:
- ❌ Any crash on startup or during use
- ❌ Console window visible
- ❌ Missing features or broken functionality
- ❌ Requires Python installation to run

---

## Notes for Next Phase

Once this development build passes all tests, proceed to:
1. **Phase 3**: Create production single-file build with `--onefile`
2. **Phase 4**: Update documentation in README.md
3. **Phase 5**: Comprehensive testing of production build
