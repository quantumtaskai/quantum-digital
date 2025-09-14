from django.apps import AppConfig


class DashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dashboard'
    
    def ready(self):
        """Apply patches when Django starts"""
        # Import the patch to prevent Site model conflicts
        from . import patch_sites  # noqa
