"""
Unit tests for game logic
"""
import pytest
from app.models import Game, CellValue, GameState


class TestGame:
    """Test Game model"""

    def test_create_game(self):
        """Test game creation"""
        game = Game("test-game-id")
        assert game.game_id == "test-game-id"
        assert game.state == GameState.WAITING
        assert len(game.players) == 0
        assert len(game.moves) == 0

    def test_add_players(self):
        """Test adding players to game"""
        game = Game("test-game")
        
        # Add first player
        assert game.add_player("player1") is True
        assert len(game.players) == 1
        assert game.players[0].symbol == CellValue.X
        assert game.state == GameState.WAITING
        
        # Add second player
        assert game.add_player("player2") is True
        assert len(game.players) == 2
        assert game.players[1].symbol == CellValue.O
        assert game.state == GameState.PLAYING
        
        # Try to add third player (should fail)
        assert game.add_player("player3") is False
        assert len(game.players) == 2

    def test_make_move(self):
        """Test making a move"""
        game = Game("test-game")
        game.add_player("player1")
        game.add_player("player2")
        
        # Player 1 makes a move
        assert game.make_move(0, 0, "player1") is True
        assert game.board[0][0] == CellValue.X
        assert len(game.moves) == 1
        assert game.current_turn == "player2"

    def test_invalid_move_wrong_turn(self):
        """Test invalid move - wrong player's turn"""
        game = Game("test-game")
        game.add_player("player1")
        game.add_player("player2")
        
        # Player 2 tries to move (but it's player 1's turn)
        assert game.make_move(0, 0, "player2") is False
        assert game.board[0][0] == CellValue.EMPTY

    def test_invalid_move_cell_occupied(self):
        """Test invalid move - cell already occupied"""
        game = Game("test-game")
        game.add_player("player1")
        game.add_player("player2")
        
        # Player 1 makes a move
        game.make_move(0, 0, "player1")
        
        # Player 2 tries to move to same cell
        assert game.make_move(0, 0, "player2") is False

    def test_vanishing_rule(self):
        """Test vanishing rule - each player max 3 symbols, 4th removes oldest"""
        game = Game("test-game")
        game.add_player("player1")
        game.add_player("player2")
        
        # Player 1 makes moves (avoiding winning patterns)
        game.make_move(0, 0, "player1")  # X at [0,0]
        game.make_move(1, 1, "player2")  # O at [1,1] (center)
        game.make_move(0, 2, "player1")  # X at [0,2]
        game.make_move(2, 0, "player2")  # O at [2,0]
        game.make_move(2, 2, "player1")  # X at [2,2]
        
        # All 3 X's should be on board (diagonal pattern, no win yet)
        assert game.board[0][0] == CellValue.X
        assert game.board[0][2] == CellValue.X
        assert game.board[2][2] == CellValue.X
        
        # Player 2 makes 3rd move
        game.make_move(0, 1, "player2")  # O at [0,1]
        
        # All 3 O's should be on board
        assert game.board[1][1] == CellValue.O
        assert game.board[2][0] == CellValue.O
        assert game.board[0][1] == CellValue.O
        
        # Player 1 makes 4th move - [0,0] should vanish
        game.make_move(1, 0, "player1")  # X at [1,0] - [0,0] vanishes
        
        # Check that [0,0] vanished but other X's remain
        assert game.board[0][0] == CellValue.EMPTY  # Vanished!
        assert game.board[0][2] == CellValue.X
        assert game.board[2][2] == CellValue.X
        assert game.board[1][0] == CellValue.X
        
        # All O's should still be there
        assert game.board[1][1] == CellValue.O
        assert game.board[2][0] == CellValue.O
        assert game.board[0][1] == CellValue.O

    def test_win_condition_row(self):
        """Test win condition - three in a row"""
        game = Game("test-game")
        game.add_player("player1")
        game.add_player("player2")
        
        # Player 1 wins with top row
        game.make_move(0, 0, "player1")  # X
        game.make_move(1, 0, "player2")  # O
        game.make_move(0, 1, "player1")  # X
        game.make_move(1, 1, "player2")  # O
        game.make_move(0, 2, "player1")  # X - wins!
        
        assert game.state == GameState.FINISHED
        assert game.winner == "player1"

    def test_win_condition_column(self):
        """Test win condition - three in a column"""
        game = Game("test-game")
        game.add_player("player1")
        game.add_player("player2")
        
        # Player 2 wins with first column
        game.make_move(0, 1, "player1")  # X
        game.make_move(0, 0, "player2")  # O
        game.make_move(1, 1, "player1")  # X
        game.make_move(1, 0, "player2")  # O
        game.make_move(0, 2, "player1")  # X
        game.make_move(2, 0, "player2")  # O - wins!
        
        assert game.state == GameState.FINISHED
        assert game.winner == "player2"

    def test_win_condition_diagonal(self):
        """Test win condition - diagonal"""
        game = Game("test-game")
        game.add_player("player1")
        game.add_player("player2")
        
        # Player 1 wins with diagonal
        game.make_move(0, 0, "player1")  # X
        game.make_move(0, 1, "player2")  # O
        game.make_move(1, 1, "player1")  # X
        game.make_move(0, 2, "player2")  # O
        game.make_move(2, 2, "player1")  # X - wins!
        
        assert game.state == GameState.FINISHED
        assert game.winner == "player1"
        
    def test_win_after_vanishing(self):
        """Test win condition happening exactly when a piece vanishes"""
        game = Game("test-game")
        game.add_player("player1")
        game.add_player("player2")
        
        # Setup: P1 has pieces that will NOT win yet
        # P1: [2,2]
        game.make_move(2, 2, "player1")
        # P2: [1,0]
        game.make_move(1, 0, "player2")
        
        # P1: [0,0]
        game.make_move(0, 0, "player1")
        # P2: [1,1]
        game.make_move(1, 1, "player2")
        
        # P1: [0,1]
        game.make_move(0, 1, "player1")
        # P2: [2,0]
        game.make_move(2, 0, "player2")
        
        # Current P1: [2,2] (oldest), [0,0], [0,1]
        # P1 places [0,2]. 
        # [2,2] should vanish.
        # Remaining: [0,0], [0,1], [0,2] -> Row 0 complete -> Win.
        
        game.make_move(0, 2, "player1")
        
        # Check that [2,2] vanished
        assert game.board[2][2] == CellValue.EMPTY
        # Check that [0,0], [0,1], [0,2] are present
        assert game.board[0][0] == CellValue.X
        assert game.board[0][1] == CellValue.X
        assert game.board[0][2] == CellValue.X
        
        # Check game state
        assert game.state == GameState.FINISHED
        assert game.winner == "player1"
