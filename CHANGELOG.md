# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-12-01

### Added
- Initial release
- Backend FastAPI application with WebSocket support
- Frontend React + TypeScript application
- Core game logic: Vanishing Tic-Tac-Toe rules
- Matchmaking system (player queue)
- Real-time multiplayer gameplay
- Docker support for local development
- Docker Compose production setup with Traefik 3.5
- Comprehensive documentation (README, DEPLOYMENT, CONTRIBUTING)
- Unit tests for game logic
- GitHub Actions CI workflow
- VS Code configuration and recommended extensions
- Health check scripts
- Backup scripts
- Makefile for common tasks

### Features
- ✅ 3x3 game board
- ✅ Two-player online multiplayer
- ✅ Vanishing rule: every 3rd move removes the oldest move
- ✅ WebSocket real-time communication
- ✅ Automatic matchmaking
- ✅ Win detection (rows, columns, diagonals)
- ✅ Draw detection
- ✅ Responsive UI design
- ✅ Automatic WebSocket reconnection
- ✅ Clean architecture (SOLID principles)
- ✅ SSL support via Traefik
- ✅ Production-ready deployment

### Technical Stack
- **Backend**: Python 3.12+, FastAPI, WebSocket, UV package manager
- **Frontend**: React 18, TypeScript, WebSocket API
- **Infrastructure**: Docker, Docker Compose, Traefik 3.5, Nginx
- **Development**: VS Code, GitHub Actions, pytest, ESLint, Prettier

## [Unreleased]

### Planned Features
- Player statistics and leaderboard
- Game history (PostgreSQL)
- User profiles
- Chat between players
- Sound effects
- Dark theme
- Mobile app (React Native)
- Tournament mode
- Achievements system
- Spectator mode
- Game replay
- AI opponent

---

[0.1.0]: https://github.com/yourusername/vanishing_tic_tac_toe/releases/tag/v0.1.0

