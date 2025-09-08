from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import BrandProfile
from .forms import BrandProfileForm


@login_required
def onboarding_view(request):
    try:
        profile = BrandProfile.objects.get(user=request.user)
        return redirect('dashboard:dashboard')
    except BrandProfile.DoesNotExist:
        pass

    if request.method == 'POST':
        form = BrandProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            
            # Auto-create platform progress records for all platforms
            created_count = profile.create_default_platform_records()
            
            messages.success(request, f'Welcome! Your brand profile has been created successfully. {created_count} platform progress records have been initialized.')
            return redirect('dashboard:dashboard')
    else:
        form = BrandProfileForm()

    return render(request, 'profiles/onboarding.html', {'form': form})


@login_required
def profile_edit_view(request):
    try:
        profile = BrandProfile.objects.get(user=request.user)
    except BrandProfile.DoesNotExist:
        messages.error(request, 'Please complete your onboarding first.')
        return redirect('profiles:onboarding')

    if request.method == 'POST':
        form = BrandProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your brand profile has been updated successfully.')
            return redirect('dashboard:dashboard')
    else:
        form = BrandProfileForm(instance=profile)

    return render(request, 'profiles/profile_edit.html', {'form': form, 'profile': profile})
