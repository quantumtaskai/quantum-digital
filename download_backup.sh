#!/bin/bash

# Quantum Digital Backup Download Script
# Usage: ./download_backup.sh [latest|all|YYYYMMDD]

SERVER="root@31.97.62.205"
CONTAINER="quantumdigitalproject-quantumdigital-ndmwqy-web-1"
BACKUP_DIR="/root/quantum_digital_backups"
LOCAL_BACKUP_DIR="/mnt/sdd2/projects_db_backup/quantum_digital"

# Create local backup directory if it doesn't exist
mkdir -p "$LOCAL_BACKUP_DIR"

echo "🔄 Quantum Digital Backup Download Tool"
echo "========================================"

# Create backup directory on server if it doesn't exist
ssh $SERVER "mkdir -p $BACKUP_DIR"

case "${1:-latest}" in
    "latest")
        echo "📦 Creating fresh backup and downloading latest..."
        
        # Create new backup
        ssh $SERVER "docker exec $CONTAINER python manage.py production_backup"
        
        # Copy backup from container to host
        BACKUP_FILE=$(ssh $SERVER "docker exec $CONTAINER ls -1t quantum_digital_backup_*.json | head -1")
        ssh $SERVER "docker cp $CONTAINER:/app/$BACKUP_FILE $BACKUP_DIR/"
        
        # Download to local backup directory
        scp $SERVER:$BACKUP_DIR/$BACKUP_FILE "$LOCAL_BACKUP_DIR/"
        
        echo "✅ Downloaded: $BACKUP_FILE"
        echo "📊 File info:"
        ls -lh "$LOCAL_BACKUP_DIR/$BACKUP_FILE"
        echo "📁 Saved to: $LOCAL_BACKUP_DIR/$BACKUP_FILE"
        ;;
        
    "all")
        echo "📦 Downloading all available backups..."
        
        # Download all backups from server
        scp $SERVER:$BACKUP_DIR/quantum_digital_backup_*.json "$LOCAL_BACKUP_DIR/" 2>/dev/null || echo "ℹ️  No backups found on server"
        
        echo "✅ Downloaded backups:"
        ls -lh "$LOCAL_BACKUP_DIR"/quantum_digital_backup_*.json 2>/dev/null || echo "No backup files found"
        ;;
        
    *)
        # Download specific date (YYYYMMDD format)
        DATE=$1
        echo "📦 Downloading backup for date: $DATE"
        
        scp $SERVER:$BACKUP_DIR/quantum_digital_backup_${DATE}_*.json "$LOCAL_BACKUP_DIR/" 2>/dev/null || {
            echo "❌ No backup found for date $DATE"
            echo "Available backups:"
            ssh $SERVER "ls -1 $BACKUP_DIR/quantum_digital_backup_*.json 2>/dev/null | xargs -I {} basename {}" || echo "No backups available"
            exit 1
        }
        
        echo "✅ Downloaded backup for $DATE"
        ls -lh "$LOCAL_BACKUP_DIR"/quantum_digital_backup_${DATE}_*.json
        ;;
esac

echo ""
echo "📁 Backups saved to: $LOCAL_BACKUP_DIR"
echo ""
echo "🔄 To restore any backup:"
echo "python manage.py loaddata $LOCAL_BACKUP_DIR/quantum_digital_backup_YYYYMMDD_HHMMSS.json"
echo ""
echo "📝 Each backup contains:"
echo "  - All Quantum Digital brand profiles"
echo "  - Platform progress data"  
echo "  - User accounts and authentication"
echo "  - Site configuration and OAuth settings"
echo ""
echo "📊 View all backups:"
echo "ls -la $LOCAL_BACKUP_DIR"