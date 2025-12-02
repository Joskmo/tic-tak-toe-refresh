/**
 * Game board component
 */
import React from 'react';
import { CellValue } from '../types/game';
import './Board.css';

interface BoardProps {
  board: CellValue[][];
  onCellClick: (row: number, col: number) => void;
  isMyTurn: boolean;
  vanishingPosition?: { row: number; col: number } | null;
  isActive: boolean;
  isPending?: boolean;
}

const Board: React.FC<BoardProps> = ({ board, onCellClick, isMyTurn, vanishingPosition, isActive, isPending = false }) => {
  const isVanishing = (rowIndex: number, colIndex: number) => {
    return vanishingPosition?.row === rowIndex && vanishingPosition?.col === colIndex;
  };

  return (
    <div className={`board ${!isActive ? 'inactive' : ''} ${isPending ? 'pending' : ''}`}>
      {board.map((row, rowIndex) => (
        <div key={rowIndex} className="board-row">
          {row.map((cell, colIndex) => {
            const willVanish = isVanishing(rowIndex, colIndex);
            const isDisabled = !isActive || !isMyTurn || cell !== "" || isPending;
            return (
              <button
                key={`${rowIndex}-${colIndex}`}
                className={`cell ${cell ? 'filled' : ''} ${isMyTurn && isActive && !isPending ? 'clickable' : ''} ${willVanish ? 'vanishing' : ''}`}
                onClick={() => isActive && !isPending && onCellClick(rowIndex, colIndex)}
                disabled={isDisabled}
                title={willVanish ? 'Эта клетка исчезнет после вашего следующего хода' : ''}
              >
                {cell && <span className={`symbol ${cell}`}>{cell}</span>}
                {willVanish && <span className="vanish-indicator">⏳</span>}
              </button>
            );
          })}
        </div>
      ))}
    </div>
  );
};

export default Board;

