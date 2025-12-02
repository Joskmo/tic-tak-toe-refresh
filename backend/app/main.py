"""
Main FastAPI application
Entry point for the backend service
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.services import GameService, MatchmakingService
from app.websocket import ConnectionManager, MessageHandler


# Initialize services as singletons
game_service = GameService()
matchmaking_service = MatchmakingService(game_service)
connection_manager = ConnectionManager()
message_handler = MessageHandler(
    game_service=game_service,
    matchmaking_service=matchmaking_service,
    connection_manager=connection_manager
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    # Startup
    print("🚀 Backend starting up...")
    yield
    # Shutdown
    print("👋 Backend shutting down...")


# Create FastAPI app
app = FastAPI(
    title="Vanishing Tic-Tac-Toe API",
    description="Backend API for multiplayer Vanishing Tic-Tac-Toe game",
    version="0.1.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "message": "Vanishing Tic-Tac-Toe Backend",
        "version": "0.1.0"
    }


@app.get("/api/health")
async def health():
    """Detailed health check"""
    games = game_service.get_all_games()
    return {
        "status": "healthy",
        "active_games": len(games),
        "games": {
            game_id: game.state.value 
            for game_id, game in games.items()
        }
    }


@app.websocket("/ws/{player_id}")
async def websocket_endpoint(websocket: WebSocket, player_id: str):
    """
    WebSocket endpoint for game communication
    Each player connects with a unique player_id
    """
    print(f"🔌 WebSocket connection attempt from player: {player_id}")
    await connection_manager.connect(websocket, player_id)
    print(f"✅ WebSocket connected for player: {player_id}")
    
    try:
        # Send welcome message
        print(f"📤 Sending welcome message to {player_id}")
        await connection_manager.send_personal_message(
            {
                "type": "connected",
                "player_id": player_id,
                "message": "Connected to game server"
            },
            player_id
        )
        print(f"✅ Welcome message sent to {player_id}")
        
        # Listen for messages
        print(f"👂 Listening for messages from {player_id}")
        while True:
            data = await websocket.receive_json()
            print(f"📩 Received message from {player_id}: {data}")
            await message_handler.handle_message(player_id, data)
            
    except WebSocketDisconnect as e:
        print(f"🔌 WebSocket disconnect for {player_id}: {e}")
        # Handle disconnect
        connection_manager.disconnect(player_id)
        matchmaking_service.remove_player(player_id)
        
        # Notify other players in the game if any
        game = matchmaking_service.get_player_game(player_id)
        if game:
            await connection_manager.broadcast_to_game(
                {
                    "type": "player_disconnected",
                    "player_id": player_id,
                    "message": "Opponent disconnected"
                },
                game.game_id
            )
    except Exception as e:
        print(f"❌ Error in WebSocket connection for {player_id}: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        connection_manager.disconnect(player_id)
        matchmaking_service.remove_player(player_id)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

