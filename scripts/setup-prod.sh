#!/bin/bash
# Production environment setup script

set -e

echo "🚀 Setting up Vanishing Tic-Tac-Toe production environment..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if .env.prod exists
if [ ! -f .env.prod ]; then
    echo "❌ .env.prod file not found!"
    echo "Please copy env.prod.example to .env.prod and configure it:"
    echo "   cp env.prod.example .env.prod"
    echo "   nano .env.prod"
    exit 1
fi

echo "✅ .env.prod found"

# Create web network if it doesn't exist
if ! docker network ls | grep -q "web"; then
    echo "📡 Creating Docker network 'web'..."
    docker network create web
    echo "✅ Network created"
else
    echo "✅ Docker network 'web' already exists"
fi

# Setup acme.json for SSL certificates
if [ ! -f traefik/acme.json ]; then
    echo "🔐 Creating traefik/acme.json for SSL certificates..."
    touch traefik/acme.json
    chmod 600 traefik/acme.json
    echo "✅ Created traefik/acme.json"
else
    echo "✅ traefik/acme.json already exists"
    chmod 600 traefik/acme.json
fi

# Check if Let's Encrypt email is set
source .env.prod
if [ -z "$LETSENCRYPT_EMAIL" ]; then
    echo "⚠️  WARNING: LETSENCRYPT_EMAIL not set in .env.prod"
    echo "SSL certificates may not be obtained automatically."
fi

if [ -z "$DOMAIN" ]; then
    echo "❌ DOMAIN not set in .env.prod"
    exit 1
fi

echo "✅ Domain configured: $DOMAIN"

# Build and start containers
echo "🏗️  Building Docker images..."
docker-compose -f docker-compose.prod.yml --env-file .env.prod build

echo "🚀 Starting production services..."
docker-compose -f docker-compose.prod.yml --env-file .env.prod up -d

echo ""
echo "✅ Production environment is running!"
echo ""
echo "📍 Access points:"
echo "   - Application: https://$DOMAIN"
echo "   - Traefik Dashboard: https://traefik.$DOMAIN"
echo ""
echo "📊 View logs:"
echo "   docker-compose -f docker-compose.prod.yml logs -f"
echo ""
echo "🔍 Check status:"
echo "   docker ps"
echo ""
echo "⚠️  Important:"
echo "   - Make sure your DNS A records point to this server"
echo "   - Ports 80 and 443 must be accessible from the internet"
echo "   - SSL certificates may take a few minutes to generate"
echo "   - Check DNS: nslookup $DOMAIN"

