#!/bin/bash

# Setup server-side cron job with 7-day retention
# Run this on the Dokploy server: ssh root@31.97.62.205 'bash -s' < server_cron_setup.sh

echo "🔄 Setting up Quantum Digital server backup cron job..."
echo "Schedule: Daily at 2:00 AM with 7-day retention"

# Updated cron job with 7-day retention
CRON_JOB="0 2 * * * docker exec quantumdigitalproject-quantumdigital-ndmwqy-web-1 python manage.py production_backup --cleanup --days=7 > /var/log/quantum_digital_backup.log 2>&1"

# Check if cron job exists
if crontab -l 2>/dev/null | grep -q "quantum"; then
    echo "⚠️  Existing Quantum Digital cron job found:"
    crontab -l | grep quantum
    echo ""
    echo "Updating to 7-day retention..."
    
    # Remove old quantum cron jobs
    crontab -l | grep -v quantum | crontab -
fi

# Add new cron job with 7-day retention
(crontab -l 2>/dev/null; echo "# Quantum Digital automated backup - runs daily at 2 AM with 7-day retention") | crontab -
(crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -

echo "✅ Server cron job updated!"
echo ""
echo "📋 Current server crontab:"
crontab -l | grep -A1 -B1 quantum
echo ""
echo "📊 Configuration:"
echo "  Server backup: Daily at 2:00 AM"
echo "  Local download: Daily at 3:00 AM"
echo "  Retention: 7 days (both server and local)"
echo "  Server log: /var/log/quantum_digital_backup.log"