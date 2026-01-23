"""
Test Suite for Win/Loss Detection

Verifies that the game correctly detects when the player has won (all non-mine
cells revealed) or lost (mine clicked and revealed).
"""

import pytest
from src.game.board import Board
from src.models.game_state import GameState


class TestWinDetection:
    """Test suite for win detection logic."""

    def test_win_when_all_safe_cells_revealed(self):
        """Test that game is won when all non-mine cells are revealed."""
        board = Board(3, 3, 2)  # 9 cells, 2 mines = 7 safe cells

        # Place mines at corners to isolate them
        board.place_mines(1, 1)

        # Find and reveal all non-mine cells
        revealed_count = 0
        for row in range(3):
            for col in range(3):
                if not board.grid[row][col].mine:
                    board.grid[row][col].revealed = True
                    revealed_count += 1

        assert revealed_count == 7, "Should have revealed 7 safe cells"

        # Check that game is won
        assert board.is_won(), "Game should be won when all safe cells are revealed"
        assert board.game_state == GameState.PLAYING, "State should be PLAYING until updated"

        # Update game state
        board.update_game_state()

        # Check that game state is now WON
        assert board.game_state == GameState.WON, "Game state should be WON"

    def test_not_won_when_mine_cells_still_hidden(self):
        """Test that game is not won when some non-mine cells remain hidden."""
        board = Board(3, 3, 1)  # 9 cells, 1 mine = 8 safe cells

        board.place_mines(1, 1)

        # Reveal only some safe cells
        revealed_count = 0
        for row in range(3):
            for col in range(3):
                if not board.grid[row][col].mine and revealed_count < 5:
                    board.grid[row][col].revealed = True
                    revealed_count += 1

        # Check that game is not won
        assert not board.is_won(), "Game should not be won when some safe cells are hidden"
        board.update_game_state()
        assert board.game_state == GameState.PLAYING, "Game state should remain PLAYING"

    def test_win_on_beginner_board(self):
        """Test win detection on Beginner board (9x9, 10 mines)."""
        board = Board(9, 9, 10)  # 81 cells, 10 mines = 71 safe cells

        board.place_mines(4, 4)

        # Reveal all safe cells
        for row in range(9):
            for col in range(9):
                if not board.grid[row][col].mine:
                    board.grid[row][col].revealed = True

        # Check that game is won
        assert board.is_won(), "Game should be won on Beginner board"
        board.update_game_state()
        assert board.game_state == GameState.WON, "Game state should be WON"

    def test_win_on_intermediate_board(self):
        """Test win detection on Intermediate board (16x16, 40 mines)."""
        board = Board(16, 16, 40)  # 256 cells, 40 mines = 216 safe cells

        board.place_mines(8, 8)

        # Reveal all safe cells
        for row in range(16):
            for col in range(16):
                if not board.grid[row][col].mine:
                    board.grid[row][col].revealed = True

        # Check that game is won
        assert board.is_won(), "Game should be won on Intermediate board"
        board.update_game_state()
        assert board.game_state == GameState.WON, "Game state should be WON"

    def test_win_on_expert_board(self):
        """Test win detection on Expert board (16x30, 99 mines)."""
        board = Board(16, 30, 99)  # 480 cells, 99 mines = 381 safe cells

        board.place_mines(8, 15)

        # Reveal all safe cells
        for row in range(16):
            for col in range(30):
                if not board.grid[row][col].mine:
                    board.grid[row][col].revealed = True

        # Check that game is won
        assert board.is_won(), "Game should be won on Expert board"
        board_game_state = board.game_state
        board.update_game_state()
        assert board.game_state == GameState.WON, "Game state should be WON"

    def test_win_detection_does_not_count_mine_cells(self):
        """Test that win detection only counts non-mine cells."""
        board = Board(3, 3, 3)

        board.place_mines(1, 1)

        # Reveal all cells including mines (shouldn't happen in real game)
        for row in range(3):
            for col in range(3):
                board.grid[row][col].revealed = True

        # All cells are revealed, but game should not be won because
        # we're checking revealed_count against safe_cells count
        assert board.is_won(), "Game should be won when all safe cells are revealed"

    def test_win_with_no_mines(self):
        """Test win detection on board with no mines."""
        board = Board(3, 3, 0)  # 9 cells, 0 mines = 9 safe cells

        board.place_mines(1, 1)

        # Reveal all cells
        for row in range(3):
            for col in range(3):
                board.grid[row][col].revealed = True

        # Check that game is won
        assert board.is_won(), "Game should be won when all cells are revealed on mine-free board"
        board.update_game_state()
        assert board.game_state == GameState.WON, "Game state should be WON"

    def test_win_flagged_cells_do_not_matter(self):
        """Test that flagged cells don't affect win detection."""
        board = Board(3, 3, 2)

        board.place_mines(1, 1)

        # Reveal all safe cells
        for row in range(3):
            for col in range(3):
                if not board.grid[row][col].mine:
                    board.grid[row][col].revealed = True

        # Add some flags (shouldn't affect win detection)
        board.grid[0][0].flagged = True
        board.grid[0][1].flagged = True

        # Check that game is won
        assert board.is_won(), "Flags should not affect win detection"


class TestLossDetection:
    """Test suite for loss detection logic."""

    def test_loss_when_mine_revealed(self):
        """Test that game is lost when a mine is revealed."""
        board = Board(3, 3, 1)

        board.place_mines(1, 1)

        # Find a mine and reveal it
        for row in range(3):
            for col in range(3):
                if board.grid[row][col].mine:
                    board.grid[row][col].revealed = True
                    break
            else:
                continue
            break

        # Check that game is lost
        assert board.is_lost(), "Game should be lost when a mine is revealed"
        assert board.game_state == GameState.PLAYING, "State should be PLAYING until updated"

        # Update game state
        board.update_game_state()

        # Check that game state is now LOST
        assert board.game_state == GameState.LOST, "Game state should be LOST"

    def test_not_lost_when_mines_still_hidden(self):
        """Test that game is not lost when all mines are still hidden."""
        board = Board(3, 3, 3)

        board.place_mines(1, 1)

        # Reveal some non-mine cells
        revealed_count = 0
        for row in range(3):
            for col in range(3):
                if not board.grid[row][col].mine and revealed_count < 3:
                    board.grid[row][col].revealed = True
                    revealed_count += 1

        # Check that game is not lost
        assert not board.is_lost(), "Game should not be lost when no mines are revealed"
        board.update_game_state()
        assert board.game_state == GameState.PLAYING, "Game state should remain PLAYING"

    def test_loss_on_first_mine_revealed(self):
        """Test that loss is detected as soon as any mine is revealed."""
        board = Board(5, 5, 5)

        board.place_mines(2, 2)

        # Reveal only one mine
        first_mine_revealed = False
        for row in range(5):
            for col in range(5):
                if board.grid[row][col].mine and not first_mine_revealed:
                    board.grid[row][col].revealed = True
                    first_mine_revealed = True
                    break
            if first_mine_revealed:
                break

        # Check that game is lost
        assert board.is_lost(), "Game should be lost as soon as any mine is revealed"

    def test_loss_with_multiple_mines_revealed(self):
        """Test loss detection when multiple mines are revealed."""
        board = Board(3, 3, 3)

        board.place_mines(1, 1)

        # Reveal all mines
        for row in range(3):
            for col in range(3):
                if board.grid[row][col].mine:
                    board.grid[row][col].revealed = True

        # Check that game is lost
        assert board.is_lost(), "Game should be lost when multiple mines are revealed"

    def test_flagged_mines_do_not_trigger_loss(self):
        """Test that flagging a mine does not trigger loss."""
        board = Board(3, 3, 2)

        board.place_mines(1, 1)

        # Flag all mines (but don't reveal them)
        for row in range(3):
            for col in range(3):
                if board.grid[row][col].mine:
                    board.grid[row][col].flagged = True

        # Check that game is not lost
        assert not board.is_lost(), "Flagged mines should not trigger loss"
        board.update_game_state()
        assert board.game_state == GameState.PLAYING, "Game state should remain PLAYING"


class TestGameStateTransitions:
    """Test suite for game state transitions."""

    def test_state_transitions_from_playing_to_won(self):
        """Test state transition from PLAYING to WON."""
        board = Board(3, 3, 1)

        board.place_mines(1, 1)
        assert board.game_state == GameState.PLAYING, "Initial state should be PLAYING"

        # Reveal all safe cells
        for row in range(3):
            for col in range(3):
                if not board.grid[row][col].mine:
                    board.grid[row][col].revealed = True

        # Update state
        board.update_game_state()
        assert board.game_state == GameState.WON, "State should transition to WON"

    def test_state_transitions_from_playing_to_lost(self):
        """Test state transition from PLAYING to LOST."""
        board = Board(3, 3, 1)

        board.place_mines(1, 1)
        assert board.game_state == GameState.PLAYING, "Initial state should be PLAYING"

        # Reveal a mine
        for row in range(3):
            for col in range(3):
                if board.grid[row][col].mine:
                    board.grid[row][col].revealed = True
                    break
            else:
                continue
            break

        # Update state
        board.update_game_state()
        assert board.game_state == GameState.LOST, "State should transition to LOST"

    def test_state_does_not_transition_from_won_to_playing(self):
        """Test that WON state doesn't transition back to PLAYING."""
        board = Board(3, 3, 1)

        board.place_mines(1, 1)

        # Win the game
        for row in range(3):
            for col in range(3):
                if not board.grid[row][col].mine:
                    board.grid[row][col].revealed = True

        board.update_game_state()
        assert board.game_state == GameState.WON, "State should be WON"

        # Try to update again (should stay WON)
        board.update_game_state()
        assert board.game_state == GameState.WON, "State should remain WON"

    def test_state_does_not_transition_from_lost_to_playing(self):
        """Test that LOST state doesn't transition back to PLAYING."""
        board = Board(3, 3, 1)

        board.place_mines(1, 1)

        # Lose the game
        for row in range(3):
            for col in range(3):
                if board.grid[row][col].mine:
                    board.grid[row][col].revealed = True
                    break
            else:
                continue
            break

        board.update_game_state()
        assert board.game_state == GameState.LOST, "State should be LOST"

        # Reveal all safe cells (should still be LOST)
        for row in range(3):
            for col in range(3):
                if not board.grid[row][col].mine:
                    board.grid[row][col].revealed = True

        # Try to update again (should stay LOST)
        board.update_game_state()
        assert board.game_state == GameState.LOST, "State should remain LOST"

    def test_loss_check_takes_priority_over_win_check(self):
        """Test that loss is detected even if all safe cells are also revealed."""
        board = Board(3, 3, 1)

        board.place_mines(1, 1)

        # Reveal all cells (including mines)
        for row in range(3):
            for col in range(3):
                board.grid[row][col].revealed = True

        # Update state - should be LOST (loss takes priority)
        board.update_game_state()
        assert board.game_state == GameState.LOST, "Loss should take priority over win"


class TestEdgeCases:
    """Test suite for edge cases."""

    def test_win_detection_on_empty_board(self):
        """Test win detection on board with no cells (edge case)."""
        # This is an edge case that shouldn't happen in practice
        # but we should handle it gracefully
        board = Board(1, 1, 0)

        board.place_mines(0, 0)

        # Reveal the only cell
        board.grid[0][0].revealed = True

        # Check that game is won
        assert board.is_won(), "Game should be won on 1x1 board with no mines"
        board.update_game_state()
        assert board.game_state == GameState.WON, "Game state should be WON"

    def test_initial_state_is_playing(self):
        """Test that initial game state is PLAYING."""
        board = Board(9, 9, 10)
        assert board.game_state == GameState.PLAYING, "Initial state should be PLAYING"

    def test_update_state_without_changes(self):
        """Test that updating state without board changes keeps state as PLAYING."""
        board = Board(3, 3, 1)

        board.place_mines(1, 1)

        # Update multiple times without changing board
        board.update_game_state()
        assert board.game_state == GameState.PLAYING

        board.update_game_state()
        assert board.game_state == GameState.PLAYING

        board.update_game_state()
        assert board.game_state == GameState.PLAYING

    def test_reveal_cell_does_not_automatically_update_state(self):
        """Test that revealing cells doesn't automatically update game state."""
        board = Board(3, 3, 1)

        board.place_mines(1, 1)

        # Reveal all safe cells using reveal_cell
        for row in range(3):
            for col in range(3):
                if not board.grid[row][col].mine:
                    board.reveal_cell(row, col)

        # State should still be PLAYING until update_game_state is called
        assert board.game_state == GameState.PLAYING, \
            "State should be PLAYING until update_game_state is called"

        # Now update the state
        board.update_game_state()
        assert board.game_state == GameState.WON, "State should be WON after update"


if __name__ == "__main__":
    # Run tests when executed directly
    pytest.main([__file__, "-v"])
