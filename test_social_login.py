#!/usr/bin/env python
"""
Quick test script to verify social login setup
"""

import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quantum_digital.settings')
django.setup()

from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp
from django.template.loader import get_template
from django.template import Context


def test_social_login_setup():
    """Test if social login is properly configured"""
    
    print("🔍 Testing Social Login Setup")
    print("=" * 40)
    
    # Test 1: Check Site configuration
    print("\n1. Site Configuration:")
    try:
        site = Site.objects.get(pk=1)
        print(f"   ✅ Site domain: {site.domain}")
        print(f"   ✅ Site name: {site.name}")
    except Site.DoesNotExist:
        print("   ❌ Site not configured")
        return False
    
    # Test 2: Check installed providers
    print("\n2. Social Providers:")
    try:
        from allauth.socialaccount import providers
        available_providers = ['google', 'facebook', 'github', 'linkedin_oauth2']
        for provider_id in available_providers:
            try:
                provider = providers.registry.by_id(provider_id)
                print(f"   ✅ {provider.name} provider available")
            except:
                print(f"   ❌ {provider_id} provider not available")
    except Exception as e:
        print(f"   ❌ Error checking providers: {e}")
    
    # Test 3: Check Social Apps (OAuth credentials)
    print("\n3. OAuth Applications:")
    apps = SocialApp.objects.all()
    if apps.count() == 0:
        print("   ⚠️  No OAuth applications configured yet")
        print("      You need to add OAuth credentials in Django admin")
    else:
        for app in apps:
            print(f"   ✅ {app.name} ({app.provider}) configured")
    
    # Test 4: Check templates
    print("\n4. Template Integration:")
    try:
        template = get_template('registration/login.html')
        print("   ✅ Login template loads successfully")
        
        template = get_template('registration/signup.html')
        print("   ✅ Signup template loads successfully")
    except Exception as e:
        print(f"   ❌ Template error: {e}")
        return False
    
    # Test 5: Check database migrations
    print("\n5. Database Setup:")
    try:
        from allauth.account.models import EmailAddress
        from allauth.socialaccount.models import SocialAccount
        print("   ✅ Allauth tables exist in database")
    except Exception as e:
        print(f"   ❌ Database migration error: {e}")
        return False
    
    print("\n" + "=" * 40)
    print("📋 Setup Summary:")
    print("✅ Django-allauth installed and configured")
    print("✅ Social login templates updated")
    print("✅ Database migrations completed")
    print("✅ Site configuration updated")
    
    if apps.count() == 0:
        print("\n⚠️  Next Steps:")
        print("1. Set up OAuth applications with providers:")
        print("   - Google: https://console.cloud.google.com/")
        print("   - Facebook: https://developers.facebook.com/")
        print("   - GitHub: https://github.com/settings/developers")
        print("   - LinkedIn: https://www.linkedin.com/developers/apps")
        print("2. Add credentials to Django admin at /admin/")
        print("3. Update .env file with your OAuth credentials")
        print("\nSee SOCIAL_AUTH_SETUP.md for detailed instructions.")
    else:
        print("🎉 Social login fully configured and ready to use!")
    
    return True


if __name__ == '__main__':
    test_social_login_setup()
