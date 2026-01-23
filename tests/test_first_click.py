"""
Test Suite for First-Click Safety

Verifies that the mine placement algorithm guarantees the first-click cell
and all 8 of its neighbors are mine-free across multiple random generations.
"""

import pytest
from src.game.board import Board
from src.game.mine_placement import place_mines


class TestFirstClickSafety:
    """Test suite for first-click safety in mine placement."""

    def test_first_click_cell_never_mine_center(self):
        """Test that the first-click cell is never a mine (center of board)."""
        # Test 100 random generations to ensure consistency
        for _ in range(100):
            board = Board(9, 9, 10)
            first_row, first_col = 4, 4  # Center of 9x9 board

            board.place_mines(first_row, first_col)

            # Verify first-click cell is not a mine
            assert not board.grid[first_row][first_col].mine, \
                f"First-click cell ({first_row}, {first_col}) should never be a mine"

    def test_first_click_neighbors_never_mine_center(self):
        """Test that all neighbors of first-click cell are never mines (center)."""
        for _ in range(100):
            board = Board(9, 9, 10)
            first_row, first_col = 4, 4

            board.place_mines(first_row, first_col)

            # Check all 8 neighbors
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    row = first_row + dr
                    col = first_col + dc
                    assert not board.grid[row][col].mine, \
                        f"Neighbor ({row}, {col}) of first-click should never be a mine"

    def test_first_click_cell_never_mine_corner(self):
        """Test that the first-click cell is never a mine (corner of board)."""
        for _ in range(100):
            board = Board(9, 9, 10)
            first_row, first_col = 0, 0  # Top-left corner

            board.place_mines(first_row, first_col)

            # Verify first-click cell is not a mine
            assert not board.grid[first_row][first_col].mine, \
                f"First-click cell at corner should never be a mine"

    def test_first_click_neighbors_never_mine_corner(self):
        """Test that all valid neighbors of first-click cell are never mines (corner)."""
        for _ in range(100):
            board = Board(9, 9, 10)
            first_row, first_col = 0, 0  # Top-left corner

            board.place_mines(first_row, first_col)

            # Check all valid neighbors (corner has only 3 neighbors)
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    row = first_row + dr
                    col = first_col + dc
                    if board.is_valid_coordinate(row, col):
                        assert not board.grid[row][col].mine, \
                            f"Neighbor ({row}, {col}) of corner first-click should never be a mine"

    def test_first_click_cell_never_mine_edge(self):
        """Test that the first-click cell is never a mine (edge of board)."""
        for _ in range(100):
            board = Board(9, 9, 10)
            first_row, first_col = 0, 4  # Top edge

            board.place_mines(first_row, first_col)

            # Verify first-click cell is not a mine
            assert not board.grid[first_row][first_col].mine, \
                f"First-click cell at edge should never be a mine"

    def test_correct_mine_count_placed(self):
        """Test that exactly the specified number of mines are placed."""
        for _ in range(50):
            board = Board(9, 9, 10)
            first_row, first_col = 4, 4

            board.place_mines(first_row, first_col)

            # Count total mines
            mine_count = sum(
                cell.mine
                for row in board.grid
                for cell in row
            )
            assert mine_count == board.mine_count, \
                f"Expected {board.mine_count} mines, but found {mine_count}"

    def test_intermediate_difficulty_first_click_safety(self):
        """Test first-click safety on Intermediate difficulty (16x16, 40 mines)."""
        for _ in range(100):
            board = Board(16, 16, 40)
            first_row, first_col = 8, 8  # Center

            board.place_mines(first_row, first_col)

            # Verify first-click cell and neighbors are safe
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    row = first_row + dr
                    col = first_col + dc
                    assert not board.grid[row][col].mine, \
                        f"Intermediate: Neighbor ({row}, {col}) should never be a mine"

            # Verify correct mine count
            mine_count = sum(
                cell.mine
                for row in board.grid
                for cell in row
            )
            assert mine_count == 40, \
                f"Intermediate: Expected 40 mines, but found {mine_count}"

    def test_expert_difficulty_first_click_safety(self):
        """Test first-click safety on Expert difficulty (16x30, 99 mines)."""
        for _ in range(100):
            board = Board(16, 30, 99)
            first_row, first_col = 8, 15  # Center

            board.place_mines(first_row, first_col)

            # Verify first-click cell and neighbors are safe
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    row = first_row + dr
                    col = first_col + dc
                    assert not board.grid[row][col].mine, \
                        f"Expert: Neighbor ({row}, {col}) should never be a mine"

            # Verify correct mine count
            mine_count = sum(
                cell.mine
                for row in board.grid
                for cell in row
            )
            assert mine_count == 99, \
                f"Expert: Expected 99 mines, but found {mine_count}"

    def test_invalid_first_click_coordinates(self):
        """Test that invalid first-click coordinates raise ValueError."""
        board = Board(9, 9, 10)

        # Test out of bounds coordinates
        with pytest.raises(ValueError, match="out of bounds"):
            board.place_mines(-1, 0)

        with pytest.raises(ValueError, match="out of bounds"):
            board.place_mines(0, -1)

        with pytest.raises(ValueError, match="out of bounds"):
            board.place_mines(9, 0)

        with pytest.raises(ValueError, match="out of bounds"):
            board.place_mines(0, 9)

    def test_too_many_mines_for_board(self):
        """Test that placing too many mines raises ValueError."""
        board = Board(3, 3, 9)  # 3x3 board with 9 mines

        # First-click protects 9 cells (entire board for 3x3 center click)
        # This should fail because there are no available cells
        with pytest.raises(ValueError, match="Cannot place"):
            board.place_mines(1, 1)

    def test_mines_only_placed_after_first_click(self):
        """Test that mines are placed AFTER first-click, not during initialization."""
        board = Board(9, 9, 10)

        # Before placing mines, no cells should have mines
        mine_count_before = sum(
            cell.mine
            for row in board.grid
            for cell in row
        )
        assert mine_count_before == 0, \
            "Board should have no mines before place_mines() is called"

        # After placing mines, there should be mines
        board.place_mines(4, 4)
        mine_count_after = sum(
            cell.mine
            for row in board.grid
            for cell in row
        )
        assert mine_count_after == 10, \
            "Board should have 10 mines after place_mines() is called"

    def test_multiple_first_clicks_different_positions(self):
        """Test first-click safety works for various positions on the board."""
        test_positions = [
            (0, 0), (0, 4), (0, 8),  # Top row: corners and center
            (4, 0), (4, 4), (4, 8),  # Middle row: left, center, right
            (8, 0), (8, 4), (8, 8),  # Bottom row: corners and center
        ]

        for first_row, first_col in test_positions:
            for _ in range(20):  # Test each position 20 times
                board = Board(9, 9, 10)
                board.place_mines(first_row, first_col)

                # Verify first-click cell is safe
                assert not board.grid[first_row][first_col].mine, \
                    f"Position ({first_row}, {first_col}): First-click should never be a mine"


if __name__ == "__main__":
    # Run tests when executed directly
    pytest.main([__file__, "-v"])
