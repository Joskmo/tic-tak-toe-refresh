# Руководство по деплою

Инструкции по развертыванию приложения "Vanishing Tic-Tac-Toe" на сервере.

## Предварительные требования

- Docker и Docker Compose установлены на сервере
- Доменное имя (для продакшн)
- Cloudflare аккаунт (для SSL сертификатов через Traefik)

## Локальная разработка

### Быстрый старт

```bash
# Клонировать репозиторий
git clone <your-repo>
cd vanishing_tic_tac_toe

# Запустить все сервисы
make dev

# Или в фоновом режиме
make dev-d
```

Доступ к приложению:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Остановка

```bash
make stop
```

### Просмотр логов

```bash
# Все логи
make logs

# Только backend
make logs-backend

# Только frontend
make logs-frontend
```

## Продакшн деплой с Traefik

### Шаг 1: Подготовка сервера

```bash
# Установить Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Установить Docker Compose
sudo apt update
sudo apt install docker-compose-plugin

# Создать Docker network для Traefik
docker network create web
```

### Шаг 2: Подготовка домена

Убедитесь, что:
1. Ваш домен настроен и A-записи указывают на IP сервера
2. Домен доступен из интернета (порты 80 и 443 открыты)
3. У вас есть email для уведомлений Let's Encrypt

### Шаг 3: Конфигурация

```bash
# Скопировать example файл
cp env.prod.example .env.prod

# Отредактировать .env.prod
nano .env.prod
```

Заполните:
```env
DOMAIN=yourdomain.com

# Сгенерировать пароль: htpasswd -nb admin your-password
TRAEFIK_USER=admin
TRAEFIK_PASSWORD=$apr1$...

# Email для Let's Encrypt уведомлений
LETSENCRYPT_EMAIL=your-email@example.com
```

### Шаг 4: Настройка Traefik

```bash
# Создать файл для SSL сертификатов
touch traefik/acme.json
chmod 600 traefik/acme.json

# Отредактировать traefik.yml (указать email)
nano traefik/traefik.yml
```

Измените строку:
```yaml
email: your-email@example.com  # Ваш email
```

### Шаг 5: Настройка DNS

Добавьте A-записи в вашем DNS провайдере:

```
Type: A
Name: @
Content: <IP вашего сервера>
TTL: Auto или 300

Type: A
Name: traefik
Content: <IP вашего сервера>
TTL: Auto или 300
```

**Важно:** Убедитесь, что домен разрешается на ваш сервер командой: `nslookup yourdomain.com`

### Шаг 6: Деплой

```bash
# Запустить продакшн
make prod

# Проверить логи
make logs-traefik
docker-compose -f docker-compose.prod.yml logs backend
docker-compose -f docker-compose.prod.yml logs frontend
```

### Шаг 7: Проверка

Приложение будет доступно на:
- https://yourdomain.com - Игра
- https://traefik.yourdomain.com - Traefik Dashboard

## Обновление приложения

```bash
# Получить последние изменения
git pull

# Пересобрать и перезапустить
make prod
```

## Мониторинг

### Проверка статуса контейнеров

```bash
docker ps
```

### Просмотр использования ресурсов

```bash
docker stats
```

### Логи

```bash
# Все сервисы
docker-compose -f docker-compose.prod.yml logs -f

# Конкретный сервис
docker-compose -f docker-compose.prod.yml logs -f backend
docker-compose -f docker-compose.prod.yml logs -f traefik
```

## Резервное копирование

### Backend (если добавите БД)

```bash
# Пример для PostgreSQL
docker exec postgres pg_dump -U user dbname > backup.sql
```

### Traefik SSL сертификаты

```bash
cp traefik/acme.json traefik/acme.json.backup
```

## Масштабирование

### Несколько инстансов backend

```bash
docker-compose -f docker-compose.prod.yml up -d --scale backend=3
```

Traefik автоматически распределит нагрузку.

## Устранение неполадок

### SSL сертификаты не получаются

1. Проверьте DNS настройки (A-записи должны указывать на ваш сервер)
2. Убедитесь, что Cloudflare proxy отключен (серое облако)
3. Проверьте API токен Cloudflare
4. Посмотрите логи: `docker logs traefik`

### Backend не доступен

```bash
# Проверить контейнер
docker ps
docker logs vanishing_ttt_backend

# Проверить сеть
docker network inspect web
```

### WebSocket не работает

1. Убедитесь, что путь `/ws` правильно проксируется через Traefik
2. Проверьте CORS настройки в backend
3. Проверьте frontend переменные окружения (REACT_APP_WS_URL)

## Безопасность

### Рекомендации

1. **Firewall**: Открыть только порты 80, 443, 22
   ```bash
   ufw allow 22/tcp
   ufw allow 80/tcp
   ufw allow 443/tcp
   ufw enable
   ```

2. **SSH**: Использовать ключи вместо паролей
3. **Traefik Dashboard**: Обязательно защитить паролем
4. **Обновления**: Регулярно обновлять Docker images
   ```bash
   docker-compose -f docker-compose.prod.yml pull
   make prod
   ```

5. **Rate limiting**: Уже настроен в Traefik config

## Производительность

### Оптимизация

1. **Nginx кэширование** (уже включено в frontend/nginx.conf)
2. **Gzip compression** (уже включено)
3. **Docker ресурсы**: Ограничить в docker-compose.yml если нужно

### Мониторинг

Рекомендуется добавить:
- Prometheus + Grafana для метрик
- Loki для логов
- Uptime Kuma для мониторинга доступности

## Полезные команды

```bash
# Остановить все
make stop

# Полная очистка
make clean

# Пересборка образов
make prod-build

# Войти в контейнер
docker exec -it vanishing_ttt_backend sh
docker exec -it vanishing_ttt_frontend sh

# Просмотр сетей
docker network ls
docker network inspect web

# Просмотр volumes
docker volume ls
```

## Дополнительные возможности

### Добавление Redis для сессий

Раскомментировать в docker-compose.prod.yml:

```yaml
redis:
  image: redis:7-alpine
  container_name: redis
  restart: unless-stopped
  networks:
    - web
```

### Добавление PostgreSQL для хранения истории игр

```yaml
postgres:
  image: postgres:17-alpine
  container_name: postgres
  restart: unless-stopped
  environment:
    POSTGRES_DB: ${DB_NAME}
    POSTGRES_USER: ${DB_USER}
    POSTGRES_PASSWORD: ${DB_PASSWORD}
  volumes:
    - postgres_data:/var/lib/postgresql/data
  networks:
    - web

volumes:
  postgres_data:
```

## Поддержка

Для вопросов и проблем создавайте issues в репозитории.

