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
}

const Board: React.FC<BoardProps> = ({ board, onCellClick, isMyTurn, vanishingPosition, isActive }) => {
  const isVanishing = (rowIndex: number, colIndex: number) => {
    return vanishingPosition?.row === rowIndex && vanishingPosition?.col === colIndex;
  };

  return (
    <div className={`board ${!isActive ? 'inactive' : ''}`}>
      {board.map((row, rowIndex) => (
        <div key={rowIndex} className="board-row">
          {row.map((cell, colIndex) => {
            const willVanish = isVanishing(rowIndex, colIndex);
            return (
              <button
                key={`${rowIndex}-${colIndex}`}
                className={`cell ${cell ? 'filled' : ''} ${isMyTurn && isActive ? 'clickable' : ''} ${willVanish ? 'vanishing' : ''}`}
                onClick={() => isActive && onCellClick(rowIndex, colIndex)}
                disabled={!isActive || !isMyTurn || cell !== ""}
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

