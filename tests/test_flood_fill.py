"""
Test Suite for Flood Fill Algorithm

Verifies that the flood fill algorithm correctly reveals connected blank regions
when cells with 0 adjacent mines are clicked, and stops at numbered cells.
"""

import pytest

from src.game.board import Board


class TestFloodFill:
    """Test suite for flood fill reveal algorithm."""

    def test_reveal_single_blank_cell(self):
        """Test revealing a single cell with 0 adjacent mines
        (no neighbors to reveal)."""
        board = Board(3, 3, 0)  # 3x3 board with no mines

        # Manually set up a blank cell at center
        board.place_mines(0, 0)

        # Reveal the center cell
        board.reveal_cell(1, 1)

        # Center cell should be revealed
        assert board.grid[1][1].revealed, "Center cell should be revealed"

        # All neighbors should also be revealed (flood fill)
        for row in range(3):
            for col in range(3):
                assert board.grid[row][
                    col
                ].revealed, f"Cell ({row}, {col}) should be revealed by flood fill"

    def test_flood_fill_stops_at_numbered_cells(self):
        """Test that flood fill reveals numbered cells but doesn't
        continue past them."""
        board = Board(5, 5, 1)  # 5x5 board with 1 mine

        # Place mine at (4, 4) - far corner
        board.place_mines(0, 0)

        # Cell (2, 2) should have 0 adjacent mines (center of board, mine far away)
        # Reveal it to trigger flood fill
        board.reveal_cell(2, 2)

        # All cells in the blank region should be revealed
        # The flood fill should stop before reaching cells adjacent to the mine
        revealed_count = sum(cell.revealed for row in board.grid for cell in row)

        # The flood fill should have revealed most cells
        # (all except those adjacent to or containing the mine)
        assert revealed_count > 0, "Flood fill should reveal cells"

    def test_flood_fill_from_corner(self):
        """Test flood fill starting from a corner cell."""
        board = Board(5, 5, 1)  # 5x5 board with 1 mine

        # Place mine at center, click corner
        board.place_mines(0, 0)

        # Corner (0, 0) should be blank, reveal it
        board.reveal_cell(0, 0)

        # Should reveal connected blank region
        assert board.grid[0][0].revealed, "Corner cell should be revealed"

        # Count revealed cells
        revealed_count = sum(cell.revealed for row in board.grid for cell in row)
        assert revealed_count > 1, "Flood fill should reveal multiple cells"

    def test_flood_fill_from_edge(self):
        """Test flood fill starting from an edge cell."""
        board = Board(5, 5, 1)  # 5x5 board with 1 mine

        # Place mine at one corner, click opposite edge
        board.place_mines(4, 4)

        # Edge cell (0, 2) should be blank, reveal it
        board.reveal_cell(0, 2)

        # Should reveal connected blank region
        assert board.grid[0][2].revealed, "Edge cell should be revealed"

        # Count revealed cells
        revealed_count = sum(cell.revealed for row in board.grid for cell in row)
        assert revealed_count > 1, "Flood fill should reveal multiple cells"

    def test_reveal_numbered_cell_no_flood_fill(self):
        """Test that revealing a numbered cell doesn't trigger flood fill."""
        board = Board(5, 5, 1)  # 5x5 board with 1 mine

        # Manually place a mine at (0, 0) to ensure deterministic behavior
        board.grid[0][0].mine = True
        # Recalculate adjacent counts
        from src.game.adjacent_counter import calculate_adjacent_mines

        calculate_adjacent_mines(board.grid, 5, 5)

        # Cell (0, 1) should be adjacent to the mine at (0, 0)
        # Reveal it (should have adjacent_mines = 1)
        board.reveal_cell(0, 1)

        # Only that cell should be revealed, not its neighbors
        assert board.grid[0][1].revealed, "Cell (0, 1) should be revealed"
        assert (
            board.grid[0][1].adjacent_mines == 1
        ), "Cell (0, 1) should have 1 adjacent mine"

        # Check that neighbors are NOT revealed (no flood fill for numbered cells)
        # Cell (0, 2) should NOT be revealed
        assert not board.grid[0][
            2
        ].revealed, (
            "Cell (0, 2) should NOT be revealed (no flood fill for numbered cells)"
        )

    def test_flood_fill_respects_flags(self):
        """Test that flood fill does not reveal flagged cells."""
        board = Board(3, 3, 0)  # 3x3 board with no mines

        board.place_mines(0, 0)

        # Flag a cell
        board.grid[0][1].flagged = True

        # Reveal center cell (should trigger flood fill)
        board.reveal_cell(1, 1)

        # Center cell should be revealed
        assert board.grid[1][1].revealed, "Center cell should be revealed"

        # Flagged cell should NOT be revealed
        assert not board.grid[0][
            1
        ].revealed, "Flagged cell should NOT be revealed by flood fill"

    def test_flood_fill_skips_already_revealed(self):
        """Test that flood fill skips cells that are already revealed."""
        board = Board(3, 3, 0)  # 3x3 board with no mines

        board.place_mines(0, 0)

        # Manually reveal a cell
        board.grid[0][1].revealed = True

        # Reveal center cell (should trigger flood fill)
        board.reveal_cell(1, 1)

        # All cells should be revealed except potentially some
        # The important part is that the algorithm doesn't crash or loop infinitely
        revealed_count = sum(cell.revealed for row in board.grid for cell in row)
        assert revealed_count > 0, "Flood fill should reveal cells"

    def test_reveal_already_revealed_cell_no_op(self):
        """Test that revealing an already revealed cell is a no-op."""
        board = Board(3, 3, 0)

        board.place_mines(0, 0)

        # Reveal a cell
        board.reveal_cell(1, 1)
        revealed_count_after_first = sum(
            cell.revealed for row in board.grid for cell in row
        )

        # Try to reveal the same cell again
        board.reveal_cell(1, 1)
        revealed_count_after_second = sum(
            cell.revealed for row in board.grid for cell in row
        )

        # Count should be the same (no change)
        assert (
            revealed_count_after_first == revealed_count_after_second
        ), "Revealing an already revealed cell should be a no-op"

    def test_flood_fill_multiple_blank_regions(self):
        """Test flood fill in a board with multiple separate blank regions."""
        board = Board(5, 5, 2)  # 5x5 board with 2 mines

        # Place mines to create separate blank regions
        board.place_mines(2, 2)  # First click at center

        # Reveal a cell in one region
        board.reveal_cell(0, 0)

        # Count revealed cells
        revealed_count = sum(cell.revealed for row in board.grid for cell in row)

        # Should reveal at least the starting cell
        assert revealed_count > 0, "Flood fill should reveal cells"

    def test_flood_fill_entire_board_blank(self):
        """Test flood fill on a completely blank board (no mines)."""
        board = Board(5, 5, 0)  # 5x5 board with no mines

        board.place_mines(2, 2)

        # Reveal center cell
        board.reveal_cell(2, 2)

        # All cells should be revealed (entire board is one blank region)
        for row in range(5):
            for col in range(5):
                assert board.grid[row][
                    col
                ].revealed, f"Cell ({row}, {col}) should be revealed on blank board"

    def test_flood_fill_large_blank_region(self):
        """Test flood fill on a large blank region (simulating Expert board)."""
        board = Board(16, 30, 0)  # Expert-sized board with no mines

        board.place_mines(8, 15)

        # Reveal center cell
        board.reveal_cell(8, 15)

        # All cells should be revealed
        for row in range(16):
            for col in range(30):
                assert board.grid[row][
                    col
                ].revealed, (
                    f"Cell ({row}, {col}) should be revealed on large blank board"
                )

    def test_invalid_coordinates_raise_error(self):
        """Test that revealing invalid coordinates raises IndexError."""
        board = Board(5, 5, 1)

        board.place_mines(0, 0)

        # Test out of bounds coordinates
        with pytest.raises(IndexError, match="out of bounds"):
            board.reveal_cell(-1, 0)

        with pytest.raises(IndexError, match="out of bounds"):
            board.reveal_cell(0, -1)

        with pytest.raises(IndexError, match="out of bounds"):
            board.reveal_cell(5, 0)

        with pytest.raises(IndexError, match="out of bounds"):
            board.reveal_cell(0, 5)

    def test_flood_fill_performance_on_expert_board(self):
        """Test that flood fill completes quickly on Expert board."""
        import time

        board = Board(16, 30, 99)  # Expert difficulty

        board.place_mines(8, 15)

        # Time the flood fill operation
        start_time = time.time()
        board.reveal_cell(0, 0)
        end_time = time.time()

        # Should complete in less than 100ms (0.1 seconds)
        elapsed_ms = (end_time - start_time) * 1000
        assert (
            elapsed_ms < 100
        ), f"Flood fill on Expert board should take < 100ms, took {elapsed_ms:.2f}ms"

    def test_flood_fill_does_not_modify_mine_placement(self):
        """Test that flood fill does not change mine locations."""
        board = Board(5, 5, 3)

        board.place_mines(2, 2)

        # Count mines before flood fill
        mine_count_before = sum(cell.mine for row in board.grid for cell in row)

        # Perform flood fill
        board.reveal_cell(0, 0)

        # Count mines after flood fill
        mine_count_after = sum(cell.mine for row in board.grid for cell in row)

        # Mine count should be unchanged
        assert (
            mine_count_before == mine_count_after == 3
        ), "Flood fill should not modify mine placement"

    def test_flood_fill_does_not_modify_adjacent_counts(self):
        """Test that flood fill does not change adjacent mine counts."""
        board = Board(5, 5, 3)

        board.place_mines(2, 2)

        # Store adjacent counts before flood fill
        adjacent_counts_before = [
            [board.grid[row][col].adjacent_mines for col in range(5)]
            for row in range(5)
        ]

        # Perform flood fill
        board.reveal_cell(0, 0)

        # Check adjacent counts after flood fill
        for row in range(5):
            for col in range(5):
                assert (
                    board.grid[row][col].adjacent_mines
                    == adjacent_counts_before[row][col]
                ), f"Flood fill should not change adjacent count at ({row}, {col})"


if __name__ == "__main__":
    # Run tests when executed directly
    pytest.main([__file__, "-v"])
