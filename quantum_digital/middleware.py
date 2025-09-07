from django.shortcuts import redirect
from django.urls import reverse
from profiles.models import BrandProfile


class OnboardingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if user is authenticated and not accessing auth, admin, or manager pages
        if (request.user.is_authenticated and 
            not request.path.startswith('/accounts/') and 
            not request.path.startswith('/admin/') and
            not request.path.startswith('/manager/') and
            not request.path.startswith('/profiles/onboarding/') and
            request.path != '/'):
            
            # Skip onboarding check for admin/staff users
            if request.user.is_staff or request.user.is_superuser:
                # Admin users can access manager dashboard without onboarding
                pass
            else:
                # Check if regular user has completed onboarding
                try:
                    BrandProfile.objects.get(user=request.user)
                except BrandProfile.DoesNotExist:
                    return redirect('profiles:onboarding')
        
        response = self.get_response(request)
        return response