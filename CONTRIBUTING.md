# Contributing to Vanishing Tic-Tac-Toe

Спасибо за интерес к проекту! Вот руководство для разработчиков.

## Начало работы

### Форк и клонирование

```bash
# Форкните репозиторий на GitHub
# Затем клонируйте ваш форк
git clone https://github.com/YOUR-USERNAME/vanishing_tic_tac_toe.git
cd vanishing_tic_tac_toe

# Добавьте upstream remote
git remote add upstream https://github.com/ORIGINAL-OWNER/vanishing_tic_tac_toe.git
```

### Настройка окружения

```bash
# Запустить dev окружение
make dev

# Или установить зависимости локально
cd backend && uv sync
cd ../frontend && npm install
```

## Архитектура проекта

### Backend

Следует принципам SOLID и чистой архитектуры:

- **Models** (`app/models/`) - Domain layer, бизнес-логика игры
- **Services** (`app/services/`) - Application layer, управление играми
- **WebSocket** (`app/websocket/`) - Infrastructure layer, коммуникация
- **Main** (`app/main.py`) - Entry point, FastAPI приложение

### Frontend

React компонентная архитектура:

- **Components** - Переиспользуемые UI компоненты
- **Hooks** - Custom React hooks для логики
- **Types** - TypeScript определения

## Coding Standards

### Backend (Python)

- **Style**: PEP 8
- **Type hints**: Обязательны для всех функций
- **Docstrings**: Для всех публичных классов и методов
- **Naming**: 
  - Classes: `PascalCase`
  - Functions/methods: `snake_case`
  - Constants: `UPPER_SNAKE_CASE`

Пример:

```python
class GameService:
    """Service for managing game instances."""
    
    def create_game(self) -> Game:
        """Create a new game."""
        game_id = str(uuid4())
        return Game(game_id=game_id)
```

### Frontend (TypeScript/React)

- **Style**: Prettier/ESLint
- **Components**: Functional components with hooks
- **Naming**:
  - Components: `PascalCase`
  - Functions/variables: `camelCase`
  - Types/Interfaces: `PascalCase`
- **Files**: Component files should match component name

Пример:

```typescript
interface BoardProps {
  board: CellValue[][];
  onCellClick: (row: number, col: number) => void;
}

const Board: React.FC<BoardProps> = ({ board, onCellClick }) => {
  // Component logic
};
```

## Разработка новых функций

### Процесс

1. **Создайте issue** для обсуждения функции
2. **Создайте ветку** от `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Реализуйте функцию** следуя coding standards
4. **Тестируйте** локально
5. **Commit** с понятным сообщением:
   ```bash
   git commit -m "feat: add player statistics tracking"
   ```
6. **Push** в ваш форк:
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Создайте Pull Request**

### Commit Messages

Используйте [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` - новая функция
- `fix:` - исправление бага
- `docs:` - изменения в документации
- `style:` - форматирование, отсутствующие точки с запятой и т.д.
- `refactor:` - рефакторинг кода
- `test:` - добавление тестов
- `chore:` - обновление зависимостей, конфигурации и т.д.

Примеры:
```
feat(backend): add player statistics tracking
fix(frontend): resolve websocket reconnection issue
docs: update deployment instructions
```

## Тестирование

### Backend

```bash
cd backend

# Запустить тесты
uv run pytest

# С покрытием
uv run pytest --cov=app --cov-report=html
```

### Frontend

```bash
cd frontend

# Запустить тесты
npm test

# Coverage
npm test -- --coverage
```

## Pull Requests

### Чеклист перед PR

- [ ] Код следует coding standards
- [ ] Добавлены тесты для новой функциональности
- [ ] Все тесты проходят
- [ ] Документация обновлена
- [ ] Commit messages следуют Conventional Commits
- [ ] Нет конфликтов с main веткой

### PR Template

```markdown
## Описание
Краткое описание изменений

## Тип изменения
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Как тестировать
Шаги для проверки изменений

## Screenshots (если применимо)

## Checklist
- [ ] Код следует проектным стандартам
- [ ] Добавлены тесты
- [ ] Документация обновлена
```

## Идеи для улучшений

### Backend

- [ ] Добавить Redis для хранения сессий
- [ ] Реализовать систему рейтингов
- [ ] Добавить историю игр (PostgreSQL)
- [ ] Реализовать систему достижений
- [ ] Добавить чат между игроками
- [ ] Таймер на ход

### Frontend

- [ ] Добавить звуковые эффекты
- [ ] Реализовать темную тему
- [ ] Добавить анимации для исчезновения ходов
- [ ] Показывать историю ходов
- [ ] Добавить профили игроков
- [ ] Реализовать зрительский режим

### Infrastructure

- [ ] CI/CD pipeline
- [ ] Автоматические тесты
- [ ] Prometheus метрики
- [ ] Grafana дашборды
- [ ] Мониторинг с Uptime Kuma

## Вопросы?

Создайте issue или свяжитесь с maintainers.

## Лицензия

Все contributions будут лицензированы под MIT License.

