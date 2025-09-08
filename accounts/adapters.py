from allauth.account.adapter import DefaultAccountAdapter
from django.urls import reverse
from django.conf import settings


class CustomAccountAdapter(DefaultAccountAdapter):
    """
    Custom account adapter to handle role-based login redirects
    """
    
    def get_login_redirect_url(self, request):
        """
        Redirect users to appropriate dashboard based on their role
        """
        user = request.user
        
        # Redirect admin/staff users to manager dashboard
        if user.is_authenticated and (user.is_staff or user.is_superuser):
            return reverse('manager:dashboard')
        
        # For regular users, check if they have completed onboarding
        if user.is_authenticated:
            try:
                from profiles.models import BrandProfile
                BrandProfile.objects.get(user=user)
                # User has completed onboarding, go to regular dashboard
                return reverse('dashboard:dashboard')
            except BrandProfile.DoesNotExist:
                # User hasn't completed onboarding, redirect to onboarding
                return reverse('profiles:onboarding')
        
        # Fallback to default behavior
        return super().get_login_redirect_url(request)