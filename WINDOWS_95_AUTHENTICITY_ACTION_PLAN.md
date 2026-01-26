# Windows 95/98 Minesweeper Authenticity Action Plan

## Executive Summary

This document outlines the visual improvements needed to transform Minedetector from a functional game into an authentic Windows 95/98 Minesweeper recreation. The current implementation uses modern UI elements (emojis, flat colors, Unicode symbols) that deviate from the classic Windows aesthetic.

**Target:** Windows 95/98 Minesweeper (winmine.exe)
**Current Status:** Functional gameplay with modern UI
**Goal:** Pixel-perfect visual authenticity while maintaining clean architecture

---

## Visual Reference: Windows 95/98 Minesweeper

The original Windows 95/98 Minesweeper had these distinctive characteristics:

### Color Palette
- **Background**: Standard Windows gray (#C0C0C0)
- **3D Bevels**: White highlight (#FFFFFF) and dark shadow (#808080)
- **LCD Displays**: Black text on red background (#FF0000)
- **Number Colors**: Blue (1), Green (2), Red (3), Dark Blue (4), Maroon (5), Teal (6), Black (7), Gray (8)

### UI Elements
- **Sunken 3D Border**: Main game area with proper bevel effects
- **Raised Buttons**: Unrevealed cells with highlight/shadow
- **Sunken Cells**: Revealed cells with inset appearance
- **Bitmap Icons**: Canvas-drawn face, mine, and flag icons (not emojis)
- **LCD Digits**: 7-segment style numbers for timer and counter

### Typography
- **Font**: MS Sans Serif or Arial (bold for numbers)
- **Sizes**: 8pt for UI, 10-12pt for game elements

---

## Prioritized Action Items

### HIGH PRIORITY

#### 1. Replace Emoji Face with Canvas-Drawn Bitmap
**File**: `C:\Projects\minedetector\src\ui\reset_button.py`
**Effort**: Medium
**Visual Impact**: HIGH - Face button is the centerpiece of the UI

**Description**: Replace Unicode emoji faces with canvas-drawn bitmap icons matching Windows 95 style. The current implementation uses `Segoe UI Emoji` font with emoji characters, which look modern and break immersion.

**Before**:
```python
FACE_HAPPY = "🙂"
FACE_SHOCKED = "😮"
FACE_DEAD = "😵"
FACE_COOL = "😎"
```

**After**: Create a new module `C:\Projects\minedetector\src\ui\win95_icons.py` with canvas drawing functions:

```python
"""
Windows 95 Icons Module

Contains canvas drawing functions for authentic Windows 95 Minesweeper icons:
- Face buttons (happy, shocked, dead, cool)
- Mine icon
- Flag icon
- Question mark icon (optional feature)
"""

from tkinter import Canvas
from typing import Optional


class Win95Icons:
    """Collection of Windows 95 style icon drawing methods."""

    @staticmethod
    def draw_happy_face(canvas: Canvas, x: int, y: int, size: int = 26) -> None:
        """
        Draw a Windows 95 style happy face.

        The happy face has:
        - Yellow/ochre circular background
        - Two black dot eyes
        - Curved black smile
        - Subtle 3D bevel effect

        Args:
            canvas: The canvas widget to draw on
            x: Top-left X coordinate
            y: Top-left Y coordinate
            size: Width/height of the icon (square)
        """
        center_x = x + size // 2
        center_y = y + size // 2
        radius = size // 2 - 2

        # Draw face circle (ochre/yellow background)
        canvas.create_oval(
            x + 2, y + 2,
            x + size - 2, y + size - 2,
            fill="#FFFF00", outline="#000000", width=1
        )

        # Draw eyes (black dots)
        eye_y = center_y - 3
        left_eye_x = center_x - 5
        right_eye_x = center_x + 5
        eye_radius = 2

        canvas.create_oval(
            left_eye_x - eye_radius, eye_y - eye_radius,
            left_eye_x + eye_radius, eye_y + eye_radius,
            fill="#000000", outline="#000000"
        )
        canvas.create_oval(
            right_eye_x - eye_radius, eye_y - eye_radius,
            right_eye_x + eye_radius, eye_y + eye_radius,
            fill="#000000", outline="#000000"
        )

        # Draw smile (arc)
        smile_y = center_y + 3
        canvas.create_arc(
            center_x - 7, smile_y - 5,
            center_x + 7, smile_y + 5,
            start=180, extent=180,
            style="arc", outline="#000000", width=2
        )

    @staticmethod
    def draw_shocked_face(canvas: Canvas, x: int, y: int, size: int = 26) -> None:
        """
        Draw a Windows 95 style shocked face (open mouth).

        The shocked face has:
        - Yellow/ochre circular background
        - Two black dot eyes (same as happy)
        - Open circular mouth (O shape)

        Args:
            canvas: The canvas widget to draw on
            x: Top-left X coordinate
            y: Top-left Y coordinate
            size: Width/height of the icon (square)
        """
        center_x = x + size // 2
        center_y = y + size // 2
        radius = size // 2 - 2

        # Draw face circle
        canvas.create_oval(
            x + 2, y + 2,
            x + size - 2, y + size - 2,
            fill="#FFFF00", outline="#000000", width=1
        )

        # Draw eyes
        eye_y = center_y - 4
        left_eye_x = center_x - 5
        right_eye_x = center_x + 5
        eye_radius = 2

        canvas.create_oval(
            left_eye_x - eye_radius, eye_y - eye_radius,
            left_eye_x + eye_radius, eye_y + eye_radius,
            fill="#000000", outline="#000000"
        )
        canvas.create_oval(
            right_eye_x - eye_radius, eye_y - eye_radius,
            right_eye_x + eye_radius, eye_y + eye_radius,
            fill="#000000", outline="#000000"
        )

        # Draw open mouth (O shape)
        mouth_y = center_y + 4
        mouth_radius = 3
        canvas.create_oval(
            center_x - mouth_radius, mouth_y - mouth_radius,
            center_x + mouth_radius, mouth_y + mouth_radius,
            fill="#000000", outline="#000000"
        )

    @staticmethod
    def draw_dead_face(canvas: Canvas, x: int, y: int, size: int = 26) -> None:
        """
        Draw a Windows 95 style dead face (X eyes).

        The dead face has:
        - Yellow/ochre circular background
        - Two X eyes (crossed out)
        - Straight or slightly sad mouth

        Args:
            canvas: The canvas widget to draw on
            x: Top-left X coordinate
            y: Top-left Y coordinate
            size: Width/height of the icon (square)
        """
        center_x = x + size // 2
        center_y = y + size // 2
        radius = size // 2 - 2

        # Draw face circle
        canvas.create_oval(
            x + 2, y + 2,
            x + size - 2, y + size - 2,
            fill="#FFFF00", outline="#000000", width=1
        )

        # Draw X eyes
        eye_y = center_y - 3
        left_eye_x = center_x - 5
        right_eye_x = center_x + 5
        eye_offset = 3

        # Left eye X
        canvas.create_line(
            left_eye_x - eye_offset, eye_y - eye_offset,
            left_eye_x + eye_offset, eye_y + eye_offset,
            fill="#000000", width=2
        )
        canvas.create_line(
            left_eye_x + eye_offset, eye_y - eye_offset,
            left_eye_x - eye_offset, eye_y + eye_offset,
            fill="#000000", width=2
        )

        # Right eye X
        canvas.create_line(
            right_eye_x - eye_offset, eye_y - eye_offset,
            right_eye_x + eye_offset, eye_y + eye_offset,
            fill="#000000", width=2
        )
        canvas.create_line(
            right_eye_x + eye_offset, eye_y - eye_offset,
            right_eye_x - eye_offset, eye_y + eye_offset,
            fill="#000000", width=2
        )

        # Draw straight mouth
        mouth_y = center_y + 5
        canvas.create_line(
            center_x - 5, mouth_y,
            center_x + 5, mouth_y,
            fill="#000000", width=2
        )

    @staticmethod
    def draw_cool_face(canvas: Canvas, x: int, y: int, size: int = 26) -> None:
        """
        Draw a Windows 95 style cool face (sunglasses).

        The cool face has:
        - Yellow/ochre circular background
        - Black sunglasses (rectangles)
        - Smile (same as happy face)

        Args:
            canvas: The canvas widget to draw on
            x: Top-left X coordinate
            y: Top-left Y coordinate
            size: Width/height of the icon (square)
        """
        center_x = x + size // 2
        center_y = y + size // 2
        radius = size // 2 - 2

        # Draw face circle
        canvas.create_oval(
            x + 2, y + 2,
            x + size - 2, y + size - 2,
            fill="#FFFF00", outline="#000000", width=1
        )

        # Draw sunglasses (two connected black rectangles)
        glasses_y = center_y - 4
        glasses_height = 6
        left_glass_x = center_x - 8
        right_glass_x = center_x + 2

        # Left lens
        canvas.create_rectangle(
            left_glass_x, glasses_y,
            left_glass_x + 6, glasses_y + glasses_height,
            fill="#000000", outline="#000000"
        )

        # Right lens
        canvas.create_rectangle(
            right_glass_x, glasses_y,
            right_glass_x + 6, glasses_y + glasses_height,
            fill="#000000", outline="#000000"
        )

        # Bridge (connecting line)
        canvas.create_line(
            left_glass_x + 6, glasses_y + 2,
            right_glass_x, glasses_y + 2,
            fill="#000000", width=2
        )

        # Draw smile
        smile_y = center_y + 4
        canvas.create_arc(
            center_x - 6, smile_y - 5,
            center_x + 6, smile_y + 5,
            start=180, extent=180,
            style="arc", outline="#000000", width=2
        )

    @staticmethod
    def draw_mine(canvas: Canvas, x: int, y: int, size: int = 26) -> None:
        """
        Draw a Windows 95 style mine icon.

        The mine has:
        - Black circular body
        - Spikes (lines radiating from center)
        - Highlight dot (for 3D effect)

        Args:
            canvas: The canvas widget to draw on
            x: Top-left X coordinate
            y: Top-left Y coordinate
            size: Width/height of the icon (square)
        """
        center_x = x + size // 2
        center_y = y + size // 2
        radius = 8

        # Draw mine spikes (8 directions)
        for angle in range(0, 360, 45):
            import math
            rad = math.radians(angle)
            end_x = center_x + int(radius * 1.5 * math.cos(rad))
            end_y = center_y + int(radius * 1.5 * math.sin(rad))
            canvas.create_line(
                center_x, center_y,
                end_x, end_y,
                fill="#000000", width=2
            )

        # Draw mine body (circle)
        canvas.create_oval(
            center_x - radius, center_y - radius,
            center_x + radius, center_y + radius,
            fill="#000000", outline="#000000"
        )

        # Draw highlight (white dot for 3D effect)
        canvas.create_oval(
            center_x - 3, center_y - 3,
            center_x, center_y,
            fill="#FFFFFF", outline="#FFFFFF"
        )

    @staticmethod
    def draw_flag(canvas: Canvas, x: int, y: int, size: int = 26) -> None:
        """
        Draw a Windows 95 style flag icon.

        The flag has:
        - Red triangular flag
        - Black pole
        - Base (small square)

        Args:
            canvas: The canvas widget to draw on
            x: Top-left X coordinate
            y: Top-left Y coordinate
            size: Width/height of the icon (square)
        """
        pole_x = x + 5
        pole_top = y + 4
        pole_bottom = y + size - 4

        # Draw pole
        canvas.create_line(
            pole_x, pole_top,
            pole_x, pole_bottom,
            fill="#000000", width=2
        )

        # Draw flag (red triangle)
        flag_width = 10
        flag_height = 8
        canvas.create_polygon(
            pole_x + 2, pole_top,
            pole_x + 2, pole_top + flag_height,
            pole_x + flag_width, pole_top + flag_height // 2,
            fill="#FF0000", outline="#000000", width=1
        )

        # Draw base
        canvas.create_rectangle(
            pole_x - 2, pole_bottom - 2,
            pole_x + 4, pole_bottom + 2,
            fill="#000000", outline="#000000"
        )


# Helper function to create a canvas with an icon
def create_icon_canvas(parent, icon_type: str, size: int = 26) -> Canvas:
    """
    Create a canvas widget with a specific Windows 95 icon drawn on it.

    Args:
        parent: The parent widget
        icon_type: Type of icon ('happy', 'shocked', 'dead', 'cool', 'mine', 'flag')
        size: Size of the canvas/icon

    Returns:
        Canvas widget with the icon drawn

    Raises:
        ValueError: If icon_type is not recognized
    """
    canvas = Canvas(parent, width=size, height=size, highlightthickness=0)

    if icon_type == "happy":
        Win95Icons.draw_happy_face(canvas, 0, 0, size)
    elif icon_type == "shocked":
        Win95Icons.draw_shocked_face(canvas, 0, 0, size)
    elif icon_type == "dead":
        Win95Icons.draw_dead_face(canvas, 0, 0, size)
    elif icon_type == "cool":
        Win95Icons.draw_cool_face(canvas, 0, 0, size)
    elif icon_type == "mine":
        Win95Icons.draw_mine(canvas, 0, 0, size)
    elif icon_type == "flag":
        Win95Icons.draw_flag(canvas, 0, 0, size)
    else:
        raise ValueError(f"Unknown icon type: {icon_type}")

    return canvas
```

**Modified Reset Button Implementation**:
Update `C:\Projects\minedetector\src\ui\reset_button.py`:

```python
"""
Reset Button Module (Windows 95 Authentic)

Creates and manages the reset button with reactive face icons for the Mine Detector game.
Changes expression based on game state and resets the game when clicked.
"""

import tkinter as tk
from typing import Optional, Callable
from src.ui.win95_icons import create_icon_canvas


class ResetButton:
    """
    Manages the reset button with reactive face icons for the Mine Detector game.

    The reset button displays different face icons based on the current game state:
    - Happy: Game is in progress, normal playing state
    - Shocked: Player is clicking a cell (momentary state during click)
    - Dead: Game was lost (mine clicked)
    - Cool: Game was won (all non-mine cells revealed)

    Clicking the button at any time resets the game to the initial state,
    regenerating the mine positions and resetting the timer and counter.

    Attributes:
        parent: The parent Tkinter widget (usually the main window).
        on_reset: Optional callback function invoked when button is clicked.
        current_state: The current face state being displayed.
        icon_canvas: Canvas widget displaying the current face icon.
    """

    # Face state names for validation
    VALID_STATES = {"happy", "shocked", "dead", "cool"}
    """Set of valid face state names."""

    def __init__(
        self,
        parent: tk.Widget,
        on_reset: Optional[Callable[[], None]] = None
    ):
        """
        Initialize the reset button with reactive face icons.

        Creates a button widget with the happy face icon (default playing state).
        The button is sized to display the Windows 95 style face icon clearly.

        Args:
            parent: The parent Tkinter widget to contain the button.
            on_reset: Optional callback function invoked when button is clicked.

        Raises:
            ValueError: If parent is None.
        """
        if parent is None:
            raise ValueError("Parent cannot be None")

        self.parent = parent
        """The parent Tkinter widget containing this button."""

        self.on_reset = on_reset
        """Optional callback function invoked when button is clicked."""

        # Track current face state
        self.current_state = "happy"
        """The current face state being displayed."""

        # Create frame to hold canvas (for proper 3D border)
        self.frame = tk.Frame(parent, relief="raised", bd=2)
        """The frame widget containing the icon canvas."""

        # Create canvas with happy face icon
        self.icon_canvas = create_icon_canvas(self.frame, "happy", size=26)
        """The canvas widget displaying the face icon."""

        # Pack canvas into frame
        self.icon_canvas.pack()

        # Bind click events to frame
        self.frame.bind("<Button-1>", self._handle_click)
        self.icon_canvas.bind("<Button-1>", self._handle_click)

    def _handle_click(self, event) -> None:
        """
        Handle button click event.

        This method is called when the reset button is clicked. It temporarily
        changes the face to shocked, then invokes the on_reset callback if one
        was provided, and finally resets the face to happy.

        The shocked state provides visual feedback during the click action,
        mimicking the classic Windows Mine Detector behavior.
        """
        # Show shocked face momentarily
        self.set_shocked()
        self.frame.update_idletasks()

        # Invoke reset callback if provided
        if self.on_reset:
            self.on_reset()

        # Reset to happy face after click
        self.set_happy()

    def set_happy(self) -> None:
        """
        Set the button to show the happy face.

        The happy face is displayed during normal gameplay when the game
        is in progress and the player is not currently clicking a cell.
        """
        self.current_state = "happy"
        self._update_icon("happy")

    def set_shocked(self) -> None:
        """
        Set the button to show the shocked face.

        The shocked face is displayed momentarily when the player clicks
        on a cell, providing visual feedback for the click action. This state
        is typically shown during mouse button press and reverted after release.
        """
        self.current_state = "shocked"
        self._update_icon("shocked")

    def set_dead(self) -> None:
        """
        Set the button to show the dead face.

        The dead face is displayed when the game is lost (a mine was
        clicked). This state persists until the game is reset.
        """
        self.current_state = "dead"
        self._update_icon("dead")

    def set_cool(self) -> None:
        """
        Set the button to show the cool face.

        The cool face is displayed when the game is won (all non-mine
        cells have been revealed). This state persists until the game
        is reset.
        """
        self.current_state = "cool"
        self._update_icon("cool")

    def _update_icon(self, icon_type: str) -> None:
        """
        Update the displayed icon on the canvas.

        Clears the current canvas and redraws the specified icon.

        Args:
            icon_type: Type of icon to display
        """
        self.icon_canvas.delete("all")
        from src.ui.win95_icons import Win95Icons
        Win95Icons.draw_happy_face if icon_type == "happy" else \
            Win95Icons.draw_shocked_face if icon_type == "shocked" else \
            Win95Icons.draw_dead_face if icon_type == "dead" else \
            Win95Icons.draw_cool_face(
                self.icon_canvas, 0, 0, 26
            )

    def set_state(self, state: str) -> None:
        """
        Set the button face state by name.

        This is a convenience method to set the face state using a string
        name instead of calling the specific set_* methods. Useful for
        programmatic state updates based on game state enums.

        Args:
            state: The face state to set ("happy", "shocked", "dead", or "cool").

        Raises:
            ValueError: If the state name is not recognized.
        """
        if state not in self.VALID_STATES:
            raise ValueError(
                f"Invalid face state: {state}. "
                f"Must be one of {list(self.VALID_STATES)}"
            )

        if state == "happy":
            self.set_happy()
        elif state == "shocked":
            self.set_shocked()
        elif state == "dead":
            self.set_dead()
        elif state == "cool":
            self.set_cool()

    def get_state(self) -> str:
        """
        Get the current face state.

        Returns the name of the currently displayed face state.

        Returns:
            The current face state name ("happy", "shocked", "dead", or "cool").
        """
        return self.current_state

    def pack(self, **kwargs) -> None:
        """
        Pack the button frame into the parent widget.

        This is a convenience method that delegates to the frame's pack method,
        allowing the reset button to be easily positioned in the main window.

        Args:
            **kwargs: Keyword arguments to pass to frame.pack().
        """
        self.frame.pack(**kwargs)

    def grid(self, **kwargs) -> None:
        """
        Grid the button frame into the parent widget.

        This is a convenience method that delegates to the frame's grid method,
        allowing the reset button to be easily positioned in the main window.

        Args:
            **kwargs: Keyword arguments to pass to frame.grid().
        """
        self.frame.grid(**kwargs)
```

**Visual Impact**: Replaces modern emoji faces with authentic Windows 95 bitmap-style icons drawn on canvas. The face button is the most prominent UI element, so this change dramatically improves authenticity.

---

- [ ] **Task 1.1**: Create `C:\Projects\minedetector\src\ui\win95_icons.py` module
- [ ] **Task 1.2**: Update `ResetButton` class to use canvas-drawn icons instead of emoji
- [ ] **Task 1.3**: Test all four face states (happy, shocked, dead, cool)
- [ ] **Task 1.4**: Adjust icon sizes if needed for visual balance

---

#### 2. Replace Unicode Mine/Flag with Canvas-Drawn Icons
**File**: `C:\Projects\minedetector\src\ui\game_grid.py`
**Effort**: Medium
**Visual Impact**: HIGH - Mines and flags appear constantly during gameplay

**Description**: Replace Unicode mine (💣) and flag (🚩) symbols with canvas-drawn Windows 95 style icons. The current implementation uses emoji characters that look comically modern.

**Before** (current code in `game_grid.py`):
```python
if cell.flagged:
    # Show flag
    button.config(
        text="🚩",
        relief="raised",
        bg="lightgray"
    )
elif cell.revealed:
    if cell.mine:
        # Revealed mine - show mine symbol
        button.config(
            text="💣",
            relief="sunken",
            bg="#c0c0c0"
        )
```

**After**: Use canvas-based rendering or button with bitmap image.

**Option A: Canvas-Based Approach (Recommended)**

Since the game uses buttons for cells, we need to modify the approach. The cleanest solution is to create images from canvas drawings and apply them to buttons. Add this helper to `win95_icons.py`:

```python
def create_icon_photoimage(icon_type: str, size: int = 20) -> tk.PhotoImage:
    """
    Create a PhotoImage from a canvas-drawn icon.

    This creates a temporary canvas, draws the icon, and converts it to
    a PhotoImage that can be used on buttons and labels.

    Args:
        icon_type: Type of icon ('happy', 'shocked', 'dead', 'cool', 'mine', 'flag')
        size: Size of the icon (square)

    Returns:
        PhotoImage object containing the icon
    """
    import tempfile
    import os

    # Create temporary canvas
    canvas = Canvas(tk._default_root, width=size, height=size, highlightthickness=0, bg="#C0C0C0")

    # Draw the icon
    if icon_type == "happy":
        Win95Icons.draw_happy_face(canvas, 0, 0, size)
    elif icon_type == "shocked":
        Win95Icons.draw_shocked_face(canvas, 0, 0, size)
    elif icon_type == "dead":
        Win95Icons.draw_dead_face(canvas, 0, 0, size)
    elif icon_type == "cool":
        Win95Icons.draw_cool_face(canvas, 0, 0, size)
    elif icon_type == "mine":
        Win95Icons.draw_mine(canvas, 0, 0, size)
    elif icon_type == "flag":
        Win95Icons.draw_flag(canvas, 0, 0, size)
    else:
        raise ValueError(f"Unknown icon type: {icon_type}")

    # Save canvas to PostScript and convert to GIF (requires PIL)
    # Note: This approach requires PIL/Pillow. Alternative: Use bitmap characters.
    # For a simpler approach without external dependencies, see Option B below.

    canvas.destroy()
```

**Option B: Built-in Bitmap Approach (Simpler, No Dependencies)**

For maximum compatibility and simplicity, use Tkinter's built-in bitmap capability with custom XBM (X Bitmap) format. Add these bitmap definitions to `win95_icons.py`:

```python
# Windows 95 Mine Icon (XBM format)
MINE_XBM = """
#define mine_width 16
#define mine_height 16
static unsigned char mine_bits[] = {
  0x00, 0x00, 0x30, 0x03, 0x38, 0x07, 0x3c, 0x0f, 0x3e, 0x1f,
  0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0x7e, 0x3f, 0x3c, 0x1f,
  0x38, 0x07, 0x30, 0x03, 0x00, 0x00, 0x00, 0x00};
"""

# Windows 95 Flag Icon (XBM format)
FLAG_XBM = """
#define flag_width 16
#define flag_height 16
static unsigned char flag_bits[] = {
  0x00, 0x00, 0x80, 0x01, 0x80, 0x01, 0xc0, 0x03, 0xe0, 0x02,
  0xf0, 0x02, 0xc0, 0x03, 0x80, 0x01, 0x80, 0x01, 0x80, 0x01,
  0x80, 0x01, 0x80, 0x01, 0xf0, 0x0f, 0x00, 0x00};
"""

# Alternative: Use text characters with proper styling
# The Windows 95 mine looked like a spiky ball, can approximate with
# a combination of characters or use the canvas approach above


def create_mine_bitmap() -> tk.BitmapImage:
    """Create a bitmap image for the mine icon."""
    # Write XBM to temporary file
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.xbm', delete=False) as f:
        f.write(MINE_XBM)
        temp_path = f.name

    bitmap = tk.BitmapImage(file=temp_path, background="#C0C0C0")
    return bitmap


def create_flag_bitmap() -> tk.BitmapImage:
    """Create a bitmap image for the flag icon."""
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.xbm', delete=False) as f:
        f.write(FLAG_XBM)
        temp_path = f.name

    bitmap = tk.BitmapImage(file=temp_path, background="#C0C0C0")
    return bitmap
```

**Actually, the simplest authentic approach: Use button text with characters**

The original Windows 95 Minesweeper used specific text characters for mine and flag. Let's use a simpler approach that doesn't require bitmaps:

In `game_grid.py`, update the cell display logic:

```python
def update_cell(self, row: int, col: int) -> None:
    """
    Update the visual appearance of a single cell.

    Refreshes the display of the specified cell button based on its current
    state in the board. This handles all possible cell states:
    - Unrevealed: Raised button with no text
    - Revealed mine: Sunken button with mine symbol
    - Revealed numbered: Sunken button with number (1-8) in appropriate color
    - Flagged: Raised button with flag symbol
    """
    if not self.board.is_valid_coordinate(row, col):
        raise IndexError(
            f"Cannot update cell ({row}, {col}): "
            f"out of bounds for board size ({self.board.rows}x{self.board.cols})"
        )

    cell = self.board.get_cell(row, col)
    button = self.buttons[row][col]

    if cell.flagged:
        # Show flag - use authentic Windows 95 style
        # The original used a red flag on black pole
        button.config(
            text="⚑",  # This is the closest Unicode character to Windows flag
            relief="raised",
            bg="#C0C0C0",  # Windows 95 gray
            fg="#FF0000",  # Red flag
            font=("Wingdings", 14)  # Wingdings has authentic Windows symbols
        )
    elif cell.revealed:
        if cell.mine:
            # Revealed mine - show mine symbol
            button.config(
                text="*",  # Asterisk was used in early Windows versions
                # Or use "●" for a more modern look
                relief="sunken",
                bg="#808080",  # Darker gray for revealed mines
                fg="#000000",
                font=("Courier", 16, "bold")
            )
        elif cell.adjacent_mines > 0:
            # Revealed numbered cell - show number with color
            button.config(
                text=str(cell.adjacent_mines),
                relief="sunken",
                bg="#C0C0C0",  # Windows 95 revealed cell color
                fg=self.NUMBER_COLORS.get(cell.adjacent_mines, "black"),
                font=("Arial", 10, "bold")
            )
        else:
            # Revealed blank cell (0 adjacent mines)
            button.config(
                text="",
                relief="sunken",
                bg="#C0C0C0"  # Windows 95 revealed cell color
            )
    else:
        # Unrevealed cell - Windows 95 raised 3D effect
        button.config(
            text="",
            relief="raised",
            bg="#C0C0C0",  # Windows 95 gray (not lightgray)
            bd=2,  # Standard border width for 3D effect
            font=("Arial", 10, "bold")
        )
```

**For even more authentic symbols**, we can use the Wingdings font which comes with Windows:

```python
# Add to GameGrid class __init__ method:
self.button.config(font=("Wingdings", 14))

# Then use these characters:
# Flag: "F" in Wingdings = flag character
# Mine: "M" or "W" in Wingdings has mine-like symbols
# Or use regular font with these approximations:
# Flag: "⚑" (U+2691)
# Mine: "💣" is too modern, use "*" or "+" instead
```

**Recommended Implementation (Best Balance)**:

Create a new module `C:\Projects\minedetector\src\ui\win95_symbols.py`:

```python
"""
Windows 95 Symbols Module

Defines the text-based symbols used in Windows 95 Minesweeper.
Uses font selection and character choices that match the original game.
"""

# Windows 95 color scheme
WIN95_COLORS = {
    "background": "#C0C0C0",  # Standard Windows gray
    "button_face": "#C0C0C0",
    "button_shadow": "#808080",  # Dark gray for shadows
    "button_highlight": "#FFFFFF",  # White for highlights
    "revealed_cell": "#C0C0C0",
    "mine_revealed": "#808080",  # Darker background for revealed mines
    "mine_foreground": "#000000",  # Black mine
    "flag_foreground": "#FF0000",  # Red flag
}

# Symbol definitions
# Windows 95 Minesweeper used simple ASCII characters
SYMBOLS = {
    "mine": "*",  # Asterisk for mine (authentic)
    "mine_highlight": "X",  # X for incorrectly flagged mine
    "flag": "F",  # F for flag (when using special fonts)
    "question": "?",  # Question mark for question mark mode
    "exclamation": "!",  # Exclamation for game over
}

# Color definitions for numbers 1-8 (matching Windows 95)
NUMBER_COLORS = {
    1: "#0000FF",  # Blue
    2: "#008000",  # Green
    3: "#FF0000",  # Red
    4: "#000080",  # Dark Blue/Navy
    5: "#800000",  # Maroon
    6: "#008080",  # Teal
    7: "#000000",  # Black
    8: "#808080",  # Gray
}

# Font specifications
FONTS = {
    "numbers": ("Arial", 10, "bold"),
    "mine": ("Courier New", 14, "bold"),
    "flag": ("Wingdings", 12),  # Wingdings has flag at char 'F'
    "lcd": ("Courier New", 20, "bold"),  # LCD-style for timer/counter
}


def get_mine_text() -> str:
    """Return the text character for mine display."""
    return SYMBOLS["mine"]


def get_flag_text() -> str:
    """Return the text character for flag display."""
    # Try to use Wingdings if available, otherwise use Unicode
    try:
        import tkinter as tk
        test = tk.Label(text="F", font=("Wingdings", 12))
        # If Wingdings is available, use character 'F'
        # In Wingdings, 'F' renders as a flag
        return "F"
    except:
        # Fallback to Unicode flag character
        return "⚑"  # U+2691 - Flag symbol


def get_number_color(number: int) -> str:
    """
    Get the Windows 95 color for a number.

    Args:
        number: The number (1-8)

    Returns:
        Hex color string

    Raises:
        ValueError: If number is not in range 1-8
    """
    if number not in NUMBER_COLORS:
        raise ValueError(f"Number must be 1-8, got {number}")
    return NUMBER_COLORS[number]
```

Then update `game_grid.py`:

```python
# At top of file
from src.ui.win95_symbols import get_mine_text, get_flag_text, get_number_color

# In update_cell method:
if cell.flagged:
    button.config(
        text=get_flag_text(),
        relief="raised",
        bg="#C0C0C0",
        fg="#FF0000",
        font=("Wingdings", 12)
    )
elif cell.revealed:
    if cell.mine:
        button.config(
            text=get_mine_text(),
            relief="sunken",
            bg="#808080",
            fg="#000000",
            font=("Courier New", 14, "bold")
        )
    elif cell.adjacent_mines > 0:
        button.config(
            text=str(cell.adjacent_mines),
            relief="sunken",
            bg="#C0C0C0",
            fg=get_number_color(cell.adjacent_mines),
            font=("Arial", 10, "bold")
        )
    else:
        button.config(
            text="",
            relief="sunken",
            bg="#C0C0C0"
        )
else:
    button.config(
        text="",
        relief="raised",
        bg="#C0C0C0",
        bd=2
    )
```

**Visual Impact**: Replaces cartoonish emoji with authentic Windows 95 symbols. The mine appears frequently during gameplay, and flags are constantly used, so this significantly improves the retro feel.

---

- [ ] **Task 2.1**: Create `C:\Projects\minedetector\src\ui\win95_symbols.py` module
- [ ] **Task 2.2**: Update `GameGrid.update_cell()` to use Win95 symbols
- [ ] **Task 2.3**: Update `NUMBER_COLORS` constant in `GameGrid` with hex values
- [ ] **Task 2.4**: Test flag and mine display on cells
- [ ] **Task 2.5**: Verify Wingdings font availability or provide fallback

---

#### 3. Fix Cell Colors to Match Windows 95 Palette
**File**: `C:\Projects\minedetector\src\ui\game_grid.py`
**Effort**: Small
**Visual Impact**: MEDIUM - Affects entire game board appearance

**Description**: Replace generic color names with exact Windows 95 hex values. Currently using "lightgray", "dark blue", etc., which don't match the original.

**Before** (current code):
```python
NUMBER_COLORS = {
    1: "blue",
    2: "green",
    3: "red",
    4: "dark blue",
    5: "#800000",  # Dark brown/maroon
    6: "teal",
    7: "black",
    8: "gray"
}
```

**After**:
```python
# Windows Minesweeper number colors (exact RGB values from original)
NUMBER_COLORS = {
    1: "#0000FF",  # Blue
    2: "#008000",  # Green
    3: "#FF0000",  # Red
    4: "#000080",  # Dark Blue/Navy
    5: "#800000",  # Maroon
    6: "#008080",  # Teal
    7: "#000000",  # Black
    8: "#808080",  # Gray
}
```

**Cell background colors**:
```python
# In _create_grid method, update button initialization:
button = tk.Button(
    self.frame,
    width=2,
    height=1,
    relief="raised",
    bd=2,
    bg="#C0C0C0",  # Windows 95 standard gray
    font=("Arial", 10, "bold")
)

# In update_cell method:
# Unrevealed cells:
button.config(bg="#C0C0C0")

# Revealed cells:
button.config(bg="#C0C0C0")  # Same gray, just sunken relief

# Revealed mines (different background):
button.config(bg="#808080")  # Darker gray
```

**Visual Impact**: Subtle but important - exact color matching makes the game feel authentic. Users familiar with Windows 95 will notice the difference.

---

- [ ] **Task 3.1**: Update `NUMBER_COLORS` constant with hex values
- [ ] **Task 3.2**: Change `bg="lightgray"` to `bg="#C0C0C0"` throughout
- [ ] **Task 3.3**: Use `#808080` for revealed mine backgrounds
- [ ] **Task 3.4**: Verify colors against Windows 95 reference images

---

### MEDIUM PRIORITY

#### 4. Add Proper 3D Bevel Effects to Borders
**File**: `C:\Projects\minedetector\src\ui\game_grid.py`, `C:\Projects\minedetector\src\ui\main_window.py`
**Effort**: Medium
**Visual Impact**: MEDIUM - Creates depth and authentic Windows look

**Description**: Implement proper 3D bevel effects with highlight (white) and shadow (dark gray) borders. Windows 95 UI is defined by these raised/sunken effects.

**Current Implementation**:
The current code uses `relief="raised"` and `relief="sunken"`, which Tkinter handles automatically. However, we can enhance this with custom bevels for the main border.

**Enhanced Main Border**:

In `game_grid.py`, update the frame creation:

```python
def __init__(
    self,
    parent: tk.Widget,
    board: Board,
    cell_size: int = 30,
    on_cell_click: Optional[Callable[[int, int]], None] = None,
    on_cell_right_click: Optional[Callable[[int, int]], None] = None,
    is_input_allowed: Optional[Callable[[], bool]] = None
):
    # ... existing validation code ...

    self.parent = parent
    self.board = board
    self.cell_size = cell_size
    self.on_cell_click = on_cell_click
    self.on_cell_right_click = on_cell_right_click
    self.is_input_allowed = is_input_allowed

    # Create frame with proper Windows 95 sunken border
    # The sunken effect creates the "game well" appearance
    self.frame = tk.Frame(
        parent,
        relief="sunken",
        bd=3,  # Increase border width for more pronounced 3D effect
        bg="#C0C0C0"  # Match Windows 95 background
    )

    # Initialize buttons storage
    self.buttons: list[list[tk.Button]] = []

    # Create the grid of buttons
    self._create_grid()
```

**Optional: Custom Bevel Drawing for Extra Polish**:

For even more authentic bevels, you can add a custom border frame:

```python
def _create_3d_border(self, parent, thickness=2) -> tk.Frame:
    """
    Create a custom 3D border frame with Windows 95 styling.

    Windows 95 3D borders consist of:
    - Top/Left: White highlight (#FFFFFF)
    - Bottom/Right: Dark shadow (#808080)

    Args:
        parent: Parent widget
        thickness: Border thickness in pixels

    Returns:
        Frame with 3D border effect
    """
    border = tk.Frame(parent, bg="#C0C0C0", bd=0)

    # Create highlight (top and left edges)
    tk.Frame(border, bg="#FFFFFF", height=thickness).place(
        x=0, y=0, relwidth=1, anchor="nw"
    )
    tk.Frame(border, bg="#FFFFFF", width=thickness).place(
        x=0, y=0, relheight=1, anchor="nw"
    )

    # Create shadow (bottom and right edges)
    tk.Frame(border, bg="#808080", height=thickness).place(
        x=0, rely=1.0, relwidth=1, anchor="sw"
    )
    tk.Frame(border, bg="#808080", width=thickness).place(
        relx=1.0, y=0, relheight=1, anchor="ne"
    )

    return border
```

**Cell Button 3D Effects**:

Ensure cell buttons have proper 3D appearance by checking relief settings:

```python
def _create_grid(self) -> None:
    """Create the 2D grid of clickable cell buttons."""
    self.buttons = []

    for row in range(self.board.rows):
        button_row = []
        for col in range(self.board.cols):
            button = tk.Button(
                self.frame,
                width=2,
                height=1,
                relief="raised",  # Raised for unrevealed cells
                bd=2,  # Standard 3D border width
                bg="#C0C0C0",
                activebackground="#C0C0C0",  # No color change on click
                font=("Arial", 10, "bold"),
                highlightthickness=0  # Remove focus highlight (not Win95 style)
            )

            # ... event binding code ...

            button.grid(row=row, column=col, padx=0, pady=0)
            button_row.append(button)
        self.buttons.append(button_row)
```

**Visual Impact**: The 3D bevel effects are essential for the Windows 95 aesthetic. The raised/sunken states provide tactile feedback and depth.

---

- [ ] **Task 4.1**: Increase border depth on game frame (`bd=3`)
- [ ] **Task 4.2**: Add `highlightthickness=0` to cell buttons
- [ ] **Task 4.3**: Set `activebackground="#C0C0C0"` to prevent color changes
- [ ] **Task 4.4**: Optionally implement custom 3D border helper function
- [ ] **Task 4.5**: Test raised/sken transitions during gameplay

---

#### 5. Replace LCD Font with True 7-Segment Style
**Files**: `C:\Projects\minedetector\src\ui\mine_counter.py`, `C:\Projects\minedetector\src\ui\timer.py`
**Effort**: Medium
**Visual Impact**: MEDIUM - Timer and counter are always visible

**Description**: The current LCD display uses Courier font, which doesn't look like the 7-segment LED displays in the original Windows Minesweeper.

**Before** (current code):
```python
font=("Courier", 20, "bold")
```

**After**: Use a custom 7-segment font or draw LCD segments on canvas.

**Option A: Use Digital-7 Font (Requires Font File)**

If you can include a font file with the application, use the "Digital-7" font which is freely available and closely matches the Windows LCD style.

```python
# If Digital-7 font is installed or bundled:
font=("Digital-7", 20, "bold")
```

**Option B: Draw LCD Segments on Canvas (Authentic, No External Dependencies)**

Create a new module `C:\Projects\minedetector\src\ui\lcd_display.py`:

```python
"""
LCD Display Module

Provides authentic 7-segment LED display rendering for the timer and counter.
Matches the Windows 95 Minesweeper LCD style.
"""

import tkinter as tk
from typing import Optional


class LCDDisplay:
    """
    Renders 7-segment LCD-style numbers on a canvas.

    The 7-segment display consists of 7 segments labeled A-G:
        AAA
       F   B
       F   B
        GGG
       E   C
       E   C
        DDD

    Each digit (0-9) is formed by lighting specific segments.
    """

    # Segment definitions for each digit (0-9)
    # Order: A, B, C, D, E, F, G (top, top-right, bottom-right, bottom, bottom-left, top-left, middle)
    SEGMENTS = {
        0: [1, 1, 1, 1, 1, 1, 0],  # A, B, C, D, E, F
        1: [0, 1, 1, 0, 0, 0, 0],  # B, C
        2: [1, 1, 0, 1, 1, 0, 1],  # A, B, D, E, G
        3: [1, 1, 1, 1, 0, 0, 1],  # A, B, C, D, G
        4: [0, 1, 1, 0, 0, 1, 1],  # B, C, F, G
        5: [1, 0, 1, 1, 0, 1, 1],  # A, C, D, F, G
        6: [1, 0, 1, 1, 1, 1, 1],  # A, C, D, E, F, G
        7: [1, 1, 1, 0, 0, 0, 0],  # A, B, C
        8: [1, 1, 1, 1, 1, 1, 1],  # All segments
        9: [1, 1, 1, 1, 0, 1, 1],  # A, B, C, D, F, G
    }

    def __init__(
        self,
        parent: tk.Widget,
        value: int = 0,
        digit_count: int = 3,
        size: str = "large"
    ):
        """
        Initialize an LCD display.

        Args:
            parent: Parent widget
            value: Initial value to display
            digit_count: Number of digits (default: 3 for Windows Mine Detector)
            size: Display size ("large" or "small")
        """
        self.value = value
        self.digit_count = digit_count

        # Size configuration
        if size == "large":
            self.width = 80
            self.height = 30
            self.segment_width = 4
        else:
            self.width = 60
            self.height = 20
            self.segment_width = 3

        # Create canvas with LCD background (red)
        self.canvas = tk.Canvas(
            parent,
            width=self.width,
            height=self.height,
            bg="#FF0000",  # Red LCD background
            highlightthickness=0,
            bd=0
        )

        # Draw initial value
        self.update_display(value)

    def update_display(self, value: int) -> None:
        """
        Update the displayed value.

        Args:
            value: New value to display (will be clamped to 0-999)
        """
        # Clamp to display range
        self.value = max(0, min(999, value))

        # Clear canvas
        self.canvas.delete("all")

        # Format as zero-padded string
        value_str = f"{self.value:0{self.digit_count}d}"

        # Calculate digit positioning
        digit_width = self.width // self.digit_count
        digit_spacing = 4

        # Draw each digit
        for i, char in enumerate(value_str):
            digit = int(char)
            x_offset = i * digit_width + digit_spacing // 2
            self._draw_digit(x_offset, digit, digit_width - digit_spacing)

    def _draw_digit(self, x: int, digit: int, width: int) -> None:
        """
        Draw a single 7-segment digit.

        Args:
            x: X coordinate of the digit
            digit: Digit to draw (0-9)
            width: Width of the digit area
        """
        segments = self.SEGMENTS[digit]

        # Calculate segment positions
        margin = 4
        segment_length = width - 2 * margin
        half_length = segment_length // 2
        center_y = self.height // 2

        # Define segment coordinates
        # A: Top horizontal
        seg_a = [(x + margin, center_y - half_length),
                 (x + margin + segment_length, center_y - half_length)]

        # B: Top-right vertical
        seg_b = [(x + margin + segment_length, center_y - half_length),
                 (x + margin + segment_length, center_y)]

        # C: Bottom-right vertical
        seg_c = [(x + margin + segment_length, center_y),
                 (x + margin + segment_length, center_y + half_length)]

        # D: Bottom horizontal
        seg_d = [(x + margin, center_y + half_length),
                 (x + margin + segment_length, center_y + half_length)]

        # E: Bottom-left vertical
        seg_e = [(x + margin, center_y),
                 (x + margin, center_y + half_length)]

        # F: Top-left vertical
        seg_f = [(x + margin, center_y - half_length),
                 (x + margin, center_y)]

        # G: Middle horizontal
        seg_g = [(x + margin, center_y),
                 (x + margin + segment_length, center_y)]

        # All segment definitions
        all_segments = [seg_a, seg_b, seg_c, seg_d, seg_e, seg_f, seg_g]

        # Draw active segments (black)
        for i, segment in enumerate(all_segments):
            if segments[i]:
                self.canvas.create_line(
                    segment[0], segment[1],
                    fill="#000000",
                    width=self.segment_width,
                    capstyle=tk.ROUND
                )

    def get_canvas(self) -> tk.Canvas:
        """Get the canvas widget for packing/gridding."""
        return self.canvas
```

Then update `mine_counter.py` and `timer.py` to use the LCD display:

```python
# In mine_counter.py:
from src.ui.lcd_display import LCDDisplay

# Replace the label creation with:
# Create LCD-style counter display
self.lcd = LCDDisplay(
    parent,
    value=self.current_count,
    digit_count=3,
    size="large"
)

# Update _update_display method:
def _update_display(self) -> None:
    """Update the counter display and colors."""
    self.lcd.update_display(self.current_count)

    # Note: Colors are now handled by LCD canvas (black on red by default)
    # For negative values, we could invert colors if desired

# Update pack/grid methods to use lcd.canvas instead of label
```

**Simpler Alternative: Use System Font with LCD Styling**

If the full canvas implementation is too complex, use a monospaced font with styling to approximate the LCD look:

```python
# Create label with LCD-like appearance
self.label = tk.Label(
    parent,
    text=str(self._format_display(self.current_count)),
    font=("Lucida Console", 20, "bold"),  # More digital than Courier
    width=4,
    relief="sunken",
    bd=2,
    fg="#000000",  # Black text
    bg="#FF0000",  # Red background (authentic LCD color)
    highlightthickness=0
)
```

**Visual Impact**: The LCD displays are always visible at the top of the game window. Authentic 7-segment rendering significantly enhances the retro feel.

---

- [ ] **Task 5.1**: Create `C:\Projects\minedetector\src\ui\lcd_display.py` module
- [ ] **Task 5.2**: Update `MineCounter` to use `LCDDisplay`
- [ ] **Task 5.3**: Update `GameTimer` to use `LCDDisplay`
- [ ] **Task 5.4**: Test digit transitions and edge cases (000, 999, negative)
- [ ] **Task 5.5**: Adjust segment width and spacing for readability

---

#### 6. Improve Number Font Styling
**File**: `C:\Projects\minedetector\src\ui\game_grid.py`
**Effort**: Small
**Visual Impact**: LOW-MEDIUM - Numbers are important gameplay elements

**Description**: The current number font is adequate but could more closely match Windows 95 styling. Windows 95 used bold Arial or MS Sans Serif for numbers.

**Current Code**:
```python
font=("Arial", 10, "bold")
```

**Improved Version**:
```python
# MS Sans Serif was the default Windows 95 UI font
# Arial is an acceptable substitute
font=("MS Sans Serif", 10, "bold")  # Try MS Sans Serif first
# Fallback to Arial if MS Sans Serif not available
# font=("Arial", 9, "bold")  # Slightly smaller for authenticity
```

**Actually, the original Windows 95 Minesweeper used pixel-perfect bitmaps for numbers. For a Python implementation, we have these options:**

**Option A: Use Font with Specific Styling**
```python
# In GameGrid class initialization:
self.number_font = ("Arial", 9, "bold")  # Size 9 is more authentic

# In update_cell method, when setting numbered cells:
button.config(
    text=str(cell.adjacent_mines),
    relief="sunken",
    bg="#C0C0C0",
    fg=self.NUMBER_COLORS.get(cell.adjacent_mines, "black"),
    font=self.number_font
)
```

**Option B: Use Tahoma Font (Available on most Windows systems)**
```python
font=("Tahoma", 9, "bold")  # Tahoma is closer to Windows 95 aesthetic than Arial
```

**Recommendation**:
```python
# Use Tahoma on Windows, fallback to Arial elsewhere
import sys
if sys.platform == "win32":
    NUMBER_FONT = ("Tahoma", 9, "bold")
else:
    NUMBER_FONT = ("Arial", 9, "bold")
```

**Visual Impact**: Numbers are the primary gameplay feedback mechanism. While not as dramatic as icons, proper font styling adds to overall authenticity.

---

- [ ] **Task 6.1**: Define platform-specific font constants
- [ ] **Task 6.2**: Update number cell font to use Tahoma on Windows
- [ ] **Task 6.3**: Test font rendering on different platforms
- [ ] **Task 6.4**: Adjust font size if numbers look too large/small

---

### LOW PRIORITY

#### 7. Add Question Mark Feature (Optional Windows Feature)
**File**: `C:\Projects\minedetector\src\ui\game_grid.py`, `C:\Projects\minedetector\src\ui\main_window.py`
**Effort**: Large
**Visual Impact**: LOW - This was an optional feature in Windows 95

**Description**: Windows 95 Minesweeper had a question mark mode that could be enabled via the menu. Right-clicking would cycle through empty → flag → question mark → empty.

**Note**: This requires:
1. Adding a menu option to toggle question mark mode
2. Modifying the right-click handler to cycle through three states
3. Adding question mark rendering (the "?" symbol)
4. Updating chording logic to ignore question marks

**Implementation Sketch**:

```python
# In main_window.py, add to _create_menu method:
game_menu.add_separator()
self.question_mode = tk.BooleanVar(value=False)
game_menu.add_checkbutton(
    label="Marks (?)",
    variable=self.question_mode,
    command=self._toggle_question_mode
)

# In game_grid.py, modify _handle_right_click:
def _handle_right_click(self, row: int, col: int) -> None:
    """Handle right-click event with optional question mark mode."""
    if self.is_input_allowed and not self.is_input_allowed():
        return

    cell = self.board.get_cell(row, col)

    if cell.revealed:
        return

    # Get question mode setting from parent
    question_enabled = self.parent.question_mode.get() if hasattr(self.parent, 'question_mode') else False

    if cell.flagged:
        # If question mode enabled, convert to question mark
        if question_enabled:
            cell.flagged = False
            cell.questioned = True  # New cell attribute
        else:
            # Normal mode: just remove flag
            cell.flagged = False
            if self.mine_counter:
                self.mine_counter.increment()
    elif cell.questioned:
        # Remove question mark
        cell.questioned = False
    else:
        # Place flag
        cell.flagged = True
        if self.mine_counter:
            self.mine_counter.decrement()

    if self.game_grid:
        self.game_grid.update_cell(row, col)

# In update_cell method, handle question state:
elif cell.questioned:
    button.config(
        text="?",
        relief="raised",
        bg="#C0C0C0",
        fg="#000000",
        font=("Arial", 10, "bold")
    )
```

**Visual Impact**: This was an optional feature in Windows 95, not core to the visual identity. Implement it only if you want 100% feature parity.

---

- [ ] **Task 7.1**: Add `questioned` attribute to Cell model
- [ ] **Task 7.2**: Add "Marks (?)" menu item to Game menu
- [ ] **Task 7.3**: Implement 3-state right-click cycle (empty → flag → question → empty)
- [ ] **Task 7.4**: Update `update_cell()` to render question marks
- [ ] **Task 7.5**: Test chording with question marks (should ignore them)

---

#### 8. Create Custom Window Title Bar (Advanced)
**File**: `C:\Projects\minedetector\src\ui\main_window.py`
**Effort**: Large
**Visual Impact**: LOW - Nice to have, but not essential

**Description**: Windows 95 had distinctive title bars with the gradient effect. While Tkinter uses the system default, you could create a custom title bar.

**Note**: This is very complex in Tkinter and involves:
1. Removing the default window decorations (`overrideredirect(True)`)
2. Drawing a custom title bar
3. Implementing window dragging
4. Implementing minimize/close buttons

**Recommendation**: Skip this unless you want pixel-perfect authenticity. The system title bar is close enough for most users.

**Alternative**: Just ensure the window title matches Windows 95 format:

```python
# In __init__ method of MainWindow:
# Windows 95 Minesweeper title format:
self.root.title("Minesweeper")  # Or "Minedetector" if keeping current name
```

**Visual Impact**: Minimal. Most users won't notice the difference between system title bar and Windows 95 style.

---

- [ ] **Task 8.1**: Update window title to "Minesweeper" (if desired)
- [ ] **Task 8.2**: Optionally implement custom title bar (advanced)
- [ ] **Task 8.3**: Test window dragging and controls if implementing custom bar

---

#### 9. Add Menu Icons (Nice to Have)
**File**: `C:\Projects\minedetector\src\ui\main_window.py`
**Effort**: Medium
**Visual Impact**: LOW - Menus are rarely used after setup

**Description**: Windows 95 menus had icons next to certain items. You can add icons to the Game menu items.

**Implementation**:

```python
# In _create_menu method, create icon images:
# Note: This requires icon image files or data URIs

# Example using built-in bitmaps (limited options):
game_menu = tk.Menu(menubar, tearoff=0)

# Add menu items with icons (using tk image types)
# You would need to create small icon images first
```

**Recommendation**: Skip this. Menu icons require external image files or complex data URI embedding, and the visual payoff is minimal.

**Visual Impact**: Very low - menus are opened infrequently.

---

- [ ] **Task 9.1**: Create or source menu icon images (8x8 or 12x12 pixels)
- [ ] **Task 9.2**: Convert icons to Tkinter-compatible format
- [ ] **Task 9.3**: Add icons to Game menu items
- [ ] **Task 9.4**: Test menu rendering with icons

---

#### 10. Fine-Tune Cell Spacing and Grid Layout
**File**: `C:\Projects\minedetector\src\ui\game_grid.py`
**Effort**: Small
**Visual Impact**: LOW - Minor visual polish

**Description**: Ensure cell spacing matches Windows 95 exactly. The original had no gaps between cells, creating a seamless grid.

**Current Code**:
```python
button.grid(row=row, column=col, padx=0, pady=0)
```

**Check**: The current implementation already has `padx=0, pady=0`, which is correct. Verify that buttons are sized correctly.

**Cell Size Adjustment**:

Windows 95 Minesweeper cells were approximately 16x16 pixels. The current implementation uses `width=2, height=1` which varies by system.

**For consistency**, specify exact pixel sizes:

```python
# In _create_grid method:
button = tk.Button(
    self.frame,
    width=16,  # Pixel width (character width varies)
    height=1,  # Height in text lines
    relief="raised",
    bd=2,
    bg="#C0C0C0",
    font=("Arial", 10, "bold")
)
```

**Note**: Tkinter's `width` parameter is in characters for text, not pixels. For exact pixel sizing, you'd need to:
1. Use a Frame instead of Button
2. Draw the cell manually on a Canvas
3. Or accept approximate sizing

**Recommendation**: Current implementation is acceptable. Exact pixel sizing is not worth the complexity.

**Visual Impact**: Minimal - the current grid looks correct.

---

- [ ] **Task 10.1**: Verify cell spacing matches original (no gaps)
- [ ] **Task 10.2**: Test on different screen resolutions/DPI settings
- [ ] **Task 10.3**: Adjust if cells look too large or small

---

#### 11. Add Window Icon (Taskbar Display)
**File**: `C:\Projects\minedetector\main.py` or `C:\Projects\minedetector\src\ui\main_window.py`
**Effort**: Small
**Visual Impact**: LOW - Only visible in taskbar and alt-tab

**Description**: Add a custom window icon so the game shows a minesweeper icon in the taskbar instead of the default Python icon.

**Implementation**:

```python
# In main_window.py __init__ method:
def __init__(self):
    # Create the main Tkinter window
    self.root = tk.Tk()

    # Set window title
    self.root.title("Mine Detector")

    # Set window icon (requires .ico file)
    try:
        self.root.iconbitmap("C:/Projects/minedetector/icons/minesweeper.ico")
    except tk.TclError:
        # Icon file not found, use default
        pass
```

**Creating the Icon**:
1. Extract or recreate the Windows 95 Minesweeper icon
2. Save as `.ico` file (16x16, 32x32 sizes)
3. Place in project directory

**Alternative: Use base64-encoded icon** (no external file needed):

```python
import base64
import tkinter as tk

# Base64-encoded .ico file data (would need actual icon data)
ICON_DATA = """
<base64 data would go here>
"""

def set_icon(window):
    """Set window icon from base64 data."""
    try:
        icon_data = base64.b64decode(ICON_DATA)
        # Write to temp file and load
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.ico', delete=False) as f:
            f.write(icon_data)
            temp_path = f.name
        window.iconbitmap(temp_path)
    except:
        pass
```

**Visual Impact**: Low - only affects taskbar and alt-tab display. Nice polish but not essential.

---

- [ ] **Task 11.1**: Source or create Windows 95 Minesweeper .ico file
- [ ] **Task 11.2**: Add icon to `C:\Projects\minedetector\icons\` directory
- [ ] **Task 11.3**: Update `main_window.py` to load icon
- [ ] **Task 11.4**: Test icon display in taskbar and alt-tab

---

#### 12. Implement Custom Colors Module
**File**: Create new file `C:\Projects\minedetector\src\ui\win95_colors.py`
**Effort**: Small
**Visual Impact**: LOW - Code organization improvement

**Description**: Centralize all Windows 95 color definitions in a single module for consistency and easy maintenance.

**Implementation**:

```python
"""
Windows 95 Color Palette Module

Contains all color definitions for authentic Windows 95 Minesweeper appearance.
These colors match the RGB values used in the original Windows 95 winmine.exe.
"""

# ==================== System Colors ====================
# Standard Windows 95 UI colors
WIN95_BACKGROUND = "#C0C0C0"  # Standard Windows gray (RGB: 192, 192, 192)
WIN95_BUTTON_FACE = "#C0C0C0"
WIN95_BUTTON_SHADOW = "#808080"  # Dark gray (RGB: 128, 128, 128)
WIN95_BUTTON_DARK_SHADOW = "#000000"  # Black for deepest shadows
WIN95_BUTTON_HIGHLIGHT = "#FFFFFF"  # White for highlights
WIN95_BUTTON_LIGHT = "#DFDFDF"  # Light gray for subtle highlights

# ==================== Game-Specific Colors ====================
# Cell colors
CELL_UNREVEALED = "#C0C0C0"  # Same as background
CELL_REVEALED = "#C0C0C0"  # Same, just different relief
CELL_MINE_REVEALED = "#808080"  # Darker gray for exploded mines
CELL_MINE_BACKGROUND = "#808080"  # Background for revealed mine
CELL_WRONG_FLAG = "#C0C0C0"  # Background for incorrectly placed flag

# ==================== Number Colors ====================
# Colors for numbers 1-8 (exact Windows 95 values)
NUMBER_1 = "#0000FF"  # Blue (RGB: 0, 0, 255)
NUMBER_2 = "#008000"  # Green (RGB: 0, 128, 0)
NUMBER_3 = "#FF0000"  # Red (RGB: 255, 0, 0)
NUMBER_4 = "#000080"  # Dark Blue/Navy (RGB: 0, 0, 128)
NUMBER_5 = "#800000"  # Maroon (RGB: 128, 0, 0)
NUMBER_6 = "#008080"  # Teal (RGB: 0, 128, 128)
NUMBER_7 = "#000000"  # Black (RGB: 0, 0, 0)
NUMBER_8 = "#808080"  # Gray (RGB: 128, 128, 128)

# Number colors dictionary for easy lookup
NUMBER_COLORS = {
    1: NUMBER_1,
    2: NUMBER_2,
    3: NUMBER_3,
    4: NUMBER_4,
    5: NUMBER_5,
    6: NUMBER_6,
    7: NUMBER_7,
    8: NUMBER_8,
}

# ==================== LCD Display Colors ====================
# Timer and mine counter colors
LCD_BACKGROUND = "#FF0000"  # Red (RGB: 255, 0, 0)
LCD_FOREGROUND = "#000000"  # Black (RGB: 0, 0, 0)
LCD_NEGATIVE_BACKGROUND = "#000000"  # Black (for negative mine counts)
LCD_NEGATIVE_FOREGROUND = "#FF0000"  # Red (for negative mine counts)

# ==================== Icon Colors ====================
# Face button colors
FACE_SKIN = "#FFFF00"  # Yellow/ochre (RGB: 255, 255, 0)
FACE_FEATURES = "#000000"  # Black (RGB: 0, 0, 0)

# Mine icon colors
MINE_BODY = "#000000"  # Black
MINE_HIGHLIGHT = "#FFFFFF"  # White highlight dot
MINE_STROKE = "#000000"  # Black outline

# Flag icon colors
FLAG_RED = "#FF0000"  # Red flag (RGB: 255, 0, 0)
FLAG_POLE = "#000000"  # Black pole
FLAG_OUTLINE = "#000000"  # Black outline

# ==================== Border Colors ====================
# 3D border effect colors
BORDER_OUTER_HIGHLIGHT = "#FFFFFF"  # White
BORDER_INNER_HIGHLIGHT = "#DFDFDF"  # Light gray
BORDER_FACE = "#C0C0C0"  # Standard gray
BORDER_INNER_SHADOW = "#808080"  # Dark gray
BORDER_OUTER_SHADOW = "#000000"  # Black

# ==================== Utility Functions ====================

def get_number_color(number: int) -> str:
    """
    Get the Windows 95 color for a number.

    Args:
        number: The number (1-8)

    Returns:
        Hex color string

    Raises:
        ValueError: If number is not in range 1-8
    """
    if number not in NUMBER_COLORS:
        raise ValueError(f"Number must be 1-8, got {number}")
    return NUMBER_COLORS[number]


def get_lcd_color(is_negative: bool = False) -> tuple:
    """
    Get LCD display colors.

    Args:
        is_negative: True if displaying negative value

    Returns:
        Tuple of (foreground, background) colors
    """
    if is_negative:
        return (LCD_NEGATIVE_FOREGROUND, LCD_NEGATIVE_BACKGROUND)
    return (LCD_FOREGROUND, LCD_BACKGROUND)


# ==================== Color Validation ====================
def validate_colors() -> bool:
    """
    Validate that all color strings are valid hex format.

    Returns:
        True if all colors are valid

    Raises:
        ValueError: If any color is invalid
    """
    import re

    hex_pattern = re.compile(r'^#[0-9A-Fa-f]{6}$')

    # Get all color constants from module
    colors = [
        WIN95_BACKGROUND, WIN95_BUTTON_FACE, WIN95_BUTTON_SHADOW,
        WIN95_BUTTON_DARK_SHADOW, WIN95_BUTTON_HIGHLIGHT, WIN95_BUTTON_LIGHT,
        CELL_UNREVEALED, CELL_REVEALED, CELL_MINE_REVEALED,
        CELL_MINE_BACKGROUND, CELL_WRONG_FLAG,
        LCD_BACKGROUND, LCD_FOREGROUND,
        LCD_NEGATIVE_BACKGROUND, LCD_NEGATIVE_FOREGROUND,
        FACE_SKIN, FACE_FEATURES, MINE_BODY, MINE_HIGHLIGHT,
        MINE_STROKE, FLAG_RED, FLAG_POLE, FLAG_OUTLINE,
        BORDER_OUTER_HIGHLIGHT, BORDER_INNER_HIGHLIGHT,
        BORDER_FACE, BORDER_INNER_SHADOW, BORDER_OUTER_SHADOW,
    ]

    colors.extend(NUMBER_COLORS.values())

    for color in colors:
        if not hex_pattern.match(color):
            raise ValueError(f"Invalid hex color: {color}")

    return True


# Validate colors on module import
try:
    validate_colors()
except ValueError as e:
    print(f"Warning: {e}")
```

**Then update other files to use these constants**:

```python
# In game_grid.py:
from src.ui.win95_colors import (
    CELL_UNREVEALED, CELL_REVEALED, CELL_MINE_REVEALED,
    NUMBER_COLORS, get_number_color, WIN95_BACKGROUND
)

# Use constants instead of hardcoded values:
button.config(
    bg=CELL_UNREVEALED,
    relief="raised"
)
```

**Visual Impact**: No direct visual impact, but improves code organization and ensures consistency across the codebase.

---

- [ ] **Task 12.1**: Create `C:\Projects\minedetector\src\ui\win95_colors.py` module
- [ ] **Task 12.2**: Update `game_grid.py` to use color constants
- [ ] **Task 12.3**: Update `mine_counter.py` to use LCD color constants
- [ ] **Task 12.4**: Update `timer.py` to use LCD color constants
- [ ] **Task 12.5**: Update `win95_icons.py` to use icon color constants
- [ ] **Task 12.6**: Validate all colors against Windows 95 reference

---

## Implementation Order

For maximum visual impact with minimum effort, implement changes in this order:

### Phase 1: Quick Wins (1-2 hours)
**These changes are easy to implement but provide significant visual improvements.**

1. **Fix Colors** (Task 3) - 15 minutes
   - Update `NUMBER_COLORS` with hex values
   - Change backgrounds to `#C0C0C0`
   - Immediate visual improvement

2. **Create Colors Module** (Task 12) - 30 minutes
   - Centralize all color definitions
   - Foundation for other improvements

3. **Improve Font Styling** (Task 6) - 15 minutes
   - Switch to Tahoma on Windows
   - Small but noticeable improvement

### Phase 2: Core Visual Elements (2-4 hours)
**These changes transform the most visible UI elements.**

4. **Replace Mine/Flag Icons** (Task 2) - 1-2 hours
   - Use `win95_symbols.py` module
   - Update `game_grid.py`
   - High visibility during gameplay

5. **Replace Face Icons** (Task 1) - 1-2 hours
   - Create `win95_icons.py` with canvas drawings
   - Update `reset_button.py`
   - Most prominent UI element

### Phase 3: Polish Details (2-3 hours)
**These additions add the final layer of authenticity.**

6. **LCD Display** (Task 5) - 1-2 hours
   - Create `lcd_display.py`
   - Update `mine_counter.py` and `timer.py`
   - Always-visible UI elements

7. **3D Bevel Effects** (Task 4) - 30 minutes
   - Increase border depth
   - Add highlightthickness settings
   - Enhanced depth and realism

### Phase 4: Optional Features (1-2 hours each)
**Implement these only if you want 100% feature parity.**

8. **Question Mark Mode** (Task 7) - 1-2 hours
   - Optional Windows 95 feature
   - Nice to have, not essential

9. **Window Icon** (Task 11) - 30 minutes
   - Taskbar appearance
   - Minor polish

10. **Menu Icons** (Task 9) - 1 hour
    - Rarely seen visual element
    - Lowest priority

---

## Code Snippet Library

### Complete Windows 95 Color Constants

```python
# File: src/ui/win95_colors.py

# System Colors
WIN95_BACKGROUND = "#C0C0C0"
WIN95_BUTTON_SHADOW = "#808080"
WIN95_BUTTON_HIGHLIGHT = "#FFFFFF"

# Number Colors (Windows 95 exact values)
NUMBER_COLORS = {
    1: "#0000FF",  # Blue
    2: "#008000",  # Green
    3: "#FF0000",  # Red
    4: "#000080",  # Navy
    5: "#800000",  # Maroon
    6: "#008080",  # Teal
    7: "#000000",  # Black
    8: "#808080",  # Gray
}

# LCD Colors
LCD_BG = "#FF0000"  # Red
LCD_FG = "#000000"  # Black
```

### Canvas Drawing for Face Icons

```python
# File: src/ui/win95_icons.py

def draw_happy_face(canvas, x, y, size=26):
    """Draw Windows 95 happy face on canvas."""
    center_x, center_y = x + size // 2, y + size // 2

    # Face circle (yellow)
    canvas.create_oval(
        x + 2, y + 2, x + size - 2, y + size - 2,
        fill="#FFFF00", outline="#000000"
    )

    # Eyes (black dots)
    canvas.create_oval(
        center_x - 7, center_y - 5,
        center_x - 3, center_y - 1,
        fill="#000000"
    )
    canvas.create_oval(
        center_x + 3, center_y - 5,
        center_x + 7, center_y - 1,
        fill="#000000"
    )

    # Smile (arc)
    canvas.create_arc(
        center_x - 7, center_y - 2,
        center_x + 7, center_y + 8,
        start=180, extent=180, style="arc",
        outline="#000000", width=2
    )
```

### 3D Bevel Effect

```python
# Add to game frame creation
self.frame = tk.Frame(
    parent,
    relief="sunken",
    bd=3,  # Increased for depth
    bg="#C0C0C0"
)

# Cell button configuration
button = tk.Button(
    self.frame,
    width=2, height=1,
    relief="raised",
    bd=2,
    bg="#C0C0C0",
    highlightthickness=0,  # No focus highlight
    activebackground="#C0C0C0"  # No color change
)
```

### LCD Display Example

```python
# File: src/ui/lcd_display.py

class LCDDisplay:
    """7-segment LCD display for timer and counter."""

    def __init__(self, parent, value=0):
        self.canvas = tk.Canvas(
            parent, width=80, height=30,
            bg="#FF0000", highlightthickness=0
        )
        self.value = value
        self.update()

    def update(self, value):
        """Update displayed value."""
        self.value = max(0, min(999, value))
        self.canvas.delete("all")

        # Draw 7-segment digits
        # (See Task 5 for full implementation)
```

---

## Testing Checklist

After implementing each change, verify:

- [ ] Colors match Windows 95 reference images
- [ ] Icons render correctly on all platforms
- [ ] Fonts are readable and appropriately sized
- [ ] 3D effects provide appropriate depth
- [ ] LCD digits are clear and legible
- [ ] Game functionality is not affected
- [ ] Performance is acceptable (no lag on animations)
- [ ] Window resizes correctly (if applicable)
- [ ] Accessibility is maintained (color contrast, etc.)

---

## Reference Resources

### Windows 95 Minesweeper Screenshots
Search for these to verify authenticity:
- "Windows 95 Minesweeper screenshot"
- "winmine.exe screenshot"
- "Minesweeper Windows 98"

### Color Values
- Windows 95 gray: #C0C0C0 (RGB: 192, 192, 192)
- Dark gray: #808080 (RGB: 128, 128, 128)
- Pure black: #000000
- Pure white: #FFFFFF

### Font Information
- **Primary**: MS Sans Serif (Windows 95 default UI font)
- **Substitutes**: Tahoma, Arial (close matches)
- **Numbers**: Bold, 9-10pt
- **LCD**: Digital-7 or custom 7-segment rendering

---

## Progress Tracking

Use this summary to track overall progress:

### Phase 1: Quick Wins
- [ ] Task 3: Fix Colors
- [ ] Task 12: Colors Module
- [ ] Task 6: Font Styling

### Phase 2: Core Visual Elements
- [ ] Task 2: Mine/Flag Icons
- [ ] Task 1: Face Icons

### Phase 3: Polish Details
- [ ] Task 5: LCD Display
- [ ] Task 4: 3D Bevel Effects

### Phase 4: Optional Features
- [ ] Task 7: Question Mark Mode
- [ ] Task 11: Window Icon
- [ ] Task 9: Menu Icons

### Overall Progress
- [ ] All HIGH priority tasks completed
- [ ] All MEDIUM priority tasks completed
- [ ] Desired LOW priority tasks completed
- [ ] Final testing and polish complete
- [ ] Documentation updated

---

## Notes

1. **Backward Compatibility**: All changes should maintain the current gameplay functionality. These are visual-only improvements.

2. **Cross-Platform**: While targeting Windows 95 aesthetic, ensure the game still looks good on macOS and Linux. Font handling may need platform-specific fallbacks.

3. **Performance**: Canvas drawing and custom icons should not significantly impact performance. Test on lower-end systems.

4. **Maintainability**: The modular approach (separate files for icons, colors, LCD) keeps code organized and makes future updates easier.

5. **Accessibility**: Despite retro styling, maintain reasonable color contrast and avoid relying solely on color to convey information.

---

## Conclusion

Following this action plan will transform Minedetector from a functional modern game into an authentic Windows 95/98 Minesweeper recreation. The prioritized implementation order ensures maximum visual impact with efficient use of development time.

The key to authenticity is attention to detail:
- Exact hex color values
- Proper 3D bevel effects
- Canvas-drawn icons instead of emoji
- LCD-style number displays

Start with the quick wins (Phase 1) for immediate improvement, then tackle the core visual elements (Phase 2) for transformational change. Polish with Phase 3 details, and optionally add Phase 4 features for complete feature parity.

Good luck, and enjoy the nostalgia!
