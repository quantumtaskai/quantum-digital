from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Perform daily database backup and cleanup old backups'

    def add_arguments(self, parser):
        parser.add_argument(
            '--cleanup',
            action='store_true',
            help='Also cleanup old backup files'
        )

    def handle(self, *args, **options):
        """
        Perform daily database backup with optional cleanup
        """
        self.stdout.write('🔄 Starting daily database backup...')
        
        try:
            # Perform database backup
            self.stdout.write('📦 Creating database backup...')
            call_command('dbbackup', verbosity=1)
            self.stdout.write(self.style.SUCCESS('✅ Database backup completed'))
            
            # Perform media backup if needed
            try:
                self.stdout.write('📁 Creating media backup...')
                call_command('mediabackup', verbosity=1)
                self.stdout.write(self.style.SUCCESS('✅ Media backup completed'))
            except Exception as e:
                # Media backup is optional
                self.stdout.write(
                    self.style.WARNING(f'⚠️  Media backup skipped: {e}')
                )
            
            # Cleanup old backups if requested
            if options['cleanup']:
                self.stdout.write('🧹 Cleaning up old backups...')
                try:
                    call_command('dbbackup', '--clean', verbosity=1)
                    self.stdout.write(self.style.SUCCESS('✅ Backup cleanup completed'))
                except Exception as e:
                    self.stdout.write(
                        self.style.WARNING(f'⚠️  Cleanup failed: {e}')
                    )
            
            # Log success
            timestamp = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
            logger.info(f'Daily backup completed successfully at {timestamp}')
            
            self.stdout.write(
                self.style.SUCCESS('🎉 Daily backup process completed successfully!')
            )
            
        except Exception as e:
            error_msg = f'Daily backup failed: {e}'
            logger.error(error_msg)
            self.stdout.write(
                self.style.ERROR(f'❌ {error_msg}')
            )
            raise