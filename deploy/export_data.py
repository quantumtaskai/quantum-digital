#!/usr/bin/env python
"""
Export data from Django app for migration to DigitalOcean
Run this script on your current Render deployment
"""

import os
import django
import sys
from datetime import datetime

# Add the project directory to Python path
sys.path.append('/opt/render/project/src')

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quantum_digital.settings')
django.setup()

from django.core.management import call_command
from django.contrib.auth.models import User

def export_data():
    """Export all app data to JSON file"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'backup_{timestamp}.json'
    
    print(f"Exporting data to {filename}...")
    
    # Export all data except contenttypes and sessions
    with open(filename, 'w') as f:
        call_command('dumpdata', 
                    '--natural-foreign', 
                    '--natural-primary',
                    '--exclude=contenttypes',
                    '--exclude=sessions',
                    '--exclude=admin.logentry',
                    stdout=f)
    
    print(f"✅ Data exported successfully to {filename}")
    
    # Show summary
    user_count = User.objects.count()
    print(f"📊 Summary:")
    print(f"   - Users: {user_count}")
    
    return filename

if __name__ == '__main__':
    export_data()