from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('public/<uuid:uuid>/', views.public_dashboard_view, name='public_dashboard'),
]