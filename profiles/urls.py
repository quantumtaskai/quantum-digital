from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('onboarding/', views.onboarding_view, name='onboarding'),
]