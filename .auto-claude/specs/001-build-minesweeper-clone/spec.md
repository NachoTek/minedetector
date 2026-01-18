# Specification: Build Minesweeper Clone

## Overview

Build a complete Minesweeper clone that replicates the original Windows Minesweeper feature set exactly. This is a greenfield desktop application project requiring implementation of core game mechanics (mine placement, flood fill revealing, chording), three standard difficulty levels, timer/counter UI, and win/loss state detection.

## Workflow Type

**Type**: feature

**Rationale**: This is a new feature development project building a complete desktop application from scratch. No existing codebase exists to refactor or investigate. The task requires creating new game logic, UI components, and state management systems.

## Task Scope

### Services Involved
- **Minesweeper Application** (primary) - Standalone desktop game application

### This Task Will:
- [ ] Create complete Minesweeper game with Windows-accurate feature set
- [ ] Implement three standard difficulty levels (Beginner, Intermediate, Expert)
- [ ] Build core game algorithms (mine placement, flood fill, chording, adjacent counting)
- [ ] Create game UI with grid, timer, mine counter, and reset button
- [ ] Implement first-click-safe mine placement
- [ ] Add game state management (playing, won, lost)
- [ ] Handle all mouse interactions (left-click reveal, right-click flag, chording)

### Out of Scope:
- Custom difficulty editor (Windows had this but not core requirement)
- High scores persistence (nice-to-have but not required for MVP)
- Question mark flagging toggle (advanced Windows feature)
- Multiplayer or online features
- Mobile/platform-specific adaptations

## Service Context

### Minesweeper Application

**Tech Stack:**
- Language: Python (recommended for rapid development)
- Framework Options:
  - **Tkinter** (Recommended): Built into Python, native button widgets, authentic Windows look
  - **Pygame**: External dependency, custom rendering, modern cross-platform polish
- Key directories: `/src` (game logic), `/ui` (interface), `/tests` (unit tests)

**Entry Point:** `main.py` or `app.py`

**How to Run:**
```bash
# If using Tkinter (no pip install needed)
python main.py

# If using Pygame
pip install pygame
python main.py
```

**Port:** N/A (Desktop application, no web server)

## Files to Modify

N/A - This is a greenfield project with no existing files to modify.

## Files to Reference

No existing reference files available. Use these patterns from research phase:

| Pattern | Source | Implementation Guidance |
|---------|--------|------------------------|
| Grid-based game architecture | Research phase recommendations | 2D array with cell objects containing state |
| Flood fill algorithm | Research phase | DFS/BFS to reveal connected blank cells |
| First-click safety | Research phase | Generate mines after first click, ensure first-click cell is safe |
| Chording mechanic | Research phase | When flags_placed === cell_number, reveal all neighbors |

## Patterns to Follow

### Cell Data Structure

From research phase:

```python
class Cell:
    def __init__(self):
        self.mine = False  # Is this cell a mine?
        self.revealed = False  # Has the user revealed this cell?
        self.flagged = False  # Has the user placed a flag?
        self.adjacent_mines = 0  # Count of mines in 8 neighbors (0-8)
```

**Key Points:**
- Each cell is an independent object with 4 boolean/int properties
- 2D array (list of lists) stores Cell objects
- Coordinate system: (row, col) with (0,0) at top-left corner

### Game States

From research phase:

```python
class GameState(Enum):
    PLAYING = "playing"
    WON = "won"
    LOST = "lost"
```

**Key Points:**
- Game starts in PLAYING state
- Timer starts on first cell reveal
- State transitions to WON when all non-mine cells revealed
- State transitions to LOST when mine is clicked
- Timer stops on state change to WON or LOST

### Difficulty Configurations

From research phase (Windows Minesweeper standard):

```python
DIFFICULTIES = {
    "Beginner": {"rows": 9, "cols": 9, "mines": 10},
    "Intermediate": {"rows": 16, "cols": 16, "mines": 40},
    "Expert": {"rows": 16, "cols": 30, "mines": 99}
}
```

**Key Points:**
- Beginner: 9x9 grid with 10 mines (11.1% mine density)
- Intermediate: 16x16 grid with 40 mines (15.6% mine density)
- Expert: 16x30 grid with 99 mines (20.6% mine density)
- Mine counter shows: `total_mines - flags_placed`

### Flood Fill Algorithm

From research phase:

```python
def flood_fill(board, start_row, start_col):
    # Use stack-based iteration to avoid stack overflow on large boards
    stack = [(start_row, start_col)]

    while stack:
        row, col = stack.pop()

        # Skip if out of bounds or already revealed
        if not is_valid(board, row, col) or board[row][col].revealed:
            continue

        # Reveal current cell
        board[row][col].revealed = True

        # If cell has adjacent mines, stop (only reveal blanks)
        if board[row][col].adjacent_mines > 0:
            continue

        # Add all 8 neighbors to stack
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr != 0 or dc != 0:
                    stack.append((row + dr, col + dc))
```

**Key Points:**
- Use stack-based iteration to avoid stack overflow on large boards (Expert: 480 cells)
- Only reveal cells with 0 adjacent mines (blank cells) in the flood fill
- Stop at numbered cells (1-8) - reveal them but don't continue past them
- Must check bounds before accessing board array

### First-Click Safety

From research phase:

```python
def place_mines(board, total_mines, first_click_row, first_click_col):
    mines_placed = 0
    while mines_placed < total_mines:
        row = random.randint(0, rows - 1)
        col = random.randint(0, cols - 1)

        # Skip if mine already here, or is first-click cell
        if board[row][col].mine:
            continue
        if row == first_click_row and col == first_click_col:
            continue

        board[row][col].mine = True
        mines_placed += 1

    # Calculate adjacent mine counts for all cells
    calculate_adjacent_counts(board)
```

**Key Points:**
- Generate mines AFTER first click (not during board initialization)
- Ensure first-click cell and its neighbors are safe
- Recalculate adjacent counts after mine placement

### Chording Mechanic

From research phase:

```python
def handle_chord(board, row, col):
    cell = board[row][col]

    # Only allow chording on revealed numbered cells
    if not cell.revealed or cell.adjacent_mines == 0:
        return

    # Count flags in 8 neighbors
    flag_count = count_flags(board, row, col)

    # If flags match number, reveal all neighbors
    if flag_count == cell.adjacent_mines:
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                nr, nc = row + dr, col + dc
                if is_valid(board, nr, nc) and not board[nr][nc].flagged:
                    reveal_cell(board, nr, nc)
```

**Key Points:**
- Chording: Clicking a revealed number reveals all neighbors if correct flag count
- Activated when: `flags_placed === cell_number` in neighboring cells
- Only reveal non-flagged neighbors
- Can trigger game loss if neighbor flags are incorrect

## Requirements

### Functional Requirements

1. **Grid-Based Game Board**
   - Description: Display 2D grid of cells matching Windows Minesweeper layout
   - Acceptance: Grid renders correctly for all three difficulty levels with proper spacing and alignment

2. **Mine Placement Algorithm**
   - Description: Randomly place mines on board with first-click safety guarantee
   - Acceptance: First click is never a mine, mines distributed randomly across remaining cells

3. **Adjacent Mine Counting**
   - Description: Calculate and display numbers (1-8) indicating adjacent mine count
   - Acceptance: Each non-mine cell shows correct count of mines in its 8 neighbors

4. **Flood Fill Reveal**
   - Description: When clicking a blank cell (0 adjacent mines), automatically reveal all connected blank cells and bordering numbered cells
   - Acceptance: Clicking blank cells reveals entire contiguous blank region with numbered borders

5. **Left-Click Reveal**
   - Description: Left-clicking unrevealed cells reveals them; clicking mine ends game
   - Acceptance: Reveals cells, updates UI, triggers loss on mine click

6. **Right-Click Flag**
   - Description: Right-clicking cells places/removes flag, updates mine counter
   - Acceptance: Flags toggle on/off, mine counter decrements/increments accordingly

7. **Chording Mechanic**
   - Description: Clicking revealed numbered cells with correct flag count reveals remaining neighbors
   - Acceptance: When neighbor flags === cell number, all unflagged neighbors are revealed

8. **Mine Counter**
   - Description: Display remaining mines: `total_mines - flags_placed`
   - Acceptance: Counter updates in real-time as flags are placed/removed

9. **Game Timer**
   - Description: Count up from 0, starting on first click, stopping on game end
   - Acceptance: Timer starts on first reveal, stops on win/loss, displays in seconds

10. **Reset Button**
    - Description: Button to restart game with same difficulty, changes expression based on game state
    - Acceptance: Clicking resets board, face icon shows happy (playing), shocked (clicking), dead (lost), cool (won)

11. **Three Difficulty Levels**
    - Description: Beginner (9x9, 10 mines), Intermediate (16x16, 40 mines), Expert (30x16, 99 mines)
    - Acceptance: All three difficulties selectable and playable with correct grid sizes and mine counts

12. **Win Detection**
    - Description: Detect when all non-mine cells are revealed
    - Acceptance: Game state transitions to WON, all mines revealed, timer stops, face icon changes

13. **Loss Detection**
    - Description: Detect when mine is clicked
    - Acceptance: Game state transitions to LOST, clicked mine highlighted, all mines revealed, timer stops

### Edge Cases

1. **First-Click Mine** - Must ensure first click is never a mine by generating mines after first click
2. **Flood Fill Stack Overflow** - Use iterative approach (stack/queue) instead of recursion for large boards (Expert: 480 cells)
3. **Chording with Wrong Flags** - If player flags wrong cell and chords, should trigger game loss on mine reveal
4. **Flagging Revealed Cells** - Should not allow flagging already revealed cells
5. **Chording on Blank Cells** - Chording only works on numbered cells, not blank cells
6. **Right-Click on macOS** - Tkinter right-click may require special handling on macOS (Button-2 vs Button-3)
7. **Timer Overflow** - Timer should handle games longer than 999 seconds (display max or continue counting)
8. **All Cells Flagged Incorrectly** - If player flags all cells incorrectly but no mines clicked, game continues until actual reveal

## Implementation Notes

### DO
- Follow flood fill pattern using stack/queue iteration to avoid recursion depth issues on Expert boards
- Generate mines AFTER first click to ensure safety
- Use 2D array of Cell objects for clean state management
- Implement win detection by counting revealed cells vs total non-mine cells: `revealed_count == (rows * cols) - mine_count`
- Calculate adjacent mine counts immediately after mine placement
- Reset timer to 0 and mine counter to total_mines on new game
- Use different colors for numbers 1-8 (Windows used: blue, green, red, dark blue, brown, cyan, black, gray)
- Disable all input after game ends (won or lost) until reset

### DON'T
- Don't place mines before first click - violates first-click safety requirement
- Don't use naive recursion for flood fill on Expert boards - may hit recursion limit
- Don't allow revealing flagged cells during chording
- Don't forget to stop timer on game end (both won and lost states)
- Don't allow flagging already revealed cells
- Don't allow input after game has ended (won/lost) until reset
- Don't create new UI framework from scratch - use Tkinter (built-in) or Pygame (proven game library)

### Technical Considerations

**Tkinter (Recommended for authentic Windows look):**
- `tk.Button` widgets for cells (native button look and feel)
- Grid layout manager (`grid()`) for perfect alignment
- Event binding: `<Button-1>` for left-click, `<Button-3>` (or `<Button-2>` on macOS) for right-click
- Timer: `root.after(1000, update_timer)` for 1-second updates
- macOS right-click workaround: Check platform and bind both `<Button-2>` and `<Button-3>`

**Pygame (Alternative for modern polish):**
- Custom cell rendering with `pygame.draw.rect()`
- Mouse event handling: `pygame.MOUSEBUTTONDOWN` with `event.button` (1=left, 3=right)
- Game loop: `while running:` with `clock.tick(60)` for 60 FPS
- Timer: Track `start_time` and calculate `current_time - start_time`
- More flexibility for animations, sound effects, custom graphics

## Development Environment

### Start Services

This is a desktop application - no background services needed.

```bash
# Clone/download project to: C:\Projects\minedetector
cd minedetector

# If using Tkinter (no installation needed for Python)
python main.py

# If using Pygame
pip install pygame
python main.py
```

### Service URLs
N/A - Desktop application opens in native window

### Required Environment Variables
None required for basic implementation. Optional:
- `MINESWEEPER_DIFFICULTY`: Override default difficulty (Beginner|Intermediate|Expert)
- `MINESWEEPER_THEME`: Color theme (windows_dark, windows_light, custom)

## Success Criteria

The task is complete when:

1. [ ] Application runs without errors and displays game board
2. [ ] All three difficulty levels selectable with correct grid sizes and mine counts
3. [ ] Left-click reveals cells, right-click places/removes flags
4. [ ] First click is never a mine (tested across 20+ random games)
5. [ ] Flood fill correctly reveals connected blank regions
6. [ ] Numbers (1-8) correctly display adjacent mine counts
7. [ ] Chording mechanic works when flags === cell number
8. [ ] Mine counter updates in real-time as flags placed
9. [ ] Timer starts on first click and stops on game end
10. [ ] Win detection triggers when all non-mine cells revealed
11. [ ] Loss detection triggers when mine clicked
12. [ ] Reset button restarts game cleanly
13. [ ] No console errors during normal gameplay
14. [ ] Existing tests pass (if test suite created)

## QA Acceptance Criteria

**CRITICAL**: These criteria must be verified by the QA Agent before sign-off.

### Unit Tests
| Test | File | What to Verify |
|------|------|----------------|
| Cell initialization | `test/test_cell.py` | Cell object created with correct default state (mine=False, revealed=False, flagged=False, adjacent_mines=0) |
| Adjacent mine counting | `test/test_adjacent.py` | Correctly counts mines in all 8 neighbor positions, handles edge/corner cells |
| Flood fill algorithm | `test/test_floodfill.py` | Reveals connected blank regions, stops at numbered cells, handles bounds checking |
| First-click safety | `test/test_first_click.py` | First-click cell and neighbors never contain mines across 100+ random generations |
| Chording mechanic | `test/test_chording.py` | Reveals neighbors when flags === number, doesn't reveal when flags != number |
| Win detection | `test/test_win.py` | Game state = WON when all non-mine cells revealed |
| Loss detection | `test/test_loss.py` | Game state = LOST when mine clicked |

### Integration Tests
| Test | Services | What to Verify |
|------|----------|----------------|
| Full game flow | UI ↔ Game Logic | Complete game from start to win/loss with correct state transitions |
| Timer integration | Timer ↔ Game State | Timer starts on first click, stops on game end, displays correct elapsed time |
| Mine counter integration | Counter ↔ Flag Placement | Counter decrements on flag place, increments on flag remove |
| Difficulty switching | UI ↔ Board Generator | Switching difficulties correctly changes grid size and mine count |

### End-to-End Tests
| Flow | Steps | Expected Outcome |
|------|-------|------------------|
| Beginner win | 1. Select Beginner 2. Reveal all non-mine cells 3. Verify win state | Game detects win, stops timer, shows cool face, all mines revealed |
| Expert loss | 1. Select Expert 2. Click mine 3. Verify loss state | Game detects loss, stops timer, shows dead face, clicked mine highlighted |
| First-click safety | 1. Start 20 games on each difficulty 2. Click random first cell 3. Verify safe | Zero first-click mines across all 60 games |
| Complete chording flow | 1. Reveal numbered cell 2. Place correct flag count 3. Chord cell | All unflagged neighbors revealed, no game loss |
| Incorrect chording | 1. Reveal numbered cell 2. Place wrong flags 3. Chord cell | Either nothing happens (if insufficient flags) or game loss (if wrong flags) |

### Browser Verification (if applicable)
N/A - Desktop application, verify in native window

### Desktop Application Verification
| Component | Action | Checks |
|-----------|--------|--------|
| Main menu | Launch application | Window opens, difficulty selection visible |
| Beginner game | Select Beginner | 9x9 grid displays, mine counter shows 10 |
| Intermediate game | Select Intermediate | 16x16 grid displays, mine counter shows 40 |
| Expert game | Select Expert | 30x16 grid displays, mine counter shows 99 |
| Cell reveal | Left-click unrevealed cell | Cell reveals content, blank triggers flood fill |
| Flag placement | Right-click unrevealed cell | Flag icon appears, mine counter decrements |
| Flag removal | Right-click flagged cell | Flag icon disappears, mine counter increments |
| Chording | Left-click revealed number with correct flags | All unflagged neighbors reveal |
| Reset functionality | Click reset button | Board regenerates with new mine positions, timer resets |
| Timer behavior | Start game, wait 10+ seconds | Timer counts up, starts on first click |
| Win state | Reveal all non-mine cells | All mines revealed, timer stops, face shows cool |
| Loss state | Click mine | Mine highlighted, all mines revealed, timer stops, face shows dead |

### Database Verification (if applicable)
N/A - No database required for basic implementation

### Performance Verification
| Test | Metric | Expected |
|------|--------|----------|
| Flood fill on Expert board | Time to reveal large blank region | < 100ms for any flood fill operation |
| Mine placement | Time to generate mines | < 50ms for any difficulty |
| UI responsiveness | Time from click to visual update | < 16ms (60 FPS target for Pygame) |

### QA Sign-off Requirements
- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] All E2E tests pass
- [ ] Manual desktop verification complete for all three difficulties
- [ ] First-click safety verified across 20+ games per difficulty
- [ ] Flood fill performance verified on Expert board
- [ ] Win/loss states trigger correctly
- [ ] Timer and mine counter work accurately
- [ ] No regressions in existing functionality (greenfield - N/A)
- [ ] Code follows established patterns (documented in spec)
- [ ] No crashes or unhandled exceptions during normal gameplay
- [ ] Application closes cleanly without hanging
