"""
WebSocket Connection Manager
Follows Single Responsibility Principle: manages WebSocket connections
"""
from typing import Dict, Set
from fastapi import WebSocket


class ConnectionManager:
    """
    Manages WebSocket connections
    Implements Observer pattern for broadcasting messages
    """
    
    def __init__(self):
        # Map player_id to WebSocket connection
        self._active_connections: Dict[str, WebSocket] = {}
        # Map game_id to set of player_ids
        self._game_players: Dict[str, Set[str]] = {}
    
    async def connect(self, websocket: WebSocket, player_id: str) -> None:
        """Accept and store a new WebSocket connection"""
        await websocket.accept()
        self._active_connections[player_id] = websocket
    
    def remove_player_from_game(self, player_id: str, game_id: str) -> None:
        """Remove a player from a specific game"""
        if game_id in self._game_players:
            self._game_players[game_id].discard(player_id)
            if not self._game_players[game_id]:
                del self._game_players[game_id]

    def disconnect(self, player_id: str) -> None:
        """Remove a WebSocket connection"""
        if player_id in self._active_connections:
            del self._active_connections[player_id]
        
        # Remove from game players
        for game_id, players in list(self._game_players.items()):
            if player_id in players:
                players.discard(player_id)
                if not players:
                    del self._game_players[game_id]
    
    def add_player_to_game(self, player_id: str, game_id: str) -> None:
        """Associate a player with a game"""
        if game_id not in self._game_players:
            self._game_players[game_id] = set()
        self._game_players[game_id].add(player_id)
    
    def get_game_players(self, game_id: str) -> Set[str]:
        """Get all players in a game"""
        return self._game_players.get(game_id, set()).copy()
    
    async def send_personal_message(self, message: dict, player_id: str) -> None:
        """Send a message to a specific player"""
        websocket = self._active_connections.get(player_id)
        if websocket:
            try:
                await websocket.send_json(message)
            except Exception:
                # Connection might be closed
                self.disconnect(player_id)
    
    async def broadcast_to_game(self, message: dict, game_id: str) -> None:
        """Broadcast a message to all players in a game"""
        players = self.get_game_players(game_id)
        for player_id in players:
            await self.send_personal_message(message, player_id)
    
    def is_connected(self, player_id: str) -> bool:
        """Check if a player is connected"""
        return player_id in self._active_connections

