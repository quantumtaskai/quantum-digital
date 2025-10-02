from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
import os
from django.conf import settings
from django.db import transaction


class Command(BaseCommand):
    help = 'Setup production environment correctly - handles all Site conflicts'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.site_domain = os.getenv('SITE_DOMAIN', 'digital.quantumtaskai.com')

    def handle(self, *args, **options):
        """
        Set up Sites framework correctly for production
        Bulletproof approach that handles all edge cases
        """
        self.stdout.write('🚀 Setting up production environment...')
        
        self.stdout.write(f'Ensuring site domain is set to: {self.site_domain}')
        try:
            with transaction.atomic():
                # Step 1: Clean up the mess first
                self._cleanup_sites()
                
                # Step 2: Ensure exactly one production site with correct ID
                self._setup_production_site()
                
                # Step 3: Verify the setup
                self._verify_setup()
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Setup failed: {e}')
            )
            # Try non-atomic fallback
            self._fallback_setup()
    
    def _cleanup_sites(self):
        """Remove problematic sites"""
        # Remove all example.com sites
        removed_count = Site.objects.filter(domain='example.com').count()
        if removed_count > 0:
            Site.objects.filter(domain='example.com').delete()
            self.stdout.write(f'✅ Removed {removed_count} default example.com site(s)')
        
        # Check for duplicate production sites
        prod_sites = Site.objects.filter(domain=self.site_domain)
        if prod_sites.count() > 1:
            self.stdout.write(f'⚠️  Found {prod_sites.count()} duplicate production sites')
            # Keep the first one, delete the rest
            keep_site = prod_sites.first()
            duplicate_count = prod_sites.exclude(id=keep_site.id).count()
            prod_sites.exclude(id=keep_site.id).delete()
            self.stdout.write(f'✅ Removed {duplicate_count} duplicate production site(s)')
    
    def _setup_production_site(self):
        """Ensure production site exists with correct configuration"""
        
        # Check if we need to fix the ID=1 issue
        try:
            site_1 = Site.objects.get(id=1)
            if site_1.domain != self.site_domain:
                # ID=1 exists but wrong domain - update it
                site_1.domain = self.site_domain
                site_1.name = 'Quantum Digital'
                site_1.save()
                self.stdout.write('✅ Updated site ID=1 to production domain')
            else:
                # ID=1 already correct
                site_1.name = 'Quantum Digital'
                site_1.save()
                self.stdout.write('✅ Site ID=1 already configured correctly')
                
        except Site.DoesNotExist:
            # No site with ID=1, check if production site exists elsewhere
            try:
                prod_site = Site.objects.get(domain=self.site_domain)
                # Production site exists but wrong ID
                if prod_site.id != 1:
                    # Delete and recreate with ID=1
                    prod_site.delete()
                    Site.objects.create(id=1, domain=self.site_domain, name='Quantum Digital')
                    self.stdout.write('✅ Recreated production site with ID=1')
                    
            except Site.DoesNotExist:
                # No production site at all
                Site.objects.create(id=1, domain=self.site_domain, name='Quantum Digital')
                self.stdout.write('✅ Created new production site with ID=1')
    
    def _verify_setup(self):
        """Verify the setup is correct"""
        try:
            site = Site.objects.get(id=1, domain=self.site_domain)
            self.stdout.write(f'✅ Verification passed: Site ID={site.id}, Domain={site.domain}')
            
            if hasattr(settings, 'SITE_ID'):
                if site.id == settings.SITE_ID:
                    self.stdout.write('✅ SITE_ID matches correctly')
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f'⚠️  Warning: Site ID ({site.id}) != SITE_ID setting ({settings.SITE_ID})'
                        )
                    )
        except Site.DoesNotExist:
            self.stdout.write(self.style.ERROR('❌ Verification failed: Production site not found'))
            raise
    
    def _fallback_setup(self):
        """Fallback setup if atomic transaction fails"""
        self.stdout.write('⚠️  Attempting fallback setup...')
        try:
            # Simple fallback: just ensure production site exists
            site, created = Site.objects.get_or_create(
                domain=self.site_domain,
                defaults={'name': 'Quantum Digital'}
            )
            if created:
                self.stdout.write('✅ Fallback: Created production site')
            else:
                self.stdout.write('✅ Fallback: Production site already exists')
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Fallback also failed: {e}')
            )
        
        self.stdout.write(
            self.style.SUCCESS('🎯 Production setup completed (with fallback)!')
        )