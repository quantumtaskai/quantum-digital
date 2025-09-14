from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from django.conf import settings


class Command(BaseCommand):
    help = 'Setup production environment correctly'

    def handle(self, *args, **options):
        """
        Set up Sites framework correctly for production
        """
        self.stdout.write('Setting up production environment...')
        
        # Remove default site if it exists
        default_sites = Site.objects.filter(domain='example.com')
        if default_sites.exists():
            default_sites.delete()
            self.stdout.write('✅ Removed default example.com site')
        
        # Ensure our production site exists
        site, created = Site.objects.get_or_create(
            domain='digital.quantumtaskai.com',
            defaults={
                'name': 'Quantum Digital',
            }
        )
        
        if created:
            self.stdout.write('✅ Created production site: digital.quantumtaskai.com')
        else:
            # Update existing site
            site.name = 'Quantum Digital'
            site.save()
            self.stdout.write('✅ Updated production site: digital.quantumtaskai.com')
        
        # Ensure SITE_ID is correct
        if hasattr(settings, 'SITE_ID'):
            self.stdout.write(f'✅ SITE_ID configured: {settings.SITE_ID}')
            if site.id != settings.SITE_ID:
                self.stdout.write(
                    self.style.WARNING(
                        f'⚠️  Warning: Site ID ({site.id}) != SITE_ID setting ({settings.SITE_ID})'
                    )
                )
        
        self.stdout.write(
            self.style.SUCCESS('✅ Production setup completed successfully!')
        )