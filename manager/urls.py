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
    # Platform visibility management
    path('platform/<int:platform_id>/toggle-visibility/', views.toggle_platform_visibility, name='toggle_platform_visibility'),
    path('brand/<int:brand_id>/bulk-platform-visibility/', views.bulk_platform_visibility, name='bulk_platform_visibility'),
    # Platform active status management
    path('platform/<int:platform_id>/toggle-active/', views.toggle_platform_active, name='toggle_platform_active'),
    # Platform update page
    path('platform-update/', views.platform_update, name='platform_update'),
    path('brand/<int:brand_id>/platforms/', views.get_brand_platforms, name='get_brand_platforms'),
    path('platform/update-progress/', views.update_platform_progress, name='update_platform_progress'),
    path('platform/add-content-link/', views.add_content_link, name='add_content_link'),
    path('content-link/<int:link_id>/delete/', views.delete_content_link, name='delete_content_link'),
    # Brand quick update page
    path('brand/<int:brand_id>/quick-update/', views.brand_quick_update, name='brand_quick_update'),
]