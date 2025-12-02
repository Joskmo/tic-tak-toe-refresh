# Frontend - Vanishing Tic-Tac-Toe

React + TypeScript frontend для игры "Крестики-нолики с исчезновением".

## Структура проекта

```
frontend/
├── public/
│   ├── index.html
│   └── manifest.json
├── src/
│   ├── components/      # React компоненты
│   │   ├── Board.tsx           # Игровая доска
│   │   ├── Board.css
│   │   ├── GameInfo.tsx        # Информация об игре
│   │   └── GameInfo.css
│   ├── hooks/           # Custom React hooks
│   │   └── useWebSocket.ts     # WebSocket хук
│   ├── types/           # TypeScript типы
│   │   └── game.ts
│   ├── App.tsx          # Главный компонент
│   ├── App.css
│   ├── index.tsx        # Точка входа
│   └── index.css
├── package.json
├── tsconfig.json
├── Dockerfile
└── nginx.conf
```

## Установка и запуск

### Локальная разработка

```bash
cd frontend

# Установка зависимостей
npm install

# Запуск dev сервера
npm start
```

Приложение откроется на http://localhost:3000

### Сборка для продакшн

```bash
npm run build
```

Оптимизированные файлы будут в папке `build/`.

### Docker

```bash
docker build -t vanishing-ttt-frontend .
docker run -p 3000:80 vanishing-ttt-frontend
```

## Конфигурация

### Переменные окружения

Создайте файл `.env` в корне frontend:

```env
REACT_APP_WS_URL=localhost:8000
```

Для продакшн:
```env
REACT_APP_WS_URL=yourdomain.com
```

## Архитектура

### Компоненты

- **App** - Главный компонент, управляет состоянием игры
- **Board** - Отображает игровое поле 3x3
- **GameInfo** - Показывает информацию об игроках и статусе игры

### Хуки

- **useWebSocket** - Управляет WebSocket соединением, автоматическим переподключением

### Типы

- Все типы синхронизированы с backend моделями
- Строгая типизация для всех WebSocket сообщений

## Функциональность

- ✅ Подключение к WebSocket серверу
- ✅ Автоматическое переподключение при разрыве связи
- ✅ Матчмейкинг (поиск противника)
- ✅ Игровой процесс в реальном времени
- ✅ Отображение текущего хода
- ✅ Анимации и визуальные эффекты
- ✅ Адаптивный дизайн (мобильные устройства)
- ✅ Отображение правила исчезновения ходов

## Стили

- Modern gradient design
- Анимации и transitions
- Responsive layout (мобильная адаптация)
- Glass-morphism эффекты

## Технологии

- React 18
- TypeScript
- WebSocket API
- CSS3 (Animations, Flexbox, Grid)
- Create React App

