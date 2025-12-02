#!/bin/bash
# Health check script for monitoring deployment

set -e

BACKEND_URL="${BACKEND_URL:-http://localhost:8000}"
FRONTEND_URL="${FRONTEND_URL:-http://localhost:3000}"

echo "🏥 Running health checks..."

# Check backend
echo -n "Backend API... "
if curl -f -s "${BACKEND_URL}/api/health" > /dev/null; then
    echo "✅ OK"
else
    echo "❌ FAILED"
    exit 1
fi

# Check frontend
echo -n "Frontend... "
if curl -f -s "${FRONTEND_URL}" > /dev/null; then
    echo "✅ OK"
else
    echo "❌ FAILED"
    exit 1
fi

# Check WebSocket (basic connectivity)
echo -n "WebSocket endpoint... "
if curl -f -s -I "${BACKEND_URL}/ws/test" 2>&1 | grep -q "426\|400\|101"; then
    echo "✅ OK (endpoint exists)"
else
    echo "⚠️  Warning: WebSocket endpoint check failed"
fi

echo ""
echo "✅ All health checks passed!"

