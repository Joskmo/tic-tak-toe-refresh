"""
Game Service - Application layer
Follows Single Responsibility Principle: manages game instances
"""
from typing import Dict, Optional
from uuid import uuid4

from app.models import Game


class GameService:
    """
    Service for managing game instances
    Implements Service pattern for business logic
    """
    
    def __init__(self):
        self._games: Dict[str, Game] = {}
    
    def create_game(self) -> Game:
        """Create a new game"""
        game_id = str(uuid4())
        game = Game(game_id=game_id)
        self._games[game_id] = game
        return game
    
    def get_game(self, game_id: str) -> Optional[Game]:
        """Get a game by ID"""
        return self._games.get(game_id)
    
    def delete_game(self, game_id: str) -> bool:
        """Delete a game"""
        if game_id in self._games:
            del self._games[game_id]
            return True
        return False
    
    def get_all_games(self) -> Dict[str, Game]:
        """Get all games"""
        return self._games.copy()
    
    def cleanup_finished_games(self) -> int:
        """Remove finished games and return count of removed games"""
        from app.models import GameState
        
        finished_game_ids = [
            game_id for game_id, game in self._games.items()
            if game.state == GameState.FINISHED
        ]
        
        for game_id in finished_game_ids:
            del self._games[game_id]
        
        return len(finished_game_ids)

