# Environment Variables Setup

Руководство по настройке переменных окружения для разных сред.

## Локальная разработка

### Backend

Backend не требует дополнительных переменных окружения для локального запуска.

Опционально можно создать `backend/.env`:
```env
# Debug mode
DEBUG=1
LOG_LEVEL=DEBUG

# CORS (если нужно ограничить)
# CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

### Frontend

Создайте `frontend/.env`:
```env
# WebSocket URL (без протокола, он определяется автоматически)
REACT_APP_WS_URL=localhost:8000
```

Для других портов:
```env
REACT_APP_WS_URL=localhost:8001
```

## Docker Compose (локальная разработка)

Не требует дополнительных файлов `.env`. Все настройки в `docker-compose.yml`.

## Продакшн (с Traefik)

### Создание `.env.prod`

```bash
cp env.prod.example .env.prod
nano .env.prod
```

### Обязательные переменные

```env
# Ваш домен
DOMAIN=yourdomain.com

# Traefik Dashboard доступ
# Сгенерировать: htpasswd -nb admin your-password
TRAEFIK_USER=admin
TRAEFIK_PASSWORD=$apr1$xyz$hashedpasswordhere

# Cloudflare API для SSL сертификатов
CF_API_EMAIL=your-email@example.com
CF_DNS_API_TOKEN=your-cloudflare-api-token
```

### Генерация Traefik пароля

**Linux/macOS:**
```bash
sudo apt install apache2-utils  # Debian/Ubuntu
# или
brew install apache2-utils      # macOS

htpasswd -nb admin your-password
```

**Windows (PowerShell):**
```powershell
# Используйте онлайн генератор:
# https://hostingcanada.org/htpasswd-generator/
```

**Docker (если htpasswd не установлен):**
```bash
docker run --rm httpd:2.4-alpine htpasswd -nb admin your-password
```

### Email для Let's Encrypt

Укажите ваш email для уведомлений о SSL сертификатах:

```env
LETSENCRYPT_EMAIL=your-email@example.com
```

Let's Encrypt будет отправлять уведомления:
- О приближающемся истечении сертификата
- О проблемах с обновлением
- Важные изменения в сервисе

### Опциональные переменные (для будущего расширения)

```env
# PostgreSQL (если добавите)
DB_HOST=postgres
DB_PORT=5432
DB_NAME=vanishing_ttt
DB_USER=postgres
DB_PASSWORD=your-secure-password

# Redis (если добавите)
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=your-redis-password

# Monitoring
SENTRY_DSN=your-sentry-dsn
```

## Frontend Build Environment

При сборке production frontend Docker image, переменные передаются через build args:

```bash
docker build \
  --build-arg REACT_APP_WS_URL=yourdomain.com \
  -t vanishing-ttt-frontend \
  ./frontend
```

Или в `docker-compose.prod.yml`:
```yaml
frontend:
  build:
    context: ./frontend
    args:
      REACT_APP_WS_URL: ${DOMAIN}
```

## Проверка переменных

### Локально

```bash
# Backend
cd backend
uv run python -c "import os; print(os.getenv('DEBUG', 'not set'))"

# Frontend
cd frontend
npm run env
```

### Docker

```bash
# Backend
docker exec vanishing_ttt_backend env

# Frontend build args
docker inspect vanishing_ttt_frontend | grep -A 10 Config
```

## Безопасность

### ⚠️ Важно

1. **Никогда не коммитьте `.env` файлы с секретами**
2. **Используйте сильные пароли**
3. **Храните API токены в безопасности**
4. **Регулярно меняйте пароли**
5. **Используйте разные пароли для разных сред**

### Checklist безопасности

- [ ] `.env` в `.gitignore`
- [ ] Используется `.env.example` вместо реальных значений
- [ ] Сильные пароли (16+ символов)
- [ ] API токены имеют минимальные необходимые права
- [ ] Traefik dashboard защищен паролем
- [ ] SSL сертификаты настроены
- [ ] Firewall настроен (только 22, 80, 443)

## Шаблоны для копирования

### `.env` (локальная разработка frontend)

```env
REACT_APP_WS_URL=localhost:8000
```

### `.env.prod` (продакшн)

```env
DOMAIN=yourdomain.com
TRAEFIK_USER=admin
TRAEFIK_PASSWORD=$apr1$...
LETSENCRYPT_EMAIL=your-email@example.com
```

### `backend/.env` (опционально)

```env
DEBUG=1
LOG_LEVEL=DEBUG
```

## Troubleshooting

### Frontend не подключается к WebSocket

Проверьте `REACT_APP_WS_URL`:
```bash
# Должен быть БЕЗ протокола (ws:// или wss://)
# Правильно:
REACT_APP_WS_URL=localhost:8000
REACT_APP_WS_URL=yourdomain.com

# Неправильно:
REACT_APP_WS_URL=ws://localhost:8000
REACT_APP_WS_URL=wss://yourdomain.com
```

### Traefik не может получить SSL сертификаты

1. Проверьте CF_DNS_API_TOKEN
2. Проверьте CF_API_EMAIL
3. Убедитесь, что домен использует Cloudflare DNS
4. Отключите Cloudflare proxy (серое облако)
5. Проверьте логи: `docker logs traefik`

### Переменные не применяются

После изменения `.env` файлов:
```bash
# Локально
docker-compose down
docker-compose up -d

# Продакшн
docker-compose -f docker-compose.prod.yml down
make prod
```

## Полезные ссылки

- [12 Factor App - Config](https://12factor.net/config)
- [Traefik - Let's Encrypt](https://doc.traefik.io/traefik/https/acme/)
- [Cloudflare API Tokens](https://developers.cloudflare.com/api/tokens/)

