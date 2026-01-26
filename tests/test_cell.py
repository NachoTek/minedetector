"""
Test Suite for Cell Model

Verifies that the Cell dataclass correctly initializes and maintains
cell state including mine placement, reveal status, flag status, and
adjacent mine count.
"""

import pytest

from src.models.cell import Cell


class TestCellInitialization:
    """Test suite for Cell initialization and default values."""

    def test_default_values(self):
        """Test that Cell initializes with correct default values."""
        cell = Cell()

        assert cell.mine is False, "Default mine should be False"
        assert cell.revealed is False, "Default revealed should be False"
        assert cell.flagged is False, "Default flagged should be False"
        assert cell.adjacent_mines == 0, "Default adjacent_mines should be 0"

    def test_custom_initialization_all_parameters(self):
        """Test Cell initialization with all custom parameters."""
        cell = Cell(mine=True, revealed=True, flagged=True, adjacent_mines=5)

        assert cell.mine is True, "Custom mine should be True"
        assert cell.revealed is True, "Custom revealed should be True"
        assert cell.flagged is True, "Custom flagged should be True"
        assert cell.adjacent_mines == 5, "Custom adjacent_mines should be 5"

    def test_partial_initialization_mine_only(self):
        """Test Cell initialization with only mine parameter."""
        cell = Cell(mine=True)

        assert cell.mine is True, "Custom mine should be True"
        assert cell.revealed is False, "Default revealed should be False"
        assert cell.flagged is False, "Default flagged should be False"
        assert cell.adjacent_mines == 0, "Default adjacent_mines should be 0"

    def test_partial_initialization_revealed_only(self):
        """Test Cell initialization with only revealed parameter."""
        cell = Cell(revealed=True)

        assert cell.mine is False, "Default mine should be False"
        assert cell.revealed is True, "Custom revealed should be True"
        assert cell.flagged is False, "Default flagged should be False"
        assert cell.adjacent_mines == 0, "Default adjacent_mines should be 0"

    def test_partial_initialization_flagged_only(self):
        """Test Cell initialization with only flagged parameter."""
        cell = Cell(flagged=True)

        assert cell.mine is False, "Default mine should be False"
        assert cell.revealed is False, "Default revealed should be False"
        assert cell.flagged is True, "Custom flagged should be True"
        assert cell.adjacent_mines == 0, "Default adjacent_mines should be 0"

    def test_partial_initialization_adjacent_mines_only(self):
        """Test Cell initialization with only adjacent_mines parameter."""
        cell = Cell(adjacent_mines=3)

        assert cell.mine is False, "Default mine should be False"
        assert cell.revealed is False, "Default revealed should be False"
        assert cell.flagged is False, "Default flagged should be False"
        assert cell.adjacent_mines == 3, "Custom adjacent_mines should be 3"

    def test_multiple_custom_parameters(self):
        """Test Cell initialization with multiple custom parameters."""
        cell = Cell(mine=True, adjacent_mines=2)

        assert cell.mine is True, "Custom mine should be True"
        assert cell.revealed is False, "Default revealed should be False"
        assert cell.flagged is False, "Default flagged should be False"
        assert cell.adjacent_mines == 2, "Custom adjacent_mines should be 2"


class TestCellAttributes:
    """Test suite for Cell attribute assignment and mutation."""

    def test_mine_attribute_mutation(self):
        """Test that mine attribute can be mutated."""
        cell = Cell()
        assert cell.mine is False, "Initial mine should be False"

        cell.mine = True
        assert cell.mine is True, "Mine should be True after mutation"

        cell.mine = False
        assert cell.mine is False, "Mine should be False after second mutation"

    def test_revealed_attribute_mutation(self):
        """Test that revealed attribute can be mutated."""
        cell = Cell()
        assert cell.revealed is False, "Initial revealed should be False"

        cell.revealed = True
        assert cell.revealed is True, "Revealed should be True after mutation"

        cell.revealed = False
        assert cell.revealed is False, "Revealed should be False after second mutation"

    def test_flagged_attribute_mutation(self):
        """Test that flagged attribute can be mutated."""
        cell = Cell()
        assert cell.flagged is False, "Initial flagged should be False"

        cell.flagged = True
        assert cell.flagged is True, "Flagged should be True after mutation"

        cell.flagged = False
        assert cell.flagged is False, "Flagged should be False after second mutation"

    def test_adjacent_mines_attribute_mutation(self):
        """Test that adjacent_mines attribute can be mutated."""
        cell = Cell()
        assert cell.adjacent_mines == 0, "Initial adjacent_mines should be 0"

        cell.adjacent_mines = 5
        assert cell.adjacent_mines == 5, "Adjacent mines should be 5 after mutation"

        cell.adjacent_mines = 0
        assert (
            cell.adjacent_mines == 0
        ), "Adjacent mines should be 0 after second mutation"

    def test_all_attributes_independent(self):
        """Test that all attributes are independent and don't affect each other."""
        cell = Cell()

        # Set each attribute to different values
        cell.mine = True
        cell.revealed = True
        cell.flagged = True
        cell.adjacent_mines = 8

        # Verify all are set correctly
        assert cell.mine is True, "Mine should be True"
        assert cell.revealed is True, "Revealed should be True"
        assert cell.flagged is True, "Flagged should be True"
        assert cell.adjacent_mines == 8, "Adjacent mines should be 8"

        # Change one and verify others are unaffected
        cell.mine = False
        assert cell.mine is False, "Mine should be False"
        assert cell.revealed is True, "Revealed should still be True"
        assert cell.flagged is True, "Flagged should still be True"
        assert cell.adjacent_mines == 8, "Adjacent mines should still be 8"


class TestAdjacentMinesRange:
    """Test suite for adjacent_mines valid range (0-8)."""

    def test_adjacent_mines_zero(self):
        """Test that adjacent_mines can be 0 (no adjacent mines)."""
        cell = Cell(adjacent_mines=0)
        assert cell.adjacent_mines == 0, "Adjacent mines can be 0"

    def test_adjacent_mines_one(self):
        """Test that adjacent_mines can be 1."""
        cell = Cell(adjacent_mines=1)
        assert cell.adjacent_mines == 1, "Adjacent mines can be 1"

    def test_adjacent_mines_eight(self):
        """Test that adjacent_mines can be 8 (maximum)."""
        cell = Cell(adjacent_mines=8)
        assert cell.adjacent_mines == 8, "Adjacent mines can be 8"

    def test_adjacent_mines_all_valid_values(self):
        """Test that adjacent_mines can be any value from 0 to 8."""
        for i in range(9):  # 0 through 8
            cell = Cell(adjacent_mines=i)
            assert cell.adjacent_mines == i, f"Adjacent mines should be {i}"

    def test_adjacent_mines_boundary_values(self):
        """Test adjacent_mines at boundary values."""
        # Test lower boundary
        cell_min = Cell(adjacent_mines=0)
        assert cell_min.adjacent_mines == 0, "Lower boundary should be 0"

        # Test upper boundary
        cell_max = Cell(adjacent_mines=8)
        assert cell_max.adjacent_mines == 8, "Upper boundary should be 8"

        # Test midpoint
        cell_mid = Cell(adjacent_mines=4)
        assert cell_mid.adjacent_mines == 4, "Midpoint should be 4"


class TestCellStates:
    """Test suite for common cell state combinations."""

    def test_unrevealed_unflagged_safe_cell(self):
        """Test state of unrevealed, unflagged safe cell (default)."""
        cell = Cell()
        assert cell.mine is False, "Safe cell should not be a mine"
        assert cell.revealed is False, "Cell should not be revealed"
        assert cell.flagged is False, "Cell should not be flagged"
        assert cell.adjacent_mines == 0, "Default adjacent count should be 0"

    def test_unrevealed_flagged_safe_cell(self):
        """Test state of unrevealed, flagged safe cell."""
        cell = Cell(flagged=True, adjacent_mines=2)
        assert cell.mine is False, "Safe cell should not be a mine"
        assert cell.revealed is False, "Cell should not be revealed"
        assert cell.flagged is True, "Cell should be flagged"
        assert cell.adjacent_mines == 2, "Adjacent count should be 2"

    def test_revealed_safe_cell_numbered(self):
        """Test state of revealed safe cell with number."""
        cell = Cell(revealed=True, adjacent_mines=3)
        assert cell.mine is False, "Safe cell should not be a mine"
        assert cell.revealed is True, "Cell should be revealed"
        assert cell.adjacent_mines == 3, "Adjacent count should be 3"

    def test_revealed_safe_cell_blank(self):
        """Test state of revealed safe cell with no adjacent mines (blank)."""
        cell = Cell(revealed=True, adjacent_mines=0)
        assert cell.mine is False, "Safe cell should not be a mine"
        assert cell.revealed is True, "Cell should be revealed"
        assert cell.adjacent_mines == 0, "Adjacent count should be 0 (blank)"

    def test_unrevealed_mine(self):
        """Test state of unrevealed mine."""
        cell = Cell(mine=True)
        assert cell.mine is True, "Cell should be a mine"
        assert cell.revealed is False, "Mine should not be revealed"
        assert cell.flagged is False, "Mine should not be flagged by default"

    def test_unrevealed_flagged_mine(self):
        """Test state of unrevealed, flagged mine (correctly flagged)."""
        cell = Cell(mine=True, flagged=True)
        assert cell.mine is True, "Cell should be a mine"
        assert cell.revealed is False, "Mine should not be revealed"
        assert cell.flagged is True, "Mine should be flagged"

    def test_revealed_mine(self):
        """Test state of revealed mine (game over)."""
        cell = Cell(mine=True, revealed=True)
        assert cell.mine is True, "Cell should be a mine"
        assert cell.revealed is True, "Mine should be revealed (game over)"

    def test_revealed_flagged_cell(self):
        """Test state of revealed and flagged cell (unusual but possible)."""
        cell = Cell(revealed=True, flagged=True, adjacent_mines=1)
        assert cell.revealed is True, "Cell should be revealed"
        assert cell.flagged is True, "Cell should be flagged"
        assert cell.adjacent_mines == 1, "Adjacent count should be 1"


class TestCellEquality:
    """Test suite for Cell equality and comparison."""

    def test_identical_cells_equal(self):
        """Test that two cells with identical attributes are equal."""
        cell1 = Cell(mine=True, revealed=True, adjacent_mines=3)
        cell2 = Cell(mine=True, revealed=True, adjacent_mines=3)

        assert cell1 == cell2, "Cells with identical attributes should be equal"

    def test_default_cells_equal(self):
        """Test that two default cells are equal."""
        cell1 = Cell()
        cell2 = Cell()

        assert cell1 == cell2, "Two default cells should be equal"

    def test_different_cells_not_equal(self):
        """Test that cells with different attributes are not equal."""
        cell1 = Cell(mine=True)
        cell2 = Cell(mine=False)

        assert cell1 != cell2, "Cells with different mine values should not be equal"

    def test_partial_difference_not_equal(self):
        """Test that cells differing in one attribute are not equal."""
        cell1 = Cell(revealed=True, adjacent_mines=3)
        cell2 = Cell(revealed=True, adjacent_mines=4)

        assert cell1 != cell2, "Cells with different adjacent_mines should not be equal"


class TestCellDataclassBehavior:
    """Test suite for dataclass-specific behavior."""

    def test_cell_repr(self):
        """Test that Cell has a readable string representation."""
        cell = Cell(mine=True, adjacent_mines=3)
        repr_str = repr(cell)

        assert "Cell" in repr_str, "Representation should contain class name"
        assert "mine=True" in repr_str, "Representation should show mine attribute"
        assert (
            "adjacent_mines=3" in repr_str
        ), "Representation should show adjacent_mines"

    def test_cell_with_all_attributes_repr(self):
        """Test representation with all attributes set."""
        cell = Cell(mine=True, revealed=True, flagged=True, adjacent_mines=5)
        repr_str = repr(cell)

        assert "mine=True" in repr_str
        assert "revealed=True" in repr_str
        assert "flagged=True" in repr_str
        assert "adjacent_mines=5" in repr_str

    def test_multiple_cells_independent(self):
        """Test that multiple Cell instances are independent."""
        cell1 = Cell(mine=True)
        cell2 = Cell()

        assert cell1.mine is True, "cell1 mine should be True"
        assert cell2.mine is False, "cell2 mine should be False"

        # Modify cell1
        cell1.revealed = True

        # cell2 should be unaffected
        assert cell1.revealed is True, "cell1 revealed should be True"
        assert cell2.revealed is False, "cell2 revealed should still be False"


if __name__ == "__main__":
    # Run tests when executed directly
    pytest.main([__file__, "-v"])
