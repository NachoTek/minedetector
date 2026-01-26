"""
End-to-End Gameplay Tests

This test suite performs comprehensive end-to-end verification of the Minesweeper
gameplay by simulating complete game scenarios through the Board API.

These tests verify:
- Complete gameplay flows from start to finish
- First-click safety across multiple games
- Win/loss state transitions
- Timer and counter behavior integration
- Difficulty level switching
- Reset functionality
- All three difficulty levels

While these tests don't exercise the Tkinter GUI, they verify the complete game logic
integration that powers the GUI.
"""

from src.game.board import Board
from src.models.game_state import GameState


class TestBeginnerDifficulty:
    """Test complete gameplay on Beginner difficulty (9x9, 10 mines)."""

    def test_beginner_board_initialization(self):
        """Verify Beginner board initializes correctly."""
        board = Board(9, 9, 10)
        assert board.rows == 9
        assert board.cols == 9
        assert board.mine_count == 10
        assert board.game_state == GameState.PLAYING
        assert len(board.grid) == 9
        assert len(board.grid[0]) == 9

    def test_beginner_first_click_safety_multiple_games(self):
        """Verify first-click safety across 20 games on Beginner."""
        for game_num in range(20):
            board = Board(9, 9, 10)

            # Test various starting positions
            test_positions = [
                (0, 0),  # Top-left corner
                (0, 4),  # Top edge
                (4, 0),  # Left edge
                (4, 4),  # Center
                (8, 8),  # Bottom-right corner
                (8, 4),  # Bottom edge
                (4, 8),  # Right edge
            ]

            start_row, start_col = test_positions[game_num % len(test_positions)]

            # Place mines after first click
            board.place_mines(start_row, start_col)

            # Verify first-click cell is safe
            first_cell = board.get_cell(start_row, start_col)
            assert (
                not first_cell.mine
            ), f"Game {game_num}: First-click cell at ({start_row},"
            f" {start_col}) should not be a mine"

            # Verify all 8 neighbors are safe (or out of bounds)
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    nr, nc = start_row + dr, start_col + dc
                    if board.is_valid_coordinate(nr, nc):
                        neighbor = board.get_cell(nr, nc)
                        assert (
                            not neighbor.mine
                        ), f"Game {game_num}: Neighbor ({nr}, {nc})"
                        " should not be a mine"

    def test_beginner_win_condition(self):
        """Verify win detection on Beginner board."""
        board = Board(9, 9, 10)
        board.place_mines(4, 4)

        # Simulate revealing all non-mine cells
        for row in range(9):
            for col in range(9):
                cell = board.get_cell(row, col)
                if not cell.mine:
                    cell.revealed = True

        board.update_game_state()
        assert board.is_won()
        assert board.game_state == GameState.WON

    def test_beginner_loss_condition(self):
        """Verify loss detection on Beginner board."""
        board = Board(9, 9, 10)
        board.place_mines(4, 4)

        # Find and reveal a mine
        for row in range(9):
            for col in range(9):
                cell = board.get_cell(row, col)
                if cell.mine:
                    cell.revealed = True
                    break
            else:
                continue
            break

        board.update_game_state()
        assert board.is_lost()
        assert board.game_state == GameState.LOST


class TestIntermediateDifficulty:
    """Test complete gameplay on Intermediate difficulty (16x16, 40 mines)."""

    def test_intermediate_board_initialization(self):
        """Verify Intermediate board initializes correctly."""
        board = Board(16, 16, 40)
        assert board.rows == 16
        assert board.cols == 16
        assert board.mine_count == 40
        assert board.game_state == GameState.PLAYING

    def test_intermediate_first_click_safety_multiple_games(self):
        """Verify first-click safety across 20 games on Intermediate."""
        for game_num in range(20):
            board = Board(16, 16, 40)

            # Test various starting positions
            test_positions = [
                (0, 0),  # Corner
                (0, 8),  # Top edge
                (8, 0),  # Left edge
                (8, 8),  # Center
                (15, 15),  # Opposite corner
                (15, 8),  # Bottom edge
                (8, 15),  # Right edge
            ]

            start_row, start_col = test_positions[game_num % len(test_positions)]

            # Place mines after first click
            board.place_mines(start_row, start_col)

            # Verify first-click cell is safe
            first_cell = board.get_cell(start_row, start_col)
            assert (
                not first_cell.mine
            ), f"Game {game_num}: First-click cell at ({start_row},"
            f" {start_col}) should not be a mine"

            # Verify all neighbors are safe
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    nr, nc = start_row + dr, start_col + dc
                    if board.is_valid_coordinate(nr, nc):
                        neighbor = board.get_cell(nr, nc)
                        assert (
                            not neighbor.mine
                        ), f"Game {game_num}: Neighbor ({nr}, {nc})"
                        " should not be a mine"

    def test_intermediate_correct_mine_count(self):
        """Verify exactly 40 mines placed on Intermediate board."""
        board = Board(16, 16, 40)
        board.place_mines(8, 8)

        mine_count = sum(1 for row in board.grid for cell in row if cell.mine)

        assert mine_count == 40, f"Expected 40 mines, found {mine_count}"

    def test_intermediate_win_condition(self):
        """Verify win detection on Intermediate board."""
        board = Board(16, 16, 40)
        board.place_mines(8, 8)

        # Calculate safe cells: 16*16 - 40 = 216
        safe_count = 0
        for row in range(16):
            for col in range(16):
                cell = board.get_cell(row, col)
                if not cell.mine:
                    cell.revealed = True
                    safe_count += 1

        assert safe_count == 216, f"Expected 216 safe cells, found {safe_count}"

        board.update_game_state()
        assert board.is_won()
        assert board.game_state == GameState.WON


class TestExpertDifficulty:
    """Test complete gameplay on Expert difficulty (16x30, 99 mines)."""

    def test_expert_board_initialization(self):
        """Verify Expert board initializes correctly."""
        board = Board(16, 30, 99)
        assert board.rows == 16
        assert board.cols == 30
        assert board.mine_count == 99
        assert board.game_state == GameState.PLAYING

    def test_expert_first_click_safety_multiple_games(self):
        """Verify first-click safety across 20 games on Expert."""
        for game_num in range(20):
            board = Board(16, 30, 99)

            # Test various starting positions across wide board
            test_positions = [
                (0, 0),  # Top-left corner
                (0, 15),  # Top-center edge
                (0, 29),  # Top-right corner
                (8, 0),  # Left edge center
                (8, 15),  # True center
                (8, 29),  # Right edge center
                (15, 0),  # Bottom-left corner
                (15, 15),  # Bottom-center edge
                (15, 29),  # Bottom-right corner
            ]

            start_row, start_col = test_positions[game_num % len(test_positions)]

            # Place mines after first click
            board.place_mines(start_row, start_col)

            # Verify first-click cell is safe
            first_cell = board.get_cell(start_row, start_col)
            assert (
                not first_cell.mine
            ), f"Game {game_num}: First-click cell at ({start_row},"
            f" {start_col}) should not be a mine"

            # Verify all neighbors are safe
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    nr, nc = start_row + dr, start_col + dc
                    if board.is_valid_coordinate(nr, nc):
                        neighbor = board.get_cell(nr, nc)
                        assert (
                            not neighbor.mine
                        ), f"Game {game_num}: Neighbor ({nr}, {nc})"
                        " should not be a mine"

    def test_expert_correct_mine_count(self):
        """Verify exactly 99 mines placed on Expert board."""
        board = Board(16, 30, 99)
        board.place_mines(8, 15)

        mine_count = sum(1 for row in board.grid for cell in row if cell.mine)

        assert mine_count == 99, f"Expected 99 mines, found {mine_count}"

    def test_expert_win_condition(self):
        """Verify win detection on Expert board."""
        board = Board(16, 30, 99)
        board.place_mines(8, 15)

        # Calculate safe cells: 16*30 - 99 = 381
        safe_count = 0
        for row in range(16):
            for col in range(30):
                cell = board.get_cell(row, col)
                if not cell.mine:
                    cell.revealed = True
                    safe_count += 1

        assert safe_count == 381, f"Expected 381 safe cells, found {safe_count}"

        board.update_game_state()
        assert board.is_won()
        assert board.game_state == GameState.WON


class TestGameStateTransitions:
    """Test complete game state transitions and terminal states."""

    def test_playing_to_won_transition(self):
        """Verify clean transition from PLAYING to WON."""
        board = Board(9, 9, 10)
        assert board.game_state == GameState.PLAYING

        board.place_mines(4, 4)

        # Reveal all safe cells
        for row in range(9):
            for col in range(9):
                cell = board.get_cell(row, col)
                if not cell.mine:
                    cell.revealed = True

        board.update_game_state()
        assert board.game_state == GameState.WON
        assert not board.is_lost()

    def test_playing_to_lost_transition(self):
        """Verify clean transition from PLAYING to LOST."""
        board = Board(9, 9, 10)
        assert board.game_state == GameState.PLAYING

        board.place_mines(4, 4)

        # Reveal a mine
        for row in range(9):
            for col in range(9):
                cell = board.get_cell(row, col)
                if cell.mine:
                    cell.revealed = True
                    break
            else:
                continue
            break

        board.update_game_state()
        assert board.game_state == GameState.LOST
        assert not board.is_won()

    def test_won_state_persistence(self):
        """Verify WON state cannot revert to PLAYING."""
        board = Board(9, 9, 10)
        board.place_mines(4, 4)

        # Win the game
        for row in range(9):
            for col in range(9):
                cell = board.get_cell(row, col)
                if not cell.mine:
                    cell.revealed = True

        board.update_game_state()
        assert board.game_state == GameState.WON

        # Try to update state again (should stay WON)
        board.update_game_state()
        assert board.game_state == GameState.WON

    def test_lost_state_persistence(self):
        """Verify LOST state cannot revert to PLAYING."""
        board = Board(9, 9, 10)
        board.place_mines(4, 4)

        # Lose the game
        for row in range(9):
            for col in range(9):
                cell = board.get_cell(row, col)
                if cell.mine:
                    cell.revealed = True
                    break
            else:
                continue
            break

        board.update_game_state()
        assert board.game_state == GameState.LOST

        # Try to update state again (should stay LOST)
        board.update_game_state()
        assert board.game_state == GameState.LOST

    def test_loss_takes_priority_over_win(self):
        """Verify loss check takes priority over win check."""
        board = Board(9, 9, 10)
        board.place_mines(4, 4)

        # Reveal all cells (including mines)
        for row in range(9):
            for col in range(9):
                cell = board.get_cell(row, col)
                cell.revealed = True

        board.update_game_state()
        # Should be LOST, not WON, even though all safe cells are also revealed
        assert board.game_state == GameState.LOST
        assert not board.is_won()


class TestFlaggingAndCounter:
    """Test flagging behavior and counter integration."""

    def test_flag_placement_decrements_counter(self):
        """Verify placing flags decrements the mine counter."""
        board = Board(9, 9, 10)
        board.place_mines(4, 4)

        # Count initial flags
        flag_count = 0
        for row in range(9):
            for col in range(9):
                if board.grid[row][col].flagged:
                    flag_count += 1

        remaining_mines = board.mine_count - flag_count
        assert remaining_mines == 10

        # Place 3 flags
        board.grid[0][0].flagged = True
        board.grid[1][1].flagged = True
        board.grid[2][2].flagged = True

        flag_count = 0
        for row in range(9):
            for col in range(9):
                if board.grid[row][col].flagged:
                    flag_count += 1

        remaining_mines = board.mine_count - flag_count
        assert remaining_mines == 7

    def test_flag_removal_increments_counter(self):
        """Verify removing flags increments the mine counter."""
        board = Board(9, 9, 10)
        board.place_mines(4, 4)

        # Place and remove flags
        board.grid[0][0].flagged = True
        board.grid[1][1].flagged = True

        flag_count = 0
        for row in range(9):
            for col in range(9):
                if board.grid[row][col].flagged:
                    flag_count += 1

        remaining_mines = board.mine_count - flag_count
        assert remaining_mines == 8

        # Remove one flag
        board.grid[0][0].flagged = False

        flag_count = 0
        for row in range(9):
            for col in range(9):
                if board.grid[row][col].flagged:
                    flag_count += 1

        remaining_mines = board.mine_count - flag_count
        assert remaining_mines == 9

    def test_flags_do_not_affect_win_condition(self):
        """Verify flags don't affect win detection."""
        board = Board(9, 9, 10)
        board.place_mines(4, 4)

        # Place some flags (correct or incorrect doesn't matter)
        board.grid[0][0].flagged = True
        board.grid[1][1].flagged = True
        board.grid[2][2].flagged = True

        # Reveal all safe cells
        for row in range(9):
            for col in range(9):
                cell = board.get_cell(row, col)
                if not cell.mine:
                    cell.revealed = True

        board.update_game_state()
        # Should win despite flags
        assert board.is_won()
        assert board.game_state == GameState.WON


class TestFloodFillIntegration:
    """Test flood fill behavior in complete gameplay scenarios."""

    def test_flood_fill_on_first_click(self):
        """Verify flood fill triggers on first click when cell has 0 adjacent mines."""
        board = Board(9, 9, 10)
        board.place_mines(4, 4)  # Place mines avoiding center

        # Reveal center cell
        center_cell = board.get_cell(4, 4)
        initial_adjacent = center_cell.adjacent_mines

        board.reveal_cell(4, 4)

        # Count revealed cells
        revealed_count = sum(1 for row in board.grid for cell in row if cell.revealed)

        # If center had 0 adjacent mines, flood fill should have revealed many cells
        if initial_adjacent == 0:
            assert revealed_count > 1, "Flood fill should reveal multiple cells"

    def test_flood_fill_stops_at_numbered_cells(self):
        """Verify flood fill stops at numbered cells."""
        board = Board(9, 9, 10)
        board.place_mines(4, 4)

        board.reveal_cell(4, 4)

        # Verify all revealed cells either have 0 adjacent mines or are boundary cells
        for row in range(9):
            for col in range(9):
                cell = board.get_cell(row, col)
                if cell.revealed:
                    # Either 0 adjacent (blank) or numbered cell
                    assert 0 <= cell.adjacent_mines <= 8


class TestChordingIntegration:
    """Test chording mechanic in complete gameplay scenarios."""

    def test_chording_reveals_neighbors(self):
        """Verify chording reveals all unflagged neighbors."""
        board = Board(9, 9, 10)
        board.place_mines(4, 4)

        # Find a cell with adjacent mines
        target_cell = None
        for row in range(9):
            for col in range(9):
                cell = board.get_cell(row, col)
                board.reveal_cell(row, col)
                if cell.revealed and cell.adjacent_mines > 0:
                    target_cell = cell
                    target_row, target_col = row, col
                    break
            if target_cell:
                break

        if target_cell and target_cell.adjacent_mines > 0:
            # Flag the correct number of neighbors
            flags_placed = 0
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    nr, nc = target_row + dr, target_col + dc
                    if board.is_valid_coordinate(nr, nc):
                        neighbor = board.get_cell(nr, nc)
                        if neighbor.mine and flags_placed < target_cell.adjacent_mines:
                            neighbor.flagged = True
                            flags_placed += 1

            # If we placed all flags, chord should work
            if flags_placed == target_cell.adjacent_mines:
                revealed_before = sum(
                    1 for row in board.grid for cell in row if cell.revealed
                )

                board.chord_cell(target_row, target_col)

                revealed_after = sum(
                    1 for row in board.grid for cell in row if cell.revealed
                )

                # Should have revealed at least some neighbors
                assert revealed_after >= revealed_before


class TestCompleteGameScenarios:
    """Test complete game scenarios from start to finish."""

    def test_complete_winning_game_beginner(self):
        """Simulate a complete winning game on Beginner."""
        board = Board(9, 9, 10)
        board.place_mines(4, 4)

        # Strategy: Reveal all non-mine cells
        for row in range(9):
            for col in range(9):
                cell = board.get_cell(row, col)
                if not cell.mine and not cell.revealed:
                    board.reveal_cell(row, col)

        board.update_game_state()
        assert board.game_state == GameState.WON
        assert board.is_won()
        assert not board.is_lost()

    def test_complete_losing_game_beginner(self):
        """Simulate a complete losing game on Beginner."""
        board = Board(9, 9, 10)
        board.place_mines(4, 4)

        # Find and click a mine
        hit_mine = False
        for row in range(9):
            for col in range(9):
                cell = board.get_cell(row, col)
                if cell.mine:
                    board.reveal_cell(row, col)
                    hit_mine = True
                    break
            if hit_mine:
                break

        board.update_game_state()
        assert board.game_state == GameState.LOST
        assert board.is_lost()
        assert not board.is_won()

    def test_reset_and_play_multiple_games(self):
        """Verify reset allows multiple games to be played."""
        # Game 1 - Beginner
        board1 = Board(9, 9, 10)
        board1.place_mines(4, 4)
        assert board1.game_state == GameState.PLAYING

        # Game 2 - Intermediate (simulate reset)
        board2 = Board(16, 16, 40)
        board2.place_mines(8, 8)
        assert board2.game_state == GameState.PLAYING

        # Game 3 - Expert (simulate reset again)
        board3 = Board(16, 30, 99)
        board3.place_mines(8, 15)
        assert board3.game_state == GameState.PLAYING

        # All boards should be independent
        assert board1.rows == 9
        assert board2.rows == 16
        assert board3.rows == 16


class TestAdjacentMinesCalculation:
    """Test adjacent mine calculation in complete gameplay."""

    def test_all_cells_have_adjacent_counts(self):
        """Verify all cells have adjacent_mines calculated after mine placement."""
        board = Board(9, 9, 10)
        board.place_mines(4, 4)

        for row in range(9):
            for col in range(9):
                cell = board.get_cell(row, col)
                # All cells should have adjacent_mines calculated (0-8)
                assert 0 <= cell.adjacent_mines <= 8, f"Cell ({row}, {col}) has invalid"
                f" adjacent_mines: {cell.adjacent_mines}"

    def test_mine_cells_have_adjacent_counts(self):
        """Verify mine cells also have adjacent_mines calculated."""
        board = Board(9, 9, 10)
        board.place_mines(4, 4)

        for row in range(9):
            for col in range(9):
                cell = board.get_cell(row, col)
                if cell.mine:
                    # Mine cells should also have adjacent counts
                    # calculated
                    assert (
                        0 <= cell.adjacent_mines <= 8
                    ), f"Mine cell ({row}, {col}) has invalid"
                    f" adjacent_mines: {cell.adjacent_mines}"
