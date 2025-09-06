from django.dispatch import receiver
from django.shortcuts import redirect
from allauth.socialaccount.signals import pre_social_login, social_account_added
from allauth.account.signals import user_signed_up
from django.contrib.auth.models import User


@receiver(user_signed_up)
def redirect_to_onboarding(sender, **kwargs):
    """
    Signal handler to redirect new users (both regular signup and social login)
    to the onboarding process.
    """
    user = kwargs['user']
    request = kwargs['request']
    
    # Check if the user has a profile, if not they need onboarding
    try:
        from profiles.models import BrandProfile
        profile = BrandProfile.objects.get(user=user)
        # Profile exists, redirect to dashboard
        return redirect('dashboard:dashboard')
    except BrandProfile.DoesNotExist:
        # No profile, redirect to onboarding
        return redirect('profiles:onboarding')


@receiver(social_account_added)
def social_user_signed_up(sender, request, sociallogin, **kwargs):
    """
    Signal handler for when a social account is linked to a user.
    This ensures social login users go through onboarding if needed.
    """
    user = sociallogin.user
    
    try:
        from profiles.models import BrandProfile
        profile = BrandProfile.objects.get(user=user)
        # Profile exists, user can continue to dashboard
        pass
    except BrandProfile.DoesNotExist:
        # No profile, user needs onboarding
        # We'll handle this in the middleware since signals can't redirect directly
        request.session['needs_onboarding'] = True


@receiver(pre_social_login)
def social_login_handler(sender, request, sociallogin, **kwargs):
    """
    Signal handler called before social login is processed.
    We can use this to customize the social login flow.
    """
    # Extract email from social account
    email = sociallogin.account.extra_data.get('email')
    
    # If email exists, check if user already exists with that email
    if email:
        try:
            existing_user = User.objects.get(email=email)
            # User exists with this email, connect the social account
            sociallogin.connect(request, existing_user)
        except User.DoesNotExist:
            # New user, let the normal flow continue
            pass
