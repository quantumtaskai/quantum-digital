from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('onboarding/', views.onboarding_view, name='onboarding'),
    path('edit/', views.profile_edit_view, name='edit'),
]