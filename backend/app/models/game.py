"""
Game models - Domain layer following SOLID principles
"""
from enum import Enum
from typing import List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime


class CellValue(str, Enum):
    """Possible values for a game cell"""
    EMPTY = ""
    X = "X"
    O = "O"


class GameState(str, Enum):
    """Game state enumeration"""
    WAITING = "waiting"  # Waiting for second player
    PLAYING = "playing"  # Game in progress
    FINISHED = "finished"  # Game finished (win/draw)


@dataclass
class Move:
    """Represents a single move in the game"""
    row: int
    col: int
    player_id: str
    symbol: CellValue
    timestamp: datetime = field(default_factory=datetime.now)
    
    def position(self) -> Tuple[int, int]:
        """Get position as tuple"""
        return (self.row, self.col)


@dataclass
class Player:
    """Represents a player in the game"""
    player_id: str
    symbol: CellValue
    joined_at: datetime = field(default_factory=datetime.now)


class Game:
    """
    Game model - encapsulates game logic
    Follows Single Responsibility Principle: handles only game state and rules
    """
    
    def __init__(self, game_id: str):
        self.game_id: str = game_id
        self.board: List[List[CellValue]] = [
            [CellValue.EMPTY for _ in range(3)] for _ in range(3)
        ]
        self.players: List[Player] = []
        self.moves: List[Move] = []
        self.state: GameState = GameState.WAITING
        self.current_turn: Optional[str] = None
        self.winner: Optional[str] = None
        self.created_at: datetime = datetime.now()
    
    def add_player(self, player_id: str) -> bool:
        """
        Add a player to the game
        Returns True if player was added, False if game is full
        """
        if len(self.players) >= 2:
            return False
        
        symbol = CellValue.X if len(self.players) == 0 else CellValue.O
        player = Player(player_id=player_id, symbol=symbol)
        self.players.append(player)
        
        # Start game when second player joins
        if len(self.players) == 2:
            self.state = GameState.PLAYING
            self.current_turn = self.players[0].player_id
        
        return True
    
    def remove_player(self, player_id: str) -> None:
        """Remove a player from the game"""
        self.players = [p for p in self.players if p.player_id != player_id]
        if len(self.players) < 2 and self.state == GameState.PLAYING:
            self.state = GameState.FINISHED
    
    def get_player_symbol(self, player_id: str) -> Optional[CellValue]:
        """Get the symbol for a player"""
        for player in self.players:
            if player.player_id == player_id:
                return player.symbol
        return None
    
    def is_valid_move(self, row: int, col: int, player_id: str) -> bool:
        """Check if a move is valid"""
        # Check if it's player's turn
        if self.current_turn != player_id:
            return False
        
        # Check if game is in playing state
        if self.state != GameState.PLAYING:
            return False
        
        # Check bounds
        if not (0 <= row < 3 and 0 <= col < 3):
            return False
        
        # Check if cell is empty
        if self.board[row][col] != CellValue.EMPTY:
            return False
        
        return True
    
    def make_move(self, row: int, col: int, player_id: str) -> bool:
        """
        Make a move on the board
        Returns True if move was successful
        """
        if not self.is_valid_move(row, col, player_id):
            return False
        
        symbol = self.get_player_symbol(player_id)
        if symbol is None:
            return False
        
        # Place the move
        self.board[row][col] = symbol
        move = Move(row=row, col=col, player_id=player_id, symbol=symbol)
        self.moves.append(move)
        
        # Apply vanishing rule: if player has more than 3 symbols, remove oldest
        # This happens BEFORE win check (rule: max 3 symbols even in win)
        self._apply_vanishing_rule(player_id, symbol)
        
        # Check for winner (after vanishing applied)
        if self._check_winner(symbol):
            self.state = GameState.FINISHED
            self.winner = player_id
            print(f"🏆 Player {player_id} ({symbol.value}) wins!")
            return True
        
        # Check for draw (board is full)
        if self._is_board_full():
            self.state = GameState.FINISHED
            print(f"🤝 Game ended in a draw!")
            return True
        
        # Switch turns
        self._switch_turn()
        
        return True
    
    def _apply_vanishing_rule(self, player_id: str, symbol: CellValue) -> None:
        """
        Apply vanishing rule: each player can have max 3 symbols on board
        When 4th symbol is placed, the oldest one vanishes
        """
        # Get all moves by this player
        player_moves = [
            move for move in self.moves
            if move.player_id == player_id
        ]
        
        # If player has more than 3 symbols, remove the oldest one
        if len(player_moves) > 3:
            # The move to vanish is the one that was made 3 moves before the current one
            # e.g. if moves are [1, 2, 3, 4], we want to vanish 1. 
            # 1 is at index -4.
            move_to_vanish = player_moves[-4]
            self.board[move_to_vanish.row][move_to_vanish.col] = CellValue.EMPTY
            print(f"🔄 Vanishing: {symbol.value} at [{move_to_vanish.row}, {move_to_vanish.col}]")
    
    def _switch_turn(self) -> None:
        """Switch to the other player's turn"""
        if len(self.players) != 2:
            return
        
        current_index = 0 if self.current_turn == self.players[0].player_id else 1
        next_index = 1 - current_index
        self.current_turn = self.players[next_index].player_id
    
    def _check_winner(self, symbol: CellValue) -> bool:
        """Check if the given symbol has won"""
        # Check rows
        for row in self.board:
            if all(cell == symbol for cell in row):
                return True
        
        # Check columns
        for col in range(3):
            if all(self.board[row][col] == symbol for row in range(3)):
                return True
        
        # Check diagonals
        if all(self.board[i][i] == symbol for i in range(3)):
            return True
        if all(self.board[i][2-i] == symbol for i in range(3)):
            return True
        
        return False
    
    def _is_board_full(self) -> bool:
        """Check if the board is full"""
        return all(
            cell != CellValue.EMPTY 
            for row in self.board 
            for cell in row
        )
    
    def get_next_vanishing_position(self, player_id: str) -> Optional[Tuple[int, int]]:
        """
        Get the position that will vanish on next move by this player
        Returns None if player has less than 3 symbols
        """
        symbol = self.get_player_symbol(player_id)
        if symbol is None:
            return None
        
        # Get all moves by this player
        player_moves = [
            move for move in self.moves
            if move.player_id == player_id
        ]
        
        # If player has 3 or more symbols, next move will vanish the oldest active one
        if len(player_moves) >= 3:
            oldest_active_move = player_moves[-3]
            return (oldest_active_move.row, oldest_active_move.col)
        
        return None
    
    def to_dict(self) -> dict:
        """Convert game state to dictionary for serialization"""
        vanishing_positions = {}
        for player in self.players:
            pos = self.get_next_vanishing_position(player.player_id)
            if pos:
                vanishing_positions[player.player_id] = {
                    "row": pos[0],
                    "col": pos[1]
                }
        
        return {
            "game_id": self.game_id,
            "board": [[cell.value for cell in row] for row in self.board],
            "players": [
                {
                    "player_id": p.player_id,
                    "symbol": p.symbol.value
                }
                for p in self.players
            ],
            "state": self.state.value,
            "current_turn": self.current_turn,
            "winner": self.winner,
            "move_count": len(self.moves),
            "next_vanishing": vanishing_positions
        }

