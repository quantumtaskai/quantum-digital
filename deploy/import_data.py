#!/usr/bin/env python
"""
Import data to Django app on DigitalOcean
Run this after successful deployment
"""

import os
import django
import sys
from pathlib import Path

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quantum_digital.settings')
django.setup()

from django.core.management import call_command
from django.contrib.auth.models import User

def import_data(backup_file='backup.json'):
    """Import data from JSON backup file"""
    
    if not Path(backup_file).exists():
        print(f"❌ Backup file {backup_file} not found!")
        return False
    
    print(f"Importing data from {backup_file}...")
    
    try:
        # Run migrations first
        print("🔄 Running migrations...")
        call_command('migrate')
        
        # Load data
        print("📥 Loading data...")
        call_command('loaddata', backup_file)
        
        # Show summary
        user_count = User.objects.count()
        print(f"✅ Import completed successfully!")
        print(f"📊 Summary:")
        print(f"   - Users: {user_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Import failed: {str(e)}")
        return False

if __name__ == '__main__':
    import sys
    backup_file = sys.argv[1] if len(sys.argv) > 1 else 'backup.json'
    import_data(backup_file)