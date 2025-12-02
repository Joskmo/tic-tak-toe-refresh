#!/bin/bash
# Development environment setup script

set -e

echo "🚀 Setting up Vanishing Tic-Tac-Toe development environment..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"

# Create .env file for frontend if it doesn't exist
if [ ! -f frontend/.env ]; then
    echo "📝 Creating frontend/.env file..."
    cat > frontend/.env << EOF
REACT_APP_WS_URL=localhost:8000
EOF
    echo "✅ Created frontend/.env"
else
    echo "✅ frontend/.env already exists"
fi

# Build and start containers
echo "🏗️  Building Docker images..."
docker-compose build

echo "🎮 Starting services..."
docker-compose up -d

echo ""
echo "✅ Development environment is ready!"
echo ""
echo "📍 Access points:"
echo "   - Frontend: http://localhost:3000"
echo "   - Backend:  http://localhost:8000"
echo "   - API Docs: http://localhost:8000/docs"
echo ""
echo "📊 View logs:"
echo "   docker-compose logs -f"
echo ""
echo "🛑 Stop services:"
echo "   docker-compose down"

