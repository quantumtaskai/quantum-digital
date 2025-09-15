from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.utils import timezone
from django.conf import settings
import os
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Production backup solution compatible with Dokploy environment'

    def add_arguments(self, parser):
        parser.add_argument(
            '--cleanup',
            action='store_true',
            help='Also cleanup old backup files'
        )
        parser.add_argument(
            '--days',
            type=int,
            default=30,
            help='Number of days to keep backups (default: 30)'
        )

    def handle(self, *args, **options):
        """
        Perform production backup using Django's dumpdata
        This works in environments where pg_dump is not available
        """
        timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f'quantum_digital_backup_{timestamp}.json'
        
        self.stdout.write('🔄 Starting production database backup...')
        
        try:
            # Create Django JSON backup (works everywhere)
            self.stdout.write('📦 Creating Django JSON backup...')
            
            with open(backup_filename, 'w') as backup_file:
                call_command(
                    'dumpdata',
                    '--indent=2',
                    '--natural-foreign',
                    '--natural-primary',
                    stdout=backup_file
                )
            
            # Check backup file size
            backup_size = os.path.getsize(backup_filename)
            backup_size_mb = backup_size / (1024 * 1024)
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'✅ Backup completed: {backup_filename} ({backup_size_mb:.1f} MB)'
                )
            )
            
            # Cleanup old backups if requested
            if options['cleanup']:
                self._cleanup_old_backups(options['days'])
            
            # Log success
            logger.info(f'Production backup completed: {backup_filename} ({backup_size_mb:.1f} MB)')
            
            # Print backup instructions
            self.stdout.write('')
            self.stdout.write('📋 BACKUP INFORMATION:')
            self.stdout.write(f'  File: {backup_filename}')
            self.stdout.write(f'  Size: {backup_size_mb:.1f} MB')
            self.stdout.write(f'  Records: Django JSON format with all data')
            self.stdout.write('')
            self.stdout.write('🔄 RESTORE INSTRUCTIONS:')
            self.stdout.write(f'  python manage.py loaddata {backup_filename}')
            self.stdout.write('')
            self.stdout.write('📝 BACKUP CONTAINS:')
            self.stdout.write('  - All Quantum Digital brand profiles')
            self.stdout.write('  - Platform progress data')
            self.stdout.write('  - User accounts and authentication')
            self.stdout.write('  - Site configuration and OAuth settings')
            self.stdout.write('')
            
        except Exception as e:
            error_msg = f'Production backup failed: {e}'
            logger.error(error_msg)
            self.stdout.write(self.style.ERROR(f'❌ {error_msg}'))
            raise

    def _cleanup_old_backups(self, days_to_keep):
        """Remove backup files older than specified days"""
        self.stdout.write(f'🧹 Cleaning up backups older than {days_to_keep} days...')
        
        import glob
        import time
        
        # Find all backup files
        backup_files = glob.glob('quantum_digital_backup_*.json')
        current_time = time.time()
        removed_count = 0
        
        for backup_file in backup_files:
            file_age_days = (current_time - os.path.getmtime(backup_file)) / (24 * 3600)
            
            if file_age_days > days_to_keep:
                try:
                    os.remove(backup_file)
                    removed_count += 1
                    self.stdout.write(f'  Removed: {backup_file}')
                except Exception as e:
                    self.stdout.write(
                        self.style.WARNING(f'  Failed to remove {backup_file}: {e}')
                    )
        
        if removed_count > 0:
            self.stdout.write(
                self.style.SUCCESS(f'✅ Cleaned up {removed_count} old backup files')
            )
        else:
            self.stdout.write('ℹ️  No old backup files to clean up')