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
            messages.success(request, 'Welcome! Your brand profile has been created successfully.')
            return redirect('dashboard:dashboard')
    else:
        form = BrandProfileForm()

    return render(request, 'profiles/onboarding.html', {'form': form})
