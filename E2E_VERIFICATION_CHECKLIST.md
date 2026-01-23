# End-to-End Verification Checklist
## Minesweeper Clone - Complete Gameplay Verification

**Document:** E2E Verification Checklist
**Date:** 2026-01-18
**Phase:** Integration and Testing (Phase 6, Subtask 6-9)
**Status:** Ready for Manual Verification

---

## Overview

This document provides a comprehensive checklist for manual end-to-end verification of the Minesweeper clone. The automated tests in `tests/test_e2e_gameplay.py` verify the game logic through code, while this checklist verifies the complete user experience through the GUI.

**How to Run:**
```bash
python main.py
```

---

## Test Environment Setup

- [ ] Python 3.8+ installed
- [ ] Tkinter available (built-in with Python)
- [ ] All dependencies installed: `pip install -r requirements.txt`
- [ ] Test files exist: `tests/test_e2e_gameplay.py`

---

## Verification 1: Application Launch

### Expected Behavior
- [ ] Application window opens without errors
- [ ] Window title displays "Minesweeper"
- [ ] Game menu visible in menu bar
- [ ] Default difficulty is Beginner (9x9 grid, 10 mines)

### Visual Verification
- [ ] Mine counter shows "010" (10 mines remaining)
- [ ] Timer shows "000" (0 seconds elapsed)
- [ ] Reset button shows happy face icon 🙂
- [ ] 9x9 grid of cells visible (81 total cells)
- [ ] All cells appear unrevealed (covered state)

### Menu Verification
- [ ] Click "Game" menu
- [ ] Menu shows: Beginner, Intermediate, Expert, separator, Exit
- [ ] "Beginner" has checkmark or indicator (active difficulty)

**Result:** ✅ PASS / ❌ FAIL

---

## Verification 2: Beginner Difficulty Gameplay

### 2.1 First-Click Safety (20 Games)

**Procedure:**
1. Close and restart application
2. Click various cells on the board
3. Verify first click never hits a mine

**Test Positions:**
- [ ] Game 1: Click center cell (4,4) → Should reveal safely
- [ ] Game 2: Click corner cell (0,0) → Should reveal safely
- [ ] Game 3: Click edge cell (0,4) → Should reveal safely
- [ ] Game 4: Click edge cell (4,0) → Should reveal safely
- [ ] Game 5: Click corner cell (8,8) → Should reveal safely
- [ ] Games 6-20: Click random positions → All should be safe

**Expected Behavior:**
- [ ] No game lost on first click across all 20 games
- [ ] Flood fill triggers if first click is on blank (0 adjacent mines)
- [ ] Numbered cells display correctly (1-8, matching Windows Minesweeper colors)
- [ ] Timer starts at 1 second after first click

**Result:** ✅ PASS / ❌ FAIL

### 2.2 Right-Click Flagging

**Procedure:**
1. Start new Beginner game
2. Right-click on unrevealed cell
3. Observe flag placement and counter behavior

**Expected Behavior:**
- [ ] Flag icon appears on cell
- [ ] Mine counter decrements: 010 → 009
- [ ] Right-click same cell again removes flag
- [ ] Mine counter increments: 009 → 010
- [ ] Cannot flag revealed cells
- [ ] Flag icon is visible and clear

**Counter Range Test:**
- [ ] Place 10 flags: Counter shows 000
- [ ] Place 11th flag: Counter shows -001 (red text on black background)
- [ ] Remove flags: Counter returns to 010

**Result:** ✅ PASS / ❌ FAIL

### 2.3 Cell Revealing

**Procedure:**
1. Start new Beginner game
2. Left-click various unrevealed cells
3. Observe reveal behavior

**Expected Behavior:**
- [ ] Clicking blank cell (0 adjacent) triggers flood fill
- [ ] Flood fill reveals all connected blank cells
- [ ] Flood fill stops at numbered cells (reveals them but doesn't continue)
- [ ] Clicking numbered cell reveals only that cell
- [ ] Revealed cells cannot be clicked again
- [ ] Revealed cells show correct numbers (1-8)
- [ ] Number colors match Windows Minesweeper:
  - [ ] 1: Blue
  - [ ] 2: Green
  - [ ] 3: Red
  - [ ] 4: Dark blue
  - [ ] 5: Brown
  - [ ] 6: Cyan
  - [ ] 7: Black
  - [ ] 8: Gray

**Result:** ✅ PASS / ❌ FAIL

### 2.4 Chording Mechanic

**Procedure:**
1. Start new Beginner game
2. Reveal a numbered cell (e.g., cell showing "1")
3. Flag the correct number of adjacent mines
4. Left-click the revealed numbered cell
5. Observe chording behavior

**Expected Behavior:**
- [ ] When flag count matches cell number, all unflagged neighbors reveal
- [ ] Chording triggers flood fill on blank neighbors
- [ ] Chording skips flagged cells
- [ ] Chording does nothing if flag count doesn't match (no penalty)
- [ ] Chording only works on revealed numbered cells (not blank or unrevealed)

**Test Scenario:**
- [ ] Reveal cell with "2"
- [ ] Flag exactly 2 adjacent mines
- [ ] Click the "2" cell → All unflagged neighbors reveal
- [ ] Any blank neighbors trigger flood fill

**Result:** ✅ PASS / ❌ FAIL

### 2.5 Timer Behavior

**Procedure:**
1. Start new Beginner game
2. Observe timer before and after first click
3. Watch timer count up

**Expected Behavior:**
- [ ] Timer shows 000 before first click
- [ ] Timer starts at 001 after first click
- [ ] Timer increments by 1 every second
- [ ] Timer clamps at 999 (doesn't overflow)
- [ ] Timer stops on win
- [ ] Timer stops on loss

**Timer Stop Test:**
- [ ] Win game → Timer stops at final value
- [ ] Reset game → Timer resets to 000
- [ ] Start new game → Timer stays at 000 until first click

**Result:** ✅ PASS / ❌ FAIL

---

## Verification 3: Win State

### Procedure to Force Win
**Note:** This requires luck or carefully revealing cells. May take multiple attempts.

1. Start new Beginner game
2. Reveal cells strategically
3. Flag all mines
4. Reveal all non-mine cells
5. Observe win state

### Expected Behavior
- [ ] All non-mine cells are revealed
- [ ] All mines may or may not be flagged (doesn't matter)
- [ ] Reset button face changes to cool 😎
- [ ] Timer stops counting
- [ ] No further input allowed (clicks do nothing)
- [ ] All cells remain visible

### Alternative Win Test (Code Modification)
If unable to win through gameplay, verify through code:
- [ ] Create test script that reveals all safe cells
- [ ] Verify game transitions to WON state
- [ ] Verify UI shows cool face

**Result:** ✅ PASS / ❌ FAIL

---

## Verification 4: Loss State

### Procedure to Force Loss
1. Start new Beginner game
2. Keep clicking cells until hitting a mine
3. Observe loss state

### Expected Behavior
- [ ] Clicked mine is highlighted or shown
- [ ] ALL mine positions are revealed on the board
- [ ] Reset button face changes to dead 😵
- [ ] Timer stops counting
- [ ] No further input allowed (clicks do nothing)
- [ ] All mine locations visible

### Visual Verification
- [ ] Mine that was clicked is clearly indicated
- [ ] All other mines also revealed (for player feedback)
- [ ] Incorrect flags remain visible
- [ ] Correct flags remain visible

**Result:** ✅ PASS / ❌ FAIL

---

## Verification 5: Reset Button

### Reset During Playing State
1. Start new game
2. Make a few moves
3. Click reset button (happy face)

**Expected Behavior:**
- [ ] New board generated with fresh mine positions
- [ ] Mine counter resets to 010
- [ ] Timer resets to 000
- [ ] Face remains happy 🙂
- [ ] Grid shows all unrevealed cells
- [ ] First click safety applies to new game

**Result:** ✅ PASS / ❌ FAIL

### Reset After Win
1. Win a game (or simulate win state)
2. Click reset button (cool face)

**Expected Behavior:**
- [ ] New game starts immediately
- [ ] Face changes from cool 😎 to happy 🙂
- [ ] Timer resets to 000
- [ ] Mine counter resets to 010
- [ ] Grid is ready for new game

**Result:** ✅ PASS / ❌ FAIL

### Reset After Loss
1. Lose a game (click a mine)
2. Click reset button (dead face)

**Expected Behavior:**
- [ ] New game starts immediately
- [ ] Face changes from dead 😵 to happy 🙂
- [ ] Timer resets to 000
- [ ] Mine counter resets to 010
- [ ] Grid is ready for new game

**Result:** ✅ PASS / ❌ FAIL

---

## Verification 6: Face Icon States

### Happy Face 🙂 (Playing State)
- [ ] Visible when game is in PLAYING state
- [ ] Visible after reset
- [ ] Visible after first click (returns to happy after momentary shocked)

### Shocked Face 😮 (Clicking State)
- [ ] Momentarily appears when clicking cells
- [ ] Returns to happy after click completes
- [ ] Provides visual feedback during click

### Dead Face 😵 (Loss State)
- [ ] Appears when mine is clicked
- [ ] Persists until reset
- [ ] Timer stopped
- [ ] All mines revealed

### Cool Face 😎 (Win State)
- [ ] Appears when all non-mine cells revealed
- [ ] Persists until reset
- [ ] Timer stopped
- [ ] Game won

**Result:** ✅ PASS / ❌ FAIL

---

## Verification 7: Intermediate Difficulty

### Procedure
1. Click "Game" → "Intermediate"
2. Observe board changes

### Expected Behavior
- [ ] Grid size: 16 rows × 16 columns (256 cells)
- [ ] Mine counter shows 040 (40 mines)
- [ ] Timer shows 000
- [ ] Reset button shows happy face 🙂
- [ ] All cells unrevealed

### Gameplay Test
- [ ] First click is safe (test 5 positions)
- [ ] Flood fill works on larger board
- [ ] Flagging decrements counter correctly
- [ ] Chording works
- [ ] Win/loss states work same as Beginner

**Result:** ✅ PASS / ❌ FAIL

---

## Verification 8: Expert Difficulty

### Procedure
1. Click "Game" → "Expert"
2. Observe board changes

### Expected Behavior
- [ ] Grid size: 16 rows × 30 columns (480 cells)
- [ ] Mine counter shows 099 (99 mines)
- [ ] Timer shows 000
- [ ] Reset button shows happy face 🙂
- [ ] All cells unrevealed
- [ ] Window may be wider to accommodate 30 columns

### Gameplay Test
- [ ] First click is safe (test 10 positions across wide board)
- [ ] Flood fill performs well on large board (should be instant)
- [ ] Flagging works correctly
- [ ] Chording works
- [ ] Win/loss states work same as other difficulties

**Performance Test:**
- [ ] Flood fill on large blank region completes < 100ms
- [ ] No lag or delay when revealing cells

**Result:** ✅ PASS / ❌ FAIL

---

## Verification 9: Difficulty Switching

### Beginner → Intermediate
1. Start game on Beginner
2. Make a few moves
3. Click "Game" → "Intermediate"

**Expected Behavior:**
- [ ] Game resets automatically
- [ ] Grid resizes to 16×16
- [ ] Mine counter updates to 040
- [ ] Timer resets to 000
- [ ] Face returns to happy 🙂
- [ ] New mine positions generated

### Intermediate → Expert
1. Click "Game" → "Expert"

**Expected Behavior:**
- [ ] Game resets automatically
- [ ] Grid resizes to 16×30
- [ ] Mine counter updates to 099
- [ ] Timer resets to 000
- [ ] New mine positions generated

### Expert → Beginner
1. Click "Game" → "Beginner"

**Expected Behavior:**
- [ ] Game resets automatically
- [ ] Grid resizes to 9×9
- [ ] Mine counter updates to 010
- [ ] Timer resets to 000
- [ ] New mine positions generated

**Result:** ✅ PASS / ❌ FAIL

---

## Verification 10: Exit Functionality

### Exit from Menu
1. Click "Game" → "Exit"
2. Observe application behavior

**Expected Behavior:**
- [ ] Application window closes
- [ ] No error messages
- [ ] Clean shutdown (no hanging processes)
- [ ] No console errors

### Close Window Button
1. Click window close button (X)
2. Observe application behavior

**Expected Behavior:**
- [ ] Application window closes
- [ ] No error messages
- [ ] Clean shutdown

**Result:** ✅ PASS / ❌ FAIL

---

## Verification 11: Edge Cases

### Rapid Clicking
1. Rapidly click multiple cells
2. Observe behavior

**Expected Behavior:**
- [ ] No crashes or errors
- [ ] All clicks processed correctly
- [ ] Face shows shocked momentarily for each click
- [ ] Input blocked after game over

### Flag All Mines
1. Start new game
2. Flag exactly the total number of mines (10 for Beginner)
3. Observe counter

**Expected Behavior:**
- [ ] Mine counter shows 000
- [ ] Game does not auto-win (must still reveal cells)
- [ ] Counter goes negative if too many flags placed

### Click Revealed Cell (No Chording)
1. Reveal a numbered cell
2. Don't place any flags
3. Click the revealed cell

**Expected Behavior:**
- [ ] Nothing happens (chording requires matching flags)
- [ ] No error
- [ ] Cell remains revealed
- [ ] No cells revealed

### Right-Click Revealed Cell
1. Reveal any cell
2. Try to right-click it

**Expected Behavior:**
- [ ] Flag cannot be placed on revealed cell
- [ ] No change to cell state
- [ ] No change to counter

**Result:** ✅ PASS / ❌ FAIL

---

## Verification 12: Multiple Games in Session

### Procedure
1. Play and win/lose 5 consecutive games
2. Try all three difficulties

**Expected Behavior:**
- [ ] Each game starts fresh
- [ ] No state carryover between games
- [ ] Timer resets each game
- [ ] Mine counter resets each game
- [ ] Face icon resets each game
- [ ] First-click safety applies every game
- [ ] No memory leaks or performance degradation

**Games to Play:**
- [ ] Game 1: Beginner - Win or Lose
- [ ] Game 2: Beginner - Win or Lose
- [ ] Game 3: Intermediate - Win or Lose
- [ ] Game 4: Intermediate - Win or Lose
- [ ] Game 5: Expert - Win or Lose

**Result:** ✅ PASS / ❌ FAIL

---

## Summary Checklist

### Critical Features (Must Pass)
- [ ] Application launches without errors
- [ ] All three difficulty levels work correctly
- [ ] First-click safety works (verified across 20+ games per difficulty)
- [ ] Timer starts on first click and stops on win/loss
- [ ] Mine counter increments/decrements with flagging
- [ ] Reset button works and resets all state
- [ ] Win state detected and displays cool face
- [ ] Loss state detected and displays dead face
- [ ] All mines revealed on loss
- [ ] Input blocked after game over

### Important Features (Should Pass)
- [ ] Flood fill reveals connected blank regions
- [ ] Chording mechanic works correctly
- [ ] Face icons change based on game state
- [ ] Difficulty switching resets game cleanly
- [ ] Exit functionality works
- [ ] No console errors during gameplay

### Nice-to-Have Features
- [ ] Window size accommodates Expert board
- [ ] Rapid clicking handled gracefully
- [ ] Counter shows negative values when over-flagged
- [ ] Multiple games can be played in one session

---

## Test Results Summary

**Automated Tests (tests/test_e2e_gameplay.py):**
- [ ] All tests pass (run: `pytest tests/test_e2e_gameplay.py -v`)

**Manual GUI Tests (This Checklist):**
- [ ] Verification 1: Application Launch - ✅ PASS / ❌ FAIL
- [ ] Verification 2: Beginner Difficulty - ✅ PASS / ❌ FAIL
- [ ] Verification 3: Win State - ✅ PASS / ❌ FAIL
- [ ] Verification 4: Loss State - ✅ PASS / ❌ FAIL
- [ ] Verification 5: Reset Button - ✅ PASS / ❌ FAIL
- [ ] Verification 6: Face Icon States - ✅ PASS / ❌ FAIL
- [ ] Verification 7: Intermediate Difficulty - ✅ PASS / ❌ FAIL
- [ ] Verification 8: Expert Difficulty - ✅ PASS / ❌ FAIL
- [ ] Verification 9: Difficulty Switching - ✅ PASS / ❌ FAIL
- [ ] Verification 10: Exit Functionality - ✅ PASS / ❌ FAIL
- [ ] Verification 11: Edge Cases - ✅ PASS / ❌ FAIL
- [ ] Verification 12: Multiple Games - ✅ PASS / ❌ FAIL

**Overall Result:** ✅ ALL PASS / ⚠️ PARTIAL PASS / ❌ FAIL

---

## Notes and Issues

Document any issues found during testing:

1. **Issue:** _______________________
   - **Severity:** Critical / High / Medium / Low
   - **Steps to Reproduce:**
   - **Expected Behavior:**
   - **Actual Behavior:**

2. **Issue:** _______________________
   - **Severity:** Critical / High / Medium / Low
   - **Steps to Reproduce:**
   - **Expected Behavior:**
   - **Actual Behavior:**

---

## Test Sign-Off

**Tester Name:** _______________________

**Test Date:** _______________________

**Overall Assessment:**
- [ ] Ready for production
- [ ] Ready with minor issues
- [ ] Needs fixes before release

**Comments:**
_______________________________________________________________________________
_______________________________________________________________________________
_______________________________________________________________________________

---

## Appendix: Quick Reference

### Difficulty Configurations
| Difficulty | Rows | Cols | Mines |
|------------|------|------|-------|
| Beginner   | 9    | 9    | 10    |
| Intermediate | 16 | 16   | 40    |
| Expert     | 16   | 30   | 99    |

### Face Icons
- 🙂 Happy - Playing state
- 😮 Shocked - Clicking feedback
- 😵 Dead - Lost state
- 😎 Cool - Won state

### Number Colors
1: Blue, 2: Green, 3: Red, 4: Dark Blue, 5: Brown, 6: Cyan, 7: Black, 8: Gray

### Win Condition
All non-mine cells revealed (flags don't matter)

### Loss Condition
Any mine is revealed

### First-Click Safety
First click and all 8 neighbors are guaranteed mine-free
