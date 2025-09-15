#!/bin/bash

# Quick Quantum Digital Backup Download
# Downloads latest backup to /mnt/sdd2/projects_db_backup/quantum_digital

BACKUP_DIR="/mnt/sdd2/projects_db_backup/quantum_digital"
SERVER="root@31.97.62.205"
CONTAINER="quantumdigitalproject-quantumdigital-ndmwqy-web-1"

echo "🔄 Quick Quantum Digital Backup"
echo "Downloading to: $BACKUP_DIR"

# Create backup on server and download
ssh $SERVER "docker exec $CONTAINER python manage.py production_backup && \
             docker cp $CONTAINER:/app/quantum_digital_backup_\$(date +%Y%m%d)*.json /root/ && \
             ls -la /root/quantum_digital_backup_*.json | tail -1"

# Download latest backup
LATEST_BACKUP=$(ssh $SERVER "ls -1t /root/quantum_digital_backup_*.json | head -1")
scp $SERVER:"$LATEST_BACKUP" "$BACKUP_DIR/"

echo "✅ Backup downloaded to: $BACKUP_DIR/$(basename $LATEST_BACKUP)"
ls -lh "$BACKUP_DIR"/$(basename $LATEST_BACKUP)