#!/bin/bash

# 🔄 Manual Database Backup Script
# Usage: ./scripts/manual-backup.sh

set -e

# Configuration
DB_HOST="69.62.81.168"
DB_PORT="5432"
DB_USER="quantum_user"
DB_PASSWORD="7e9f4e144881879c"
DB_NAME="postgres"

# Generate timestamp
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="quantum-digital-manual-backup-${TIMESTAMP}.sql"
BACKUP_DIR="./backups"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔄 Starting manual database backup...${NC}"

# Create backups directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# Check if pg_dump is available
if ! command -v pg_dump &> /dev/null; then
    echo -e "${RED}❌ Error: pg_dump not found. Please install PostgreSQL client tools.${NC}"
    echo -e "${YELLOW}Install with: sudo apt-get install postgresql-client${NC}"
    exit 1
fi

# Test database connection
echo -e "${BLUE}🔍 Testing database connection...${NC}"
PGPASSWORD="$DB_PASSWORD" pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME"

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Error: Cannot connect to database${NC}"
    echo -e "${YELLOW}Check your database credentials and network connectivity${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Database connection successful${NC}"

# Create backup
echo -e "${BLUE}💾 Creating backup: $BACKUP_FILE${NC}"
PGPASSWORD="$DB_PASSWORD" pg_dump \
    -h "$DB_HOST" \
    -p "$DB_PORT" \
    -U "$DB_USER" \
    -d "$DB_NAME" \
    -f "$BACKUP_DIR/$BACKUP_FILE" \
    --verbose

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Backup created successfully!${NC}"
    
    # Get file size
    BACKUP_SIZE=$(du -h "$BACKUP_DIR/$BACKUP_FILE" | cut -f1)
    echo -e "${BLUE}📊 Backup size: $BACKUP_SIZE${NC}"
    
    # Create checksum
    cd "$BACKUP_DIR"
    sha256sum "$BACKUP_FILE" > "${BACKUP_FILE}.sha256"
    echo -e "${BLUE}🔐 Checksum created: ${BACKUP_FILE}.sha256${NC}"
    cd ..
    
    # Compress backup
    echo -e "${BLUE}🗜️ Compressing backup...${NC}"
    gzip "$BACKUP_DIR/$BACKUP_FILE"
    COMPRESSED_SIZE=$(du -h "$BACKUP_DIR/${BACKUP_FILE}.gz" | cut -f1)
    echo -e "${GREEN}✅ Compressed size: $COMPRESSED_SIZE${NC}"
    
    echo -e "${GREEN}🎉 Backup completed successfully!${NC}"
    echo -e "${BLUE}📁 Location: $BACKUP_DIR/${BACKUP_FILE}.gz${NC}"
    echo -e "${BLUE}🔐 Checksum: $BACKUP_DIR/${BACKUP_FILE}.sha256${NC}"
    
    # Show restore command
    echo ""
    echo -e "${YELLOW}📋 To restore this backup:${NC}"
    echo -e "${YELLOW}   gunzip $BACKUP_DIR/${BACKUP_FILE}.gz${NC}"
    echo -e "${YELLOW}   psql -h HOST -U USER -d DATABASE < $BACKUP_DIR/$BACKUP_FILE${NC}"
    
else
    echo -e "${RED}❌ Backup failed!${NC}"
    exit 1
fi

# List recent backups
echo ""
echo -e "${BLUE}📚 Recent backups in $BACKUP_DIR:${NC}"
ls -lah "$BACKUP_DIR"/*.gz 2>/dev/null | tail -5 || echo -e "${YELLOW}No previous backups found${NC}"

echo ""
echo -e "${GREEN}✨ Manual backup complete!${NC}"