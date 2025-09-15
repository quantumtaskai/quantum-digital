"""
Monkey patch to prevent Site model conflicts
This handles the root cause by preventing duplicate site creation at the model level
"""
from django.contrib.sites.models import Site
from django.db import IntegrityError
import logging

logger = logging.getLogger(__name__)

# Store the original save method
_original_save = Site.save

def patched_save(self, *args, **kwargs):
    """
    Patched save method that handles duplicate domain conflicts gracefully
    Only active outside of migrations to avoid interference
    """
    # Skip patch during migrations to avoid interference
    import sys
    if 'migrate' in sys.argv or 'makemigrations' in sys.argv:
        return _original_save(self, *args, **kwargs)
    
    try:
        return _original_save(self, *args, **kwargs)
    except IntegrityError as e:
        error_str = str(e).lower()
        if ('django_site_domain' in error_str or 'unique constraint failed: django_site.domain' in error_str):
            logger.warning(f"Site domain conflict detected for {self.domain}. Updating existing site instead.")
            
            # Try to update the existing site instead
            try:
                existing_site = Site.objects.get(domain=self.domain)
                existing_site.name = self.name
                return _original_save(existing_site, update_fields=['name'])
            except Site.DoesNotExist:
                # If for some reason the existing site isn't found, re-raise original error
                raise e
            except Exception:
                # If anything else goes wrong, log and continue
                logger.error(f"Failed to handle Site conflict for {self.domain}")
                return
        else:
            # Re-raise if it's not our specific conflict
            raise e

# Apply the patch
Site.save = patched_save

logger.info("Site model patched to handle domain conflicts gracefully")