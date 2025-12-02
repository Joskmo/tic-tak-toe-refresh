/**
 * Game types matching backend models
 */

export type CellValue = "" | "X" | "O";

export type GameState = "waiting" | "playing" | "finished";

export interface Player {
  player_id: string;
  symbol: CellValue;
}

export interface Game {
  game_id: string;
  board: CellValue[][];
  players: Player[];
  state: GameState;
  current_turn: string | null;
  winner: string | null;
  move_count: number;
  next_vanishing?: {
    [player_id: string]: {
      row: number;
      col: number;
    };
  };
}

export interface WebSocketMessage {
  type: string;
  [key: string]: any;
}

export interface ConnectedMessage extends WebSocketMessage {
  type: "connected";
  player_id: string;
  message: string;
}

export interface WaitingMessage extends WebSocketMessage {
  type: "waiting";
  message: string;
}

export interface GameStartMessage extends WebSocketMessage {
  type: "game_start";
  game: Game;
}

export interface GameUpdateMessage extends WebSocketMessage {
  type: "game_update";
  game: Game;
}

export interface GameOverMessage extends WebSocketMessage {
  type: "game_over";
  game: Game;
  winner: string | null;
}

export interface PlayerLeftMessage extends WebSocketMessage {
  type: "player_left";
  player_id: string;
  message: string;
}

export interface ErrorMessage extends WebSocketMessage {
  type: "error";
  message: string;
}

