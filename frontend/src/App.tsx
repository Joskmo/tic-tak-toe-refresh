/**
 * Main App component
 */
import React, { useState, useEffect, useCallback } from 'react';
import { useWebSocket } from './hooks/useWebSocket';
import Board from './components/Board';
import GameInfo from './components/GameInfo';
import { Game, WebSocketMessage } from './types/game';
import './App.css';

// Generate a unique player ID
const generatePlayerId = (): string => {
  const stored = localStorage.getItem('playerId');
  if (stored) {
    return stored;
  }
  const newId = `player_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  localStorage.setItem('playerId', newId);
  return newId;
};

const App: React.FC = () => {
  const [playerId] = useState(generatePlayerId);
  const [game, setGame] = useState<Game | null>(null);
  const [isWaiting, setIsWaiting] = useState(false);
  const [connectionStatus, setConnectionStatus] = useState<string>('connecting');
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [isPendingMove, setIsPendingMove] = useState(false);

  const handleMessage = useCallback((message: WebSocketMessage) => {
    console.log('Handling message:', message);

    switch (message.type) {
      case 'connected':
        setConnectionStatus('connected');
        setErrorMessage(null);
        break;

      case 'waiting':
        setIsWaiting(true);
        setGame(null);
        break;

      case 'game_start':
        setIsWaiting(false);
        setGame(message.game);
        setIsPendingMove(false);
        break;

      case 'game_update':
        setGame(message.game);
        setIsPendingMove(false);
        break;

      case 'game_over':
        setGame(message.game);
        setIsPendingMove(false);
        break;

      case 'player_left':
      case 'player_disconnected':
        setErrorMessage('Противник покинул игру');
        setIsPendingMove(false);
        setTimeout(() => {
          setGame(null);
          setIsWaiting(false);
        }, 3000);
        break;

      case 'error':
        setErrorMessage(message.message);
        setIsPendingMove(false);
        setTimeout(() => setErrorMessage(null), 3000);
        break;

      default:
        console.log('Unknown message type:', message.type);
    }
  }, []);

  const { isConnected, error, sendMessage } = useWebSocket(playerId, {
    onMessage: handleMessage,
    onConnect: () => setConnectionStatus('connected'),
    onDisconnect: () => setConnectionStatus('disconnected'),
  });

  const handleJoinQueue = useCallback(() => {
    if (isConnected) {
      sendMessage({ type: 'join_queue' });
      setErrorMessage(null);
    }
  }, [isConnected, sendMessage]);

  const handleCellClick = useCallback((row: number, col: number) => {
    // Блокируем повторные ходы пока ждём ответ от сервера
    if (!game || game.current_turn !== playerId || isPendingMove) {
      return;
    }

    // Проверяем что ячейка пустая (защита от race condition)
    if (game.board[row][col] !== "") {
      return;
    }

    setIsPendingMove(true);
    sendMessage({
      type: 'make_move',
      row,
      col,
    });
  }, [game, playerId, sendMessage, isPendingMove]);

  const handleNewGame = useCallback(() => {
    // First, leave the current game on backend
    if (game) {
      sendMessage({ type: 'leave_game' });
    }
    
    // Clear local state
    setGame(null);
    setIsWaiting(false);
    setErrorMessage(null);
    setIsPendingMove(false);
  }, [game, sendMessage]);

  // Connection status display
  if (!isConnected || connectionStatus === 'disconnected') {
    return (
      <div className="app">
        <div className="container">
          <div className="connection-error">
            <h1>⚠️ Нет соединения</h1>
            <p>{error || 'Подключение к серверу...'}</p>
            <div className="spinner"></div>
          </div>
        </div>
      </div>
    );
  }

  const isMyTurn = game?.current_turn === playerId;

  return (
    <div className="app">
      <div className="container">
        <header className="app-header">
          <h1>🎮 Крестики-Нолики с Исчезновением</h1>
          <p className="subtitle">Многопользовательская игра онлайн</p>
        </header>

        {errorMessage && (
          <div className="error-banner">
            ⚠️ {errorMessage}
          </div>
        )}

        {!game && !isWaiting && (
          <div className="welcome-screen">
            <div className="welcome-card">
              <h2>Добро пожаловать!</h2>
              <p>Правила игры:</p>
              <ul className="rules-list">
                <li>Стандартное поле 3×3</li>
                <li>Игра для двух игроков в реальном времени</li>
                <li>🌟 Каждый 3-й ход самый первый ход исчезает!</li>
                <li>Победа при трёх символах в ряд</li>
              </ul>
              <button className="btn-primary" onClick={handleJoinQueue}>
                🎯 Найти игру
              </button>
            </div>
          </div>
        )}

        {(game || isWaiting) && (
          <>
            <GameInfo game={game} playerId={playerId} isWaiting={isWaiting} />
            
            {game && (
              <>
                <Board
                  board={game.board}
                  onCellClick={handleCellClick}
                  isMyTurn={isMyTurn && !isPendingMove}
                  isActive={game.state === 'playing'}
                  vanishingPosition={
                    game.next_vanishing?.[playerId] || null
                  }
                  isPending={isPendingMove}
                />

                {game.state === 'finished' && (
                  <div className="game-actions">
                    <button className="btn-secondary" onClick={handleNewGame}>
                      🔄 Новая игра
                    </button>
                  </div>
                )}
              </>
            )}
          </>
        )}

        <footer className="app-footer">
          <p>ID игрока: <code>{playerId.substring(0, 20)}...</code></p>
        </footer>
      </div>
    </div>
  );
};

export default App;

