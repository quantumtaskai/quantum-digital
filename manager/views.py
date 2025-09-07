from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q, Count, Sum
from django.http import JsonResponse
from profiles.models import BrandProfile
from dashboard.models import ClientPlatformProgress
import zipfile
import io
import os
from django.http import HttpResponse


def is_staff_user(user):
    """Check if user is staff/admin to access manager dashboard"""
    return user.is_authenticated and (user.is_staff or user.is_superuser)


@user_passes_test(is_staff_user)
def manager_dashboard(request):
    """Main manager dashboard - shows all brands in card layout"""
    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort', 'newest')
    
    # Get all brand profiles
    brands = BrandProfile.objects.select_related('user').all()
    
    # Search functionality
    if search_query:
        brands = brands.filter(
            Q(brand_name__icontains=search_query) |
            Q(user__username__icontains=search_query) |
            Q(user__email__icontains=search_query)
        )
    
    # Sorting
    if sort_by == 'newest':
        brands = brands.order_by('-created_at')
    elif sort_by == 'oldest':
        brands = brands.order_by('created_at')
    elif sort_by == 'name':
        brands = brands.order_by('brand_name')
    
    # Add platform progress counts to each brand
    for brand in brands:
        brand.platform_count = ClientPlatformProgress.objects.filter(user=brand.user).count()
        progress_data = ClientPlatformProgress.objects.filter(user=brand.user).aggregate(
            total_committed=Sum('committed'),
            total_published=Sum('published')
        )
        brand.total_committed = progress_data.get('total_committed', 0) or 0
        brand.total_published = progress_data.get('total_published', 0) or 0
        if brand.total_committed > 0:
            brand.completion_rate = round((brand.total_published / brand.total_committed) * 100, 1)
        else:
            brand.completion_rate = 0
    
    context = {
        'brands': brands,
        'search_query': search_query,
        'sort_by': sort_by,
        'total_brands': brands.count(),
    }
    
    return render(request, 'manager/dashboard.html', context)


@user_passes_test(is_staff_user)
def brand_detail(request, brand_id):
    """Brand detail page with tabs for management"""
    brand = get_object_or_404(BrandProfile, id=brand_id)
    
    # Get platform progress for this brand
    platforms = ClientPlatformProgress.objects.filter(user=brand.user).order_by('platform')
    
    context = {
        'brand': brand,
        'platforms': platforms,
    }
    
    return render(request, 'manager/brand_detail.html', context)


@user_passes_test(is_staff_user)
def generate_folder_structure(request, brand_id=None):
    """Generate folder structure for download"""
    if brand_id:
        brands = [get_object_or_404(BrandProfile, id=brand_id)]
    else:
        # Bulk generation - get selected brand IDs
        brand_ids = request.POST.getlist('brand_ids', [])
        brands = BrandProfile.objects.filter(id__in=brand_ids)
    
    if not brands:
        return JsonResponse({'error': 'No brands selected'}, status=400)
    
    # Create ZIP file in memory
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for brand in brands:
            clean_brand_name = brand.brand_name.replace(' ', '_').replace('/', '_')
            brand_folder = f"{clean_brand_name}/"
            
            # Create folder structure
            folders = [
                f"{brand_folder}Client Docs/",
                f"{brand_folder}Images/",
                f"{brand_folder}Videos/",
                f"{brand_folder}00_Brand_voice_guidelines_{clean_brand_name}/",
                f"{brand_folder}00_Digital Marketing {brand.brand_name}/",
                f"{brand_folder}00_Social_Media_Templates_{clean_brand_name}/",
                f"{brand_folder}01_Blogs_{clean_brand_name}/",
                f"{brand_folder}02_Website_Downloadable_{clean_brand_name}/",
                f"{brand_folder}03_Google_Business_{clean_brand_name}/",
                f"{brand_folder}04_LinkedIn_{clean_brand_name}/",
                f"{brand_folder}07_Instagram_{clean_brand_name}/",
                f"{brand_folder}08_Pinterest_{clean_brand_name}/",
                f"{brand_folder}09_X_Twitter_{clean_brand_name}/",
                f"{brand_folder}10_Facebook_{clean_brand_name}/",
                f"{brand_folder}11_Medium_{clean_brand_name}/",
                f"{brand_folder}12_Threads_{clean_brand_name}/",
            ]
            
            # Add folders to ZIP (create empty directories)
            for folder in folders:
                zip_file.writestr(folder, '')
                
            # Add a README file with instructions
            readme_content = f"""# {brand.brand_name} - Content Folder Structure

## Instructions:
1. Upload this entire folder structure to Google Drive
2. Share the main '{brand.brand_name}' folder with your content team
3. Use these folders to organize your content by platform

## Folder Structure:
- Client Docs: Important documents and contracts
- Images: Brand images, logos, graphics
- Videos: Video content and assets
- 00_Brand_voice_guidelines: Brand voice and messaging guidelines
- 00_Digital Marketing: Overall digital marketing strategy
- 00_Social_Media_Templates: Reusable templates
- Platform-specific folders (01-12): Organized by platform

Created by Quantum Digital Manager Dashboard
"""
            zip_file.writestr(f"{brand_folder}README.md", readme_content)
    
    zip_buffer.seek(0)
    
    # Return ZIP file as download
    response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
    if len(brands) == 1:
        filename = f"{brands[0].brand_name.replace(' ', '_')}_folder_structure.zip"
    else:
        filename = f"bulk_folder_structures_{len(brands)}_brands.zip"
    
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response
