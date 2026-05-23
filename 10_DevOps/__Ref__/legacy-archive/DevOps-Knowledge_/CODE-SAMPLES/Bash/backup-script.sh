#!/bin/bash

###############################################################################
# Backup Script
# Description: Automated backup script for files and databases
###############################################################################

# Configuration
BACKUP_DIR="/backup"
SOURCE_DIR="/var/www"
DB_NAME="myapp"
DB_USER="backup_user"
RETENTION_DAYS=7
DATE=$(date +%Y%m%d_%H%M%S)

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check if backup directory exists
if [ ! -d "$BACKUP_DIR" ]; then
    log_info "Creating backup directory: $BACKUP_DIR"
    mkdir -p "$BACKUP_DIR"
fi

# Backup files
log_info "Starting file backup..."
BACKUP_FILE="$BACKUP_DIR/files_backup_$DATE.tar.gz"

if tar -czf "$BACKUP_FILE" "$SOURCE_DIR" 2>/dev/null; then
    log_info "File backup completed: $BACKUP_FILE"
else
    log_error "File backup failed!"
    exit 1
fi

# Backup database
log_info "Starting database backup..."
DB_BACKUP_FILE="$BACKUP_DIR/db_backup_$DATE.sql.gz"

if mysqldump -u "$DB_USER" "$DB_NAME" | gzip > "$DB_BACKUP_FILE" 2>/dev/null; then
    log_info "Database backup completed: $DB_BACKUP_FILE"
else
    log_error "Database backup failed!"
    exit 1
fi

# Remove old backups
log_info "Removing backups older than $RETENTION_DAYS days..."
find "$BACKUP_DIR" -name "*.tar.gz" -mtime +$RETENTION_DAYS -delete
find "$BACKUP_DIR" -name "*.sql.gz" -mtime +$RETENTION_DAYS -delete

# Calculate backup size
TOTAL_SIZE=$(du -sh "$BACKUP_DIR" | cut -f1)
log_info "Total backup size: $TOTAL_SIZE"

log_info "Backup completed successfully!"
