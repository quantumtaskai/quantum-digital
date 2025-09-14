# Generated to ensure proper Site setup without conflicts
from django.db import migrations
from django.contrib.sites.models import Site
from django.db import IntegrityError


def setup_site_safely(apps, schema_editor):
    """
    Safely set up the Site object for production
    """
    db_alias = schema_editor.connection.alias
    
    try:
        # Remove any existing example.com sites
        Site.objects.using(db_alias).filter(domain='example.com').delete()
    except:
        pass  # Ignore if it doesn't exist
    
    try:
        # Try to get or create the production site
        site, created = Site.objects.using(db_alias).get_or_create(
            domain='digital.quantumtaskai.com',
            defaults={'name': 'Quantum Digital'}
        )
        if not created and site.name != 'Quantum Digital':
            site.name = 'Quantum Digital'
            site.save()
    except IntegrityError:
        # If there's still a conflict, just update the existing one
        try:
            site = Site.objects.using(db_alias).get(domain='digital.quantumtaskai.com')
            site.name = 'Quantum Digital'
            site.save()
        except:
            pass  # If all else fails, continue - the site exists


def reverse_setup_site(apps, schema_editor):
    """
    Reverse the site setup - restore default
    """
    pass  # We don't want to break production by reversing


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_alter_clientplatformprogress_platform'),
        ('sites', '0002_alter_domain_unique'),
    ]

    operations = [
        migrations.RunPython(setup_site_safely, reverse_setup_site),
    ]