#!/bin/bash
# Backup script for production data

set -e

BACKUP_DIR="backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_PATH="$BACKUP_DIR/backup_$TIMESTAMP"

echo "📦 Creating backup at $BACKUP_PATH..."

# Create backup directory
mkdir -p "$BACKUP_PATH"

# Backup Traefik SSL certificates
if [ -f traefik/acme.json ]; then
    echo "🔐 Backing up SSL certificates..."
    cp traefik/acme.json "$BACKUP_PATH/acme.json"
fi

# Backup environment files (without sensitive data exposed in logs)
if [ -f .env.prod ]; then
    echo "⚙️  Backing up configuration..."
    cp .env.prod "$BACKUP_PATH/.env.prod"
fi

# If you add PostgreSQL later, backup database:
# echo "💾 Backing up database..."
# docker exec postgres pg_dump -U $DB_USER $DB_NAME > "$BACKUP_PATH/database.sql"

# Create archive
cd "$BACKUP_DIR"
tar -czf "backup_$TIMESTAMP.tar.gz" "backup_$TIMESTAMP"
rm -rf "backup_$TIMESTAMP"

echo "✅ Backup created: $BACKUP_DIR/backup_$TIMESTAMP.tar.gz"

# Keep only last 7 backups
echo "🧹 Cleaning old backups..."
ls -t backup_*.tar.gz | tail -n +8 | xargs -r rm

echo "✅ Backup complete!"

