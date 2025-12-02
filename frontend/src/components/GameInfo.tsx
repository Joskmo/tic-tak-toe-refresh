/**
 * Game information component
 */
import React from 'react';
import { Game } from '../types/game';
import './GameInfo.css';

interface GameInfoProps {
  game: Game | null;
  playerId: string;
  isWaiting: boolean;
}

const GameInfo: React.FC<GameInfoProps> = ({ game, playerId, isWaiting }) => {
  if (isWaiting) {
    return (
      <div className="game-info waiting">
        <div className="spinner"></div>
        <h2>Ожидание противника...</h2>
        <p>Подключение к игре...</p>
      </div>
    );
  }

  if (!game) {
    return null;
  }

  const myPlayer = game.players.find(p => p.player_id === playerId);
  const opponent = game.players.find(p => p.player_id !== playerId);
  const isMyTurn = game.current_turn === playerId;

  return (
    <div className="game-info">
      <div className="players-info">
        <div className={`player-card ${isMyTurn ? 'active' : ''}`}>
          <h3>Вы</h3>
          <div className={`symbol-badge ${myPlayer?.symbol}`}>
            {myPlayer?.symbol}
          </div>
        </div>
        
        <div className="vs-divider">VS</div>
        
        <div className={`player-card ${!isMyTurn ? 'active' : ''}`}>
          <h3>Противник</h3>
          <div className={`symbol-badge ${opponent?.symbol}`}>
            {opponent?.symbol || '?'}
          </div>
        </div>
      </div>

      <div className="game-status">
        {game.state === 'playing' && (
          <p className={isMyTurn ? 'my-turn' : ''}>
            {isMyTurn ? '🎮 Ваш ход!' : '⏳ Ход противника...'}
          </p>
        )}
        
        {game.state === 'finished' && (
          <div className="game-over">
            {game.winner === playerId && <p className="winner">🎉 Победа!</p>}
            {game.winner && game.winner !== playerId && <p className="loser">😔 Поражение</p>}
            {!game.winner && <p className="draw">🤝 Ничья</p>}
          </div>
        )}
      </div>

      <div className="game-meta">
        <p>Сделано ходов: {game.move_count}</p>
        <p className="vanish-info">
          💫 На доске может быть максимум 3 ваших символа
        </p>
        <p className="vanish-info" style={{fontSize: '13px', marginTop: '5px'}}>
          При 4-м ходе самый старый символ исчезает (помечен ⏳)
        </p>
      </div>
    </div>
  );
};

export default GameInfo;

