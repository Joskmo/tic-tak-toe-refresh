"""
WebSocket Message Handler
Handles incoming WebSocket messages and delegates to appropriate services
"""
from typing import Dict, Any

from app.services import GameService, MatchmakingService
from app.websocket.connection_manager import ConnectionManager


class MessageHandler:
    """
    Handles WebSocket messages
    Follows Single Responsibility Principle: processes messages and coordinates services
    """
    
    def __init__(
        self,
        game_service: GameService,
        matchmaking_service: MatchmakingService,
        connection_manager: ConnectionManager
    ):
        self._game_service = game_service
        self._matchmaking_service = matchmaking_service
        self._connection_manager = connection_manager
    
    async def handle_message(self, player_id: str, message: Dict[str, Any]) -> None:
        """
        Process incoming message from a player
        """
        message_type = message.get("type")
        
        if message_type == "join_queue":
            await self._handle_join_queue(player_id)
        elif message_type == "make_move":
            await self._handle_make_move(player_id, message)
        elif message_type == "leave_game":
            await self._handle_leave_game(player_id)
        else:
            await self._send_error(player_id, f"Unknown message type: {message_type}")
    
    async def _handle_join_queue(self, player_id: str) -> None:
        """Handle player joining matchmaking queue"""
        game = self._matchmaking_service.add_player_to_queue(player_id)
        
        if game:
            # Match found! Notify both players
            self._connection_manager.add_player_to_game(player_id, game.game_id)
            
            # Find the other player
            for player in game.players:
                if player.player_id != player_id:
                    self._connection_manager.add_player_to_game(
                        player.player_id, 
                        game.game_id
                    )
            
            # Broadcast game start to both players
            await self._connection_manager.broadcast_to_game(
                {
                    "type": "game_start",
                    "game": game.to_dict()
                },
                game.game_id
            )
        else:
            # Player is waiting for opponent
            await self._connection_manager.send_personal_message(
                {
                    "type": "waiting",
                    "message": "Waiting for opponent..."
                },
                player_id
            )
    
    async def _handle_make_move(
        self, 
        player_id: str, 
        message: Dict[str, Any]
    ) -> None:
        """Handle player making a move"""
        row = message.get("row")
        col = message.get("col")
        
        if row is None or col is None:
            await self._send_error(player_id, "Invalid move: missing row or col")
            return
        
        game = self._matchmaking_service.get_player_game(player_id)
        if not game:
            await self._send_error(player_id, "You are not in a game")
            return
        
        print(f"🎯 Player {player_id} attempting move at [{row}, {col}]")
        
        # Attempt to make the move
        success = game.make_move(row, col, player_id)
        
        if success:
            print(f"✅ Move successful! Game state: {game.state.value}")
            
            # Broadcast updated game state to all players
            await self._connection_manager.broadcast_to_game(
                {
                    "type": "game_update",
                    "game": game.to_dict()
                },
                game.game_id
            )
            
            # Check if game is finished
            from app.models import GameState
            if game.state == GameState.FINISHED:
                print(f"🎮 Game finished! Winner: {game.winner}")
                await self._connection_manager.broadcast_to_game(
                    {
                        "type": "game_over",
                        "game": game.to_dict(),
                        "winner": game.winner
                    },
                    game.game_id
                )
        else:
            print(f"❌ Move failed for player {player_id}")
            await self._send_error(player_id, "Invalid move")
    
    async def _handle_leave_game(self, player_id: str) -> None:
        """Handle player leaving game"""
        game = self._matchmaking_service.get_player_game(player_id)
        
        if game:
            # First, remove the leaving player from the game's broadcast group
            # This prevents them from receiving their own "player_left" message
            self._connection_manager.remove_player_from_game(player_id, game.game_id)
            
            # Notify OTHER players
            await self._connection_manager.broadcast_to_game(
                {
                    "type": "player_left",
                    "player_id": player_id,
                    "message": "Opponent has left the game"
                },
                game.game_id
            )
        
        # Only remove from matchmaking/game, keep connection open!
        self._matchmaking_service.remove_player(player_id)
        # self._connection_manager.disconnect(player_id)  <-- DO NOT DISCONNECT SOCKET
    
    async def _send_error(self, player_id: str, error_message: str) -> None:
        """Send error message to player"""
        await self._connection_manager.send_personal_message(
            {
                "type": "error",
                "message": error_message
            },
            player_id
        )

