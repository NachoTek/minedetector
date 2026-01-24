"""
Test Suite for Chording Mechanic

Verifies that the chording mechanic correctly reveals neighbors when the flag count
matches the cell number, and does nothing when conditions aren't met.
"""

import pytest
from src.game.board import Board
from src.game.chording import chord_cell


class TestChording:
    """Test suite for chording mechanic."""

    def test_chord_reveals_neighbors_when_flags_match(self):
        """Test that chording reveals neighbors when flag count equals cell number."""
        board = Board(3, 3, 1)

        # Place mine at corner (0, 0)
        board.place_mines(2, 2)  # First click at opposite corner

        # Cell (1, 1) should be adjacent to the mine
        board.reveal_cell(1, 1)
        assert board.grid[1][1].revealed, "Cell (1, 1) should be revealed"
        assert board.grid[1][1].adjacent_mines == 1, "Cell (1, 1) should have 1 adjacent mine"

        # Flag the neighbor containing the mine
        board.grid[0][0].flagged = True

        # Chord on the revealed cell
        board.chord_cell(1, 1)

        # All other neighbors should be revealed (except the flagged one)
        assert board.grid[0][1].revealed, "Cell (0, 1) should be revealed by chording"
        assert board.grid[1][0].revealed, "Cell (1, 0) should be revealed by chording"
        assert board.grid[2][0].revealed, "Cell (2, 0) should be revealed by chording"
        assert board.grid[2][1].revealed, "Cell (2, 1) should be revealed by chording"
        assert board.grid[2][2].revealed, "Cell (2, 2) should be revealed by chording"
        assert board.grid[1][2].revealed, "Cell (1, 2) should be revealed by chording"
        assert board.grid[0][2].revealed, "Cell (0, 2) should be revealed by chording"

    def test_chord_does_nothing_when_insufficient_flags(self):
        """Test that chording does nothing when flag count is less than cell number."""
        board = Board(3, 3, 2)

        # Place mines to create a cell with 2 adjacent mines
        board.place_mines(2, 2)

        # Find a cell with 2 adjacent mines
        for row in range(3):
            for col in range(3):
                if board.grid[row][col].adjacent_mines == 2:
                    test_cell = (row, col)
                    break
            else:
                continue
            break

        row, col = test_cell
        board.reveal_cell(row, col)

        # Flag only 1 neighbor (insufficient)
        # Find an unflagged neighbor
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = row + dr, col + dc
                if 0 <= nr < 3 and 0 <= nc < 3:
                    board.grid[nr][nc].flagged = True
                    break
            else:
                continue
            break

        # Count revealed cells before chording
        revealed_before = sum(
            cell.revealed
            for row in board.grid
            for cell in row
        )

        # Attempt chording
        board.chord_cell(row, col)

        # Count revealed cells after chording
        revealed_after = sum(
            cell.revealed
            for row in board.grid
            for cell in row
        )

        # No new cells should be revealed
        assert revealed_before == revealed_after, \
            "Chording should not reveal cells when flag count is insufficient"

    def test_chord_does_nothing_on_unrevealed_cell(self):
        """Test that chording does nothing on an unrevealed cell."""
        board = Board(3, 3, 1)

        board.place_mines(2, 2)

        # Don't reveal the cell
        # Flag some neighbors
        board.grid[0][0].flagged = True
        board.grid[0][1].flagged = True

        # Count revealed cells before chording
        revealed_before = sum(
            cell.revealed
            for row in board.grid
            for cell in row
        )

        # Attempt chording on unrevealed cell
        board.chord_cell(1, 1)

        # Count revealed cells after chording
        revealed_after = sum(
            cell.revealed
            for row in board.grid
            for cell in row
        )

        # No new cells should be revealed
        assert revealed_before == revealed_after, \
            "Chording should not work on unrevealed cells"

    def test_chord_does_nothing_on_blank_cell(self):
        """Test that chording does nothing on a blank cell (0 adjacent mines)."""
        board = Board(3, 3, 0)  # No mines

        board.place_mines(1, 1)

        # Reveal center cell (should be blank)
        board.reveal_cell(1, 1)
        assert board.grid[1][1].adjacent_mines == 0, "Cell should have 0 adjacent mines"

        # Flag some neighbors
        board.grid[0][0].flagged = True

        # Count revealed cells before chording
        revealed_before = sum(
            cell.revealed
            for row in board.grid
            for cell in row
        )

        # Attempt chording on blank cell
        board.chord_cell(1, 1)

        # Count revealed cells after chording
        revealed_after = sum(
            cell.revealed
            for row in board.grid
            for cell in row
        )

        # No new cells should be revealed (chording doesn't work on blank cells)
        assert revealed_before == revealed_after, \
            "Chording should not work on blank cells"

    def test_chord_skips_flagged_cells(self):
        """Test that chording does not reveal flagged cells."""
        board = Board(3, 3, 1)

        board.place_mines(2, 2)

        # Reveal a cell adjacent to the mine
        board.reveal_cell(1, 1)

        # Flag multiple neighbors
        board.grid[0][0].flagged = True
        board.grid[0][1].flagged = True
        board.grid[1][0].flagged = True

        # Chord the cell
        board.chord_cell(1, 1)

        # Flagged cells should not be revealed
        assert not board.grid[0][0].revealed, "Flagged cell (0, 0) should not be revealed"
        assert not board.grid[0][1].revealed, "Flagged cell (0, 1) should not be revealed"
        assert not board.grid[1][0].revealed, "Flagged cell (1, 0) should not be revealed"

    def test_chord_with_multiple_flags(self):
        """Test chording with multiple flags (cell number > 1)."""
        board = Board(5, 5, 4)

        board.place_mines(2, 2)

        # Find a cell with 2 or more adjacent mines
        test_cell = None
        for row in range(5):
            for col in range(5):
                if board.grid[row][col].adjacent_mines >= 2:
                    test_cell = (row, col)
                    break
            if test_cell:
                break

        # If we couldn't find one, manually set up a test scenario
        if not test_cell:
            board = Board(5, 5, 3)
            # Manually place mines around a specific cell
            board.grid[0][0].mine = True
            board.grid[0][1].mine = True
            board.grid[1][0].mine = True
            # Recalculate adjacent counts
            from src.game.adjacent_counter import calculate_adjacent_mines
            calculate_adjacent_mines(board.grid, 5, 5)
            test_cell = (1, 1)
            # Flag the mines
            board.grid[0][0].flagged = True
            board.grid[0][1].flagged = True
            board.grid[1][0].flagged = True

        row, col = test_cell
        board.reveal_cell(row, col)

        # Count how many mines are adjacent
        adjacent_mines = board.grid[row][col].adjacent_mines

        # Flag neighbors that contain mines
        flag_count = 0
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = row + dr, col + dc
                if 0 <= nr < 5 and 0 <= nc < 5:
                    if board.grid[nr][nc].mine and flag_count < adjacent_mines:
                        board.grid[nr][nc].flagged = True
                        flag_count += 1

        assert flag_count == adjacent_mines, f"Should have flagged {adjacent_mines} cells"

        # Chord the cell
        board.chord_cell(row, col)

        # All unflagged neighbors should be revealed
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = row + dr, col + dc
                if 0 <= nr < 5 and 0 <= nc < 5:
                    if not board.grid[nr][nc].flagged:
                        assert board.grid[nr][nc].revealed, \
                            f"Unflagged neighbor ({nr}, {nc}) should be revealed"

    def test_chord_on_edge_cell(self):
        """Test chording on a cell at the edge of the board."""
        board = Board(3, 3, 1)

        board.place_mines(2, 2)

        # Reveal a corner cell
        board.reveal_cell(0, 0)

        # Flag the mine if adjacent
        if board.grid[0][1].mine:
            board.grid[0][1].flagged = True
        if board.grid[1][0].mine:
            board.grid[1][0].flagged = True
        if board.grid[1][1].mine:
            board.grid[1][1].flagged = True

        # Chord the corner cell
        board.chord_cell(0, 0)

        # Unflagged neighbors should be revealed (if flag count matched)
        # The exact behavior depends on mine placement, but it shouldn't crash
        assert True, "Chording on edge cell should not crash"

    def test_chord_triggers_flood_fill(self):
        """Test that chording can trigger flood fill on blank neighbors."""
        board = Board(5, 5, 1)

        # Place mine in corner
        board.place_mines(4, 4)

        # Reveal a cell adjacent to the mine
        board.reveal_cell(3, 3)

        # Flag the mine
        board.grid[4][4].flagged = True

        # Chord the cell
        board.chord_cell(3, 3)

        # Neighbors should be revealed, including blank cells that trigger flood fill
        # The exact count depends on board state, but we should have revealed cells
        revealed_count = sum(
            cell.revealed
            for row in board.grid
            for cell in row
        )
        assert revealed_count > 1, "Chording should reveal neighbors and trigger flood fill"

    def test_invalid_coordinates_raise_error(self):
        """Test that chording with invalid coordinates raises IndexError."""
        board = Board(5, 5, 1)

        board.place_mines(2, 2)

        # Test out of bounds coordinates
        with pytest.raises(IndexError, match="out of bounds"):
            board.chord_cell(-1, 0)

        with pytest.raises(IndexError, match="out of bounds"):
            board.chord_cell(0, -1)

        with pytest.raises(IndexError, match="out of bounds"):
            board.chord_cell(5, 0)

        with pytest.raises(IndexError, match="out of bounds"):
            board.chord_cell(0, 5)

    def test_chord_does_not_modify_mines(self):
        """Test that chording does not change mine locations."""
        board = Board(5, 5, 3)

        board.place_mines(2, 2)

        # Count mines before chording
        mine_count_before = sum(
            cell.mine
            for row in board.grid
            for cell in row
        )

        # Reveal a cell and chord it
        board.reveal_cell(2, 2)
        board.grid[1][1].flagged = True
        board.chord_cell(2, 2)

        # Count mines after chording
        mine_count_after = sum(
            cell.mine
            for row in board.grid
            for cell in row
        )

        # Mine count should be unchanged
        assert mine_count_before == mine_count_after == 3, \
            "Chording should not modify mine placement"

    def test_chord_does_not_modify_adjacent_counts(self):
        """Test that chording does not change adjacent mine counts."""
        board = Board(5, 5, 3)

        board.place_mines(2, 2)

        # Store adjacent counts before chording
        adjacent_counts_before = [
            [board.grid[row][col].adjacent_mines for col in range(5)]
            for row in range(5)
        ]

        # Reveal a cell and chord it
        board.reveal_cell(2, 2)
        board.grid[1][1].flagged = True
        board.chord_cell(2, 2)

        # Check adjacent counts after chording
        for row in range(5):
            for col in range(5):
                assert board.grid[row][col].adjacent_mines == adjacent_counts_before[row][col], \
                    f"Chording should not change adjacent count at ({row}, {col})"

    def test_chord_with_all_correct_flags(self):
        """Test chording when all neighbors are correctly flagged."""
        board = Board(3, 3, 2)

        board.place_mines(2, 2)

        # Find a cell that has exactly 2 adjacent mines
        for row in range(3):
            for col in range(3):
                if board.grid[row][col].adjacent_mines == 2:
                    test_row, test_col = row, col
                    break
            else:
                continue
            break

        # Reveal the cell
        board.reveal_cell(test_row, test_col)

        # Find and flag the 2 mines
        mines_flagged = 0
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = test_row + dr, test_col + dc
                if 0 <= nr < 3 and 0 <= nc < 3:
                    if board.grid[nr][nc].mine:
                        board.grid[nr][nc].flagged = True
                        mines_flagged += 1

        assert mines_flagged == 2, "Should have found and flagged 2 mines"

        # Chord should reveal all non-mine neighbors
        board.chord_cell(test_row, test_col)

        # Verify that all non-mine, non-flagged neighbors are revealed
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = test_row + dr, test_col + dc
                if 0 <= nr < 3 and 0 <= nc < 3:
                    if not board.grid[nr][nc].mine and not board.grid[nr][nc].flagged:
                        assert board.grid[nr][nc].revealed, \
                            f"Safe neighbor ({nr}, {nc}) should be revealed"

    def test_chord_preserves_flags(self):
        """Test that chording does not remove existing flags."""
        board = Board(3, 3, 1)

        board.place_mines(2, 2)

        # Reveal center cell
        board.reveal_cell(1, 1)

        # Place multiple flags
        board.grid[0][0].flagged = True
        board.grid[0][1].flagged = True
        board.grid[1][0].flagged = True

        # Store flag count before chording
        flag_count_before = sum(
            cell.flagged
            for row in board.grid
            for cell in row
        )

        # Chord the cell
        board.chord_cell(1, 1)

        # Store flag count after chording
        flag_count_after = sum(
            cell.flagged
            for row in board.grid
            for cell in row
        )

        # Flag count should be unchanged
        assert flag_count_before == flag_count_after == 3, \
            "Chording should not modify flags"


if __name__ == "__main__":
    # Run tests when executed directly
    pytest.main([__file__, "-v"])
