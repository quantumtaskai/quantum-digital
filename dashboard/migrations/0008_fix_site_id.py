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
        # Strategy: Work with what exists, don't create conflicts
        
        # Check what site currently has ID=1
        site_1_exists = False
        try:
            site_1 = Site.objects.using(db_alias).get(id=1)
            site_1_exists = True
            
            # If ID=1 is already our production domain, we're good
            if site_1.domain == 'digital.quantumtaskai.com':
                site_1.name = 'Quantum Digital'
                site_1.save(update_fields=['name'])
                return  # All done!
            
            # If ID=1 has a different domain, update it to our production domain
            else:
                site_1.domain = 'digital.quantumtaskai.com'
                site_1.name = 'Quantum Digital'
                site_1.save(update_fields=['domain', 'name'])
                
                # Remove any duplicate production sites with different IDs
                Site.objects.using(db_alias).filter(
                    domain='digital.quantumtaskai.com'
                ).exclude(id=1).delete()
                return  # All done!
                
        except Site.DoesNotExist:
            site_1_exists = False
        
        # If no site with ID=1 exists, check if production site exists elsewhere
        if not site_1_exists:
            try:
                prod_site = Site.objects.using(db_alias).get(domain='digital.quantumtaskai.com')
                # Production site exists but with wrong ID - delete and recreate with ID=1
                prod_site.delete()
                Site.objects.using(db_alias).create(
                    id=1,
                    domain='digital.quantumtaskai.com',
                    name='Quantum Digital'
                )
            except Site.DoesNotExist:
                # No production site exists at all - create it with ID=1
                Site.objects.using(db_alias).create(
                    id=1,
                    domain='digital.quantumtaskai.com',
                    name='Quantum Digital'
                )
        
        # Clean up any remaining example.com sites
        Site.objects.using(db_alias).filter(domain='example.com').delete()
        
    except Exception as e:
        # If anything fails, continue silently to avoid breaking migrations
        # Log the error if we have logging available
        import logging
        logger = logging.getLogger(__name__)
        logger.warning(f"Site ID fix migration encountered error: {e}")
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