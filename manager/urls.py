from django.urls import path
from . import views

app_name = 'manager'

urlpatterns = [
    path('', views.manager_dashboard, name='dashboard'),
    path('brand/<int:brand_id>/', views.brand_detail, name='brand_detail'),
    path('generate-folder-structure/', views.generate_folder_structure, name='generate_folder_structure'),
    path('brand/<int:brand_id>/generate-folder/', views.generate_folder_structure, name='generate_brand_folder'),
    # Public dashboard management
    path('brand/<int:brand_id>/generate-public-link/', views.generate_public_link, name='generate_public_link'),
    path('brand/<int:brand_id>/toggle-public-access/', views.toggle_public_access, name='toggle_public_access'),
    path('brand/<int:brand_id>/regenerate-uuid/', views.regenerate_public_uuid, name='regenerate_public_uuid'),
]