# Backend - Vanishing Tic-Tac-Toe

Backend API для игры "Крестики-нолики с исчезновением" на FastAPI с WebSocket поддержкой.

## Архитектура

Проект следует принципам SOLID и чистой архитектуры:

```
backend/
├── app/
│   ├── models/          # Domain layer - игровые модели
│   │   └── game.py      # Game, Player, Move классы
│   ├── services/        # Application layer - бизнес-логика
│   │   ├── game_service.py         # Управление играми
│   │   └── matchmaking_service.py  # Матчмейкинг
│   ├── websocket/       # Infrastructure layer - WebSocket
│   │   ├── connection_manager.py   # Управление соединениями
│   │   └── message_handler.py      # Обработка сообщений
│   └── main.py          # Точка входа FastAPI
├── pyproject.toml       # Зависимости (UV)
└── Dockerfile
```

## Установка (локально)

### Используя UV (рекомендуется)

```bash
# Установите UV если еще не установлен
# curl -LsSf https://astral.sh/uv/install.sh | sh

cd backend

# Создание виртуального окружения и установка зависимостей
uv sync

# Запуск сервера
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Используя Docker

```bash
cd backend
docker build -t vanishing-ttt-backend .
docker run -p 8000:8000 vanishing-ttt-backend
```

## API Endpoints

### HTTP

- `GET /` - Health check
- `GET /api/health` - Детальная информация о состоянии сервера

### WebSocket

- `WS /ws/{player_id}` - WebSocket соединение для игры

## WebSocket Protocol

### Client → Server

**Присоединиться к очереди:**
```json
{
  "type": "join_queue"
}
```

**Сделать ход:**
```json
{
  "type": "make_move",
  "row": 0,
  "col": 1
}
```

**Покинуть игру:**
```json
{
  "type": "leave_game"
}
```

### Server → Client

**Подключение:**
```json
{
  "type": "connected",
  "player_id": "player_123",
  "message": "Connected to game server"
}
```

**Ожидание противника:**
```json
{
  "type": "waiting",
  "message": "Waiting for opponent..."
}
```

**Игра начата:**
```json
{
  "type": "game_start",
  "game": {
    "game_id": "uuid",
    "board": [["", "", ""], ["", "", ""], ["", "", ""]],
    "players": [...],
    "state": "playing",
    "current_turn": "player_id",
    "winner": null,
    "move_count": 0
  }
}
```

**Обновление игры:**
```json
{
  "type": "game_update",
  "game": {...}
}
```

**Игра окончена:**
```json
{
  "type": "game_over",
  "game": {...},
  "winner": "player_id"
}
```

**Ошибка:**
```json
{
  "type": "error",
  "message": "Error description"
}
```

## Разработка

### Добавление зависимостей

```bash
uv add package-name
```

### Запуск тестов

```bash
uv run pytest
```

## Технологии

- Python 3.12+
- FastAPI - веб-фреймворк
- WebSocket - реал-тайм коммуникация
- UV - менеджер пакетов
- Pydantic - валидация данных

