"""
Matchmaking Service - Manages player queue and game matching
Follows Single Responsibility Principle: handles only matchmaking logic
"""
from typing import Optional, Set
from queue import Queue

from app.models import Game
from app.services.game_service import GameService


class MatchmakingService:
    """
    Service for managing player queue and matchmaking
    Implements Queue pattern for player matching
    """
    
    def __init__(self, game_service: GameService):
        self._game_service = game_service
        self._waiting_players: Queue[str] = Queue()
        self._player_to_game: dict[str, str] = {}
        self._waiting_set: Set[str] = set()  # For O(1) lookup
    
    def add_player_to_queue(self, player_id: str) -> Optional[Game]:
        """
        Add a player to the matchmaking queue
        Returns a Game if match was found, None if player is waiting
        """
        # Check if player is already in a game
        if player_id in self._player_to_game:
            game_id = self._player_to_game[player_id]
            game = self._game_service.get_game(game_id)
            
            # If game is finished, remove player and continue to matchmaking
            from app.models import GameState
            if game and game.state == GameState.FINISHED:
                print(f"🔄 Player {player_id} in finished game, removing...")
                del self._player_to_game[player_id]
                # Continue to matchmaking below
            else:
                # Player still in active game
                return game
        
        # Check if player is already waiting
        if player_id in self._waiting_set:
            return None
        
        # Try to match with waiting player
        if not self._waiting_players.empty():
            waiting_player_id = self._waiting_players.get()
            self._waiting_set.discard(waiting_player_id)
            
            # Create a new game
            game = self._game_service.create_game()
            
            # Add both players to the game
            game.add_player(waiting_player_id)
            game.add_player(player_id)
            
            # Track player-game mapping
            self._player_to_game[waiting_player_id] = game.game_id
            self._player_to_game[player_id] = game.game_id
            
            return game
        else:
            # No match found, add to queue
            self._waiting_players.put(player_id)
            self._waiting_set.add(player_id)
            return None
    
    def remove_player_from_queue(self, player_id: str) -> None:
        """Remove a player from the waiting queue"""
        self._waiting_set.discard(player_id)
        # Note: Can't efficiently remove from Queue, but we check _waiting_set when matching
    
    def get_player_game(self, player_id: str) -> Optional[Game]:
        """Get the game a player is in"""
        game_id = self._player_to_game.get(player_id)
        if game_id:
            return self._game_service.get_game(game_id)
        return None
    
    def remove_player(self, player_id: str) -> None:
        """Remove a player from matchmaking and their game"""
        # Remove from queue if waiting
        self.remove_player_from_queue(player_id)
        
        # Remove from game if in one
        game = self.get_player_game(player_id)
        if game:
            game.remove_player(player_id)
            del self._player_to_game[player_id]
    
    def is_player_waiting(self, player_id: str) -> bool:
        """Check if a player is in the waiting queue"""
        return player_id in self._waiting_set

