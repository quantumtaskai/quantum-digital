from django.urls import path
from . import views

app_name = 'manager'

urlpatterns = [
    path('', views.manager_dashboard, name='dashboard'),
    path('brand/<int:brand_id>/', views.brand_detail, name='brand_detail'),
    path('generate-folder-structure/', views.generate_folder_structure, name='generate_folder_structure'),
    path('brand/<int:brand_id>/generate-folder/', views.generate_folder_structure, name='generate_brand_folder'),
]