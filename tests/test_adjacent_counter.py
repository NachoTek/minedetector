"""
Test Suite for Adjacent Mine Counter

Verifies that the adjacent mine counting algorithm correctly counts mines
in all 8 neighboring cells for interior, edge, and corner cells.
"""

import pytest
from src.game.board import Board


class TestAdjacentMineCounter:
    """Test suite for adjacent mine counting algorithm."""

    def test_cell_with_no_adjacent_mines(self):
        """Test that a cell with no adjacent mines has count of 0."""
        board = Board(5, 5, 0)  # No mines
        board.place_mines(2, 2)

        # All cells should have 0 adjacent mines
        for row in range(5):
            for col in range(5):
                assert board.grid[row][col].adjacent_mines == 0, \
                    f"Cell ({row}, {col}) should have 0 adjacent mines when board has no mines"

    def test_single_mine_center(self):
        """Test adjacent count for cells around a single mine at center."""
        board = Board(5, 5, 1)
        board.place_mines(0, 0)  # First click at corner, mine placed elsewhere

        # Find the mine
        mine_row, mine_col = None, None
        for row in range(5):
            for col in range(5):
                if board.grid[row][col].mine:
                    mine_row, mine_col = row, col
                    break
            if mine_row is not None:
                break

        # Verify that the 8 neighbors of the mine have count of 1
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                neighbor_row = mine_row + dr
                neighbor_col = mine_col + dc
                if board.is_valid_coordinate(neighbor_row, neighbor_col):
                    assert board.grid[neighbor_row][neighbor_col].adjacent_mines == 1, \
                        f"Cell ({neighbor_row}, {neighbor_col}) should have 1 adjacent mine"

    def test_corner_cell_adjacent_count(self):
        """Test that corner cells correctly count their 3 neighbors."""
        board = Board(3, 3, 3)

        # Manually place mines in all 3 neighbors of top-left corner (0,0)
        # Neighbors of (0,0) are: (0,1), (1,0), (1,1)
        board.grid[0][1].mine = True
        board.grid[1][0].mine = True
        board.grid[1][1].mine = True

        # Calculate adjacent counts
        from src.game import adjacent_counter
        adjacent_counter.calculate_adjacent_mines(board.grid, board.rows, board.cols)

        # Top-left corner should have count of 3
        assert board.grid[0][0].adjacent_mines == 3, \
            "Corner cell (0,0) should count all 3 neighbors"

    def test_edge_cell_adjacent_count(self):
        """Test that edge cells correctly count their 5 neighbors."""
        board = Board(3, 3, 5)

        # Manually place mines in all 5 neighbors of top-edge cell (0,1)
        # Neighbors of (0,1) are: (0,0), (0,2), (1,0), (1,1), (1,2)
        board.grid[0][0].mine = True
        board.grid[0][2].mine = True
        board.grid[1][0].mine = True
        board.grid[1][1].mine = True
        board.grid[1][2].mine = True

        # Calculate adjacent counts
        from src.game import adjacent_counter
        adjacent_counter.calculate_adjacent_mines(board.grid, board.rows, board.cols)

        # Top-edge cell should have count of 5
        assert board.grid[0][1].adjacent_mines == 5, \
            "Edge cell (0,1) should count all 5 neighbors"

    def test_interior_cell_adjacent_count(self):
        """Test that interior cells correctly count all 8 neighbors."""
        board = Board(3, 3, 8)

        # Manually place mines in all 8 neighbors of center cell (1,1)
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                board.grid[1 + dr][1 + dc].mine = True

        # Calculate adjacent counts
        from src.game import adjacent_counter
        adjacent_counter.calculate_adjacent_mines(board.grid, board.rows, board.cols)

        # Center cell should have count of 8
        assert board.grid[1][1].adjacent_mines == 8, \
            "Interior cell (1,1) should count all 8 neighbors"

    def test_multiple_mines_adjacent_count(self):
        """Test adjacent count with multiple mines nearby."""
        board = Board(5, 5, 4)

        # Manually place mines at specific locations
        board.grid[0][1].mine = True  # Neighbor of (0,0)
        board.grid[1][0].mine = True  # Neighbor of (0,0)
        board.grid[1][1].mine = True  # Neighbor of (0,0)
        board.grid[4][4].mine = True  # Far from (0,0)

        # Calculate adjacent counts
        from src.game import adjacent_counter
        adjacent_counter.calculate_adjacent_mines(board.grid, board.rows, board.cols)

        # Cell (0,0) should have count of 3 (3 adjacent mines)
        assert board.grid[0][0].adjacent_mines == 3, \
            "Cell (0,0) should have 3 adjacent mines"

        # Cell (4,4) should have count of 0 (no adjacent mines)
        assert board.grid[4][4].adjacent_mines == 0, \
            "Cell (4,4) should have 0 adjacent mines"

    def test_calculated_after_mine_placement(self):
        """Test that adjacent counts are calculated after mine placement."""
        board = Board(9, 9, 10)

        # Before mine placement, all counts should be 0
        for row in range(9):
            for col in range(9):
                assert board.grid[row][col].adjacent_mines == 0, \
                    f"Cell ({row}, {col}) should start with 0 adjacent mines"

        # Place mines (which also calculates adjacent counts)
        board.place_mines(4, 4)

        # After mine placement, some cells should have non-zero counts
        has_non_zero = any(
            board.grid[row][col].adjacent_mines > 0
            for row in range(9)
            for col in range(9)
        )
        assert has_non_zero, \
            "After mine placement, at least one cell should have adjacent_mines > 0"

    def test_mine_cell_has_adjacent_count(self):
        """Test that mine cells also have their adjacent mine count calculated."""
        board = Board(3, 3, 4)

        # Manually place mines in a pattern
        board.grid[0][0].mine = True
        board.grid[0][1].mine = True
        board.grid[1][0].mine = True
        board.grid[1][1].mine = True

        # Calculate adjacent counts
        from src.game import adjacent_counter
        adjacent_counter.calculate_adjacent_mines(board.grid, board.rows, board.cols)

        # Mine cells should still have their adjacent count calculated
        # Cell (0,0) is a mine but has 3 adjacent mines (0,1), (1,0), (1,1)
        assert board.grid[0][0].adjacent_mines == 3, \
            "Mine cells should also have their adjacent count calculated"

    def test_all_cells_calculated(self):
        """Test that all cells on the board get their adjacent count calculated."""
        board = Board(9, 9, 10)
        board.place_mines(4, 4)

        # Verify every cell has its adjacent_mines attribute set
        for row in range(9):
            for col in range(9):
                # adjacent_mines should always be non-negative
                assert board.grid[row][col].adjacent_mines >= 0, \
                    f"Cell ({row}, {col}) should have non-negative adjacent_mines count"
                # adjacent_mines should never exceed 8
                assert board.grid[row][col].adjacent_mines <= 8, \
                    f"Cell ({row}, {col}) should have adjacent_mines <= 8"


if __name__ == "__main__":
    # Run tests when executed directly
    pytest.main([__file__, "-v"])
