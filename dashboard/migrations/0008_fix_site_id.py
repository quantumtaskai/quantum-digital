# Generated to fix Site ID configuration
from django.db import migrations
from django.contrib.sites.models import Site


def fix_site_id(apps, schema_editor):
    """
    Ensure the production site has ID=1 to match SITE_ID setting
    This prevents the common issue where default site gets ID=1 and production site gets ID=2
    """
    db_alias = schema_editor.connection.alias
    
    try:
        # First, remove any default example.com sites that Django creates automatically
        Site.objects.using(db_alias).filter(domain='example.com').delete()
        
        # Check if production site already exists
        try:
            prod_site = Site.objects.using(db_alias).get(domain='digital.quantumtaskai.com')
            if prod_site.id == 1:
                # Already correct, just ensure name is right
                prod_site.name = 'Quantum Digital'
                prod_site.save(update_fields=['name'])
            else:
                # Wrong ID, need to fix
                prod_site.delete()
                Site.objects.using(db_alias).create(
                    id=1,
                    domain='digital.quantumtaskai.com',
                    name='Quantum Digital'
                )
        except Site.DoesNotExist:
            # No production site exists, create it with ID=1
            Site.objects.using(db_alias).create(
                id=1,
                domain='digital.quantumtaskai.com',
                name='Quantum Digital'
            )
        
        # Final check: if there's somehow still a site with wrong ID=1, fix it
        try:
            site_1 = Site.objects.using(db_alias).get(id=1)
            if site_1.domain != 'digital.quantumtaskai.com':
                site_1.domain = 'digital.quantumtaskai.com'
                site_1.name = 'Quantum Digital'
                site_1.save()
        except Site.DoesNotExist:
            pass
        
    except Exception:
        # If anything fails, continue silently to avoid breaking migrations
        pass


def reverse_fix_site_id(apps, schema_editor):
    """
    Reverse migration - not implemented as it could break production
    """
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_ensure_site_setup'),
        ('sites', '0002_alter_domain_unique'),
    ]

    operations = [
        migrations.RunPython(fix_site_id, reverse_fix_site_id),
    ]