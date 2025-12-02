#!/bin/bash
# ===========================================
# СКРИПТ ДЕПЛОЯ Vanishing Tic-Tac-Toe
# ===========================================

set -e

echo "🚀 Vanishing Tic-Tac-Toe - Деплой"
echo "================================"

# Проверка .env файла
if [ ! -f .env ]; then
    echo "❌ Файл .env не найден!"
    echo "Создайте его: nano .env"
    echo "Пример: DOMAIN=game.example.com"
    exit 1
fi

# Загрузка переменных
set -a
source .env
set +a

if [ -z "$DOMAIN" ]; then
    echo "❌ Переменная DOMAIN не задана в .env"
    exit 1
fi

echo "📋 Домен: $DOMAIN"

# Проверка наличия сети web
if ! docker network inspect web >/dev/null 2>&1; then
    echo "❌ Сеть 'web' не найдена!"
    echo "Сначала создайте общую сеть и запустите Traefik:"
    echo "  docker network create web"
    exit 1
fi

# Остановка старых контейнеров
echo "⏹️  Остановка старых контейнеров..."
docker-compose -f docker-compose.prod.yml down --remove-orphans 2>/dev/null || true

# Сборка и запуск
echo "🔨 Сборка и запуск..."
docker-compose -f docker-compose.prod.yml up -d --build

echo "⏳ Ожидание запуска..."
sleep 5

echo "✅ Готово! Игра доступна по адресу: https://$DOMAIN"
