from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp
from allauth.socialaccount import providers


class Command(BaseCommand):
    help = 'Fix Google OAuth configuration for production'

    def handle(self, *args, **options):
        """
        Debug and fix Google OAuth configuration
        """
        self.stdout.write('🔍 Diagnosing Google OAuth configuration...')
        
        # Check current site
        current_site = Site.objects.get_current()
        self.stdout.write(f'Current site: {current_site.domain} (ID: {current_site.id})')
        
        # Check all sites
        all_sites = Site.objects.all()
        self.stdout.write(f'All sites in database:')
        for site in all_sites:
            self.stdout.write(f'  - Site ID: {site.id}, Domain: {site.domain}, Name: {site.name}')
        
        # Check social apps
        self.stdout.write('\n🔑 Social Apps configuration:')
        google_apps = SocialApp.objects.filter(provider='google')
        
        if not google_apps.exists():
            self.stdout.write(self.style.ERROR('❌ No Google OAuth apps found'))
            return
            
        for app in google_apps:
            self.stdout.write(f'Provider: {app.provider}')
            self.stdout.write(f'Name: {app.name}')
            self.stdout.write(f'Client ID: {app.client_id}')
            self.stdout.write(f'Has Secret: {bool(app.secret)}')
            
            app_sites = app.sites.all()
            self.stdout.write(f'Associated sites: {[s.domain for s in app_sites]}')
            
            # Check if current site is associated
            if current_site in app_sites:
                self.stdout.write(self.style.SUCCESS('✅ Current site is associated with OAuth app'))
            else:
                self.stdout.write(self.style.ERROR('❌ Current site NOT associated with OAuth app'))
                self.stdout.write('🔧 Fixing association...')
                app.sites.add(current_site)
                self.stdout.write(self.style.SUCCESS('✅ Associated current site with OAuth app'))
        
        # Test provider detection
        self.stdout.write('\n🧪 Testing provider detection...')
        try:
            from allauth.socialaccount.templatetags.socialaccount import get_providers
            from django.template import Context, RequestContext
            from django.test import RequestFactory
            from django.contrib.auth.models import AnonymousUser
            
            # Create a mock request with proper attributes
            request = RequestFactory().get('/')
            request.site = current_site
            request.user = AnonymousUser()
            request.session = {}
            
            # Try to get providers (this is what template does)
            context = RequestContext(request, {'request': request})
            provider_list = get_providers(context)
            
            self.stdout.write(f'Providers detected: {len(provider_list)}')
            for provider in provider_list:
                self.stdout.write(f'  - {provider.id}: {provider.name}')
                
            if not provider_list:
                self.stdout.write(self.style.WARNING('⚠️  No providers detected in template context'))
                
                # Additional debugging
                self.stdout.write('\n🔍 Additional debugging:')
                from allauth.socialaccount import providers as provider_registry
                
                # Check if providers are registered
                try:
                    google_provider = provider_registry.registry.by_id('google')
                    self.stdout.write(f'Google provider class: {google_provider}')
                except:
                    self.stdout.write('❌ Google provider not registered')
                
                # Check apps for current request context
                apps = SocialApp.objects.filter(sites=current_site)
                self.stdout.write(f'Apps for current site: {apps.count()}')
                
            else:
                self.stdout.write(self.style.SUCCESS('✅ Providers successfully detected'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Provider detection failed: {e}'))
        
        # Verify OAuth URLs
        self.stdout.write('\n🌐 OAuth URLs:')
        from django.urls import reverse
        try:
            google_login_url = reverse('google_login')  
            self.stdout.write(f'Google login URL: {google_login_url}')
        except:
            try:
                from allauth.socialaccount.providers.google.urls import urlpatterns
                self.stdout.write('Google URLs are registered via allauth')
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'❌ Google URL registration issue: {e}'))
        
        self.stdout.write('\n✅ OAuth diagnosis complete!')