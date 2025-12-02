# Упрощенное руководство по деплою

Быстрое развертывание на сервере с Let's Encrypt SSL (без Cloudflare).

## Требования

- Ubuntu/Debian сервер с публичным IP
- Домен, указывающий на ваш сервер
- Порты 80 и 443 открыты
- Docker установлен

## Пошаговая инструкция

### 1. Установка Docker (если не установлен)

```bash
# Установить Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Добавить текущего пользователя в группу docker
sudo usermod -aG docker $USER

# Выйти и войти заново для применения
exit
```

### 2. Клонирование проекта

```bash
git clone <your-repo-url>
cd vanishing_tic_tac_toe
```

### 3. Настройка переменных окружения

```bash
# Создать файл конфигурации
cp env.prod.example .env.prod

# Отредактировать
nano .env.prod
```

**Минимальная конфигурация:**

```env
# Ваш домен
DOMAIN=yourdomain.com

# Email для Let's Encrypt
LETSENCRYPT_EMAIL=your-email@example.com

# Пароль для Traefik dashboard
# Сгенерировать: docker run --rm httpd:2.4-alpine htpasswd -nb admin your-password
TRAEFIK_USER=admin
TRAEFIK_PASSWORD=$apr1$xxxxxxxx
```

### 4. Настройка DNS

Добавьте A-записи в вашем DNS провайдере (Cloudflare, GoDaddy, и т.д.):

```
yourdomain.com      A    YOUR_SERVER_IP
traefik.yourdomain.com  A    YOUR_SERVER_IP
```

Проверьте:
```bash
nslookup yourdomain.com
nslookup traefik.yourdomain.com
```

### 5. Обновление email в Traefik

```bash
nano traefik/traefik.yml
```

Измените строку:
```yaml
email: your-email@example.com  # Укажите ваш email
```

### 6. Запуск

```bash
# Создать Docker network
docker network create web

# Создать файл для SSL сертификатов
touch traefik/acme.json
chmod 600 traefik/acme.json

# Запустить
docker-compose -f docker-compose.prod.yml --env-file .env.prod up -d --build
```

### 7. Проверка

```bash
# Просмотр логов
docker-compose -f docker-compose.prod.yml logs -f

# Проверить статус контейнеров
docker ps

# Проверить Traefik логи для SSL
docker logs traefik
```

Откройте:
- https://yourdomain.com - Игра
- https://traefik.yourdomain.com - Traefik Dashboard

## Как работают SSL сертификаты

1. **HTTP Challenge**: Traefik использует порт 80 для проверки владения доменом
2. **Let's Encrypt** автоматически выдает бесплатный SSL сертификат
3. **Автообновление**: Сертификаты обновляются автоматически каждые 90 дней
4. **Хранение**: Сертификаты хранятся в `traefik/acme.json`

## Решение проблем

### SSL сертификаты не получаются

```bash
# Проверить логи Traefik
docker logs traefik | grep -i error

# Убедиться, что порты открыты
sudo ufw status
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 22/tcp

# Проверить доступность домена
curl -I http://yourdomain.com
```

### Firewall

```bash
# Настроить UFW
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### Перезапуск

```bash
docker-compose -f docker-compose.prod.yml restart
```

### Просмотр сертификатов

```bash
# Проверить acme.json
cat traefik/acme.json | jq .

# Проверить сертификат в браузере
# Должен быть выдан: Let's Encrypt
```

## Обновление приложения

```bash
git pull
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d --build
```

## Backup

```bash
# Создать backup
tar -czf backup-$(date +%Y%m%d).tar.gz traefik/acme.json .env.prod

# Восстановить
tar -xzf backup-YYYYMMDD.tar.gz
```

## Мониторинг

```bash
# Логи в реальном времени
docker-compose -f docker-compose.prod.yml logs -f

# Использование ресурсов
docker stats

# Статус
docker ps -a
```

## Полезные команды

```bash
# Остановить все
docker-compose -f docker-compose.prod.yml down

# Удалить все (включая volumes)
docker-compose -f docker-compose.prod.yml down -v

# Пересобрать
docker-compose -f docker-compose.prod.yml build --no-cache

# Перезапустить один сервис
docker-compose -f docker-compose.prod.yml restart backend
```

## Безопасность

1. **Firewall**: Открыты только 22, 80, 443
2. **SSH**: Используйте ключи, отключите пароли
3. **Traefik Dashboard**: Защищен паролем
4. **SSL**: Автоматические сертификаты
5. **Обновления**: Регулярно обновляйте систему

```bash
# Обновить систему
sudo apt update && sudo apt upgrade -y

# Обновить Docker images
docker-compose -f docker-compose.prod.yml pull
docker-compose -f docker-compose.prod.yml up -d
```

## Тестирование SSL

```bash
# Проверить SSL конфигурацию
openssl s_client -connect yourdomain.com:443 -servername yourdomain.com

# Или используйте онлайн тест
# https://www.ssllabs.com/ssltest/
```

## Что дальше?

- Настроить мониторинг (Grafana + Prometheus)
- Добавить логирование (Loki)
- Настроить backup автоматически
- Добавить CI/CD pipeline

