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
    echo ""
    echo "Создайте его:"
    echo "  nano .env"
    echo ""
    echo "Пример содержимого:"
    echo "  DOMAIN=game.example.com"
    echo "  ACME_EMAIL=admin@example.com"
    exit 1
fi

# Загрузка переменных для проверки
set -a
source .env
set +a

# Проверка обязательных переменных
if [ -z "$DOMAIN" ]; then
    echo "❌ Переменная DOMAIN не задана в .env"
    exit 1
fi

if [ -z "$ACME_EMAIL" ]; then
    echo "❌ Переменная ACME_EMAIL не задана в .env"
    exit 1
fi

echo "📋 Конфигурация:"
echo "   Домен: $DOMAIN"
echo "   Email: $ACME_EMAIL"
echo ""

# Создание директории для сертификатов если её нет
mkdir -p traefik/letsencrypt
chmod 600 traefik/letsencrypt

# Остановка старых контейнеров
echo "⏹️  Остановка старых контейнеров..."
docker-compose -f docker-compose.prod.yml down --remove-orphans 2>/dev/null || true

# Сборка образов
echo "🔨 Сборка образов..."
docker-compose -f docker-compose.prod.yml build

# Запуск
echo "🚀 Запуск сервисов..."
docker-compose -f docker-compose.prod.yml up -d

# Ожидание запуска
echo "⏳ Ожидание запуска сервисов..."
sleep 10

# Проверка статуса
echo ""
echo "📊 Статус контейнеров:"
docker-compose -f docker-compose.prod.yml ps

echo ""
echo "✅ Деплой завершён!"
echo ""
echo "🌐 Игра доступна по адресу:"
echo "   https://$DOMAIN"
echo ""
echo "📝 Полезные команды:"
echo "   Логи (все):   docker-compose -f docker-compose.prod.yml logs -f"
echo "   Логи backend: docker-compose -f docker-compose.prod.yml logs -f backend"
echo "   Статус:       docker-compose -f docker-compose.prod.yml ps"
echo "   Стоп:         docker-compose -f docker-compose.prod.yml down"

