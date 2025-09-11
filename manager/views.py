from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q, Count, Sum
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from profiles.models import BrandProfile
from dashboard.models import ClientPlatformProgress, ContentLink
from django.utils import timezone
from django.urls import reverse
import zipfile
import io
import os
from django.http import HttpResponse
from django.contrib import messages


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
        brand.platform_count = ClientPlatformProgress.objects.filter(brand=brand).count()
        progress_data = ClientPlatformProgress.objects.filter(brand=brand).aggregate(
            total_committed=Sum('committed'),
            total_published=Sum('published')
        )
        brand.total_committed = progress_data.get('total_committed', 0) or 0
        brand.total_published = progress_data.get('total_published', 0) or 0
        if brand.total_committed > 0:
            brand.completion_rate = round((brand.total_published / brand.total_committed) * 100, 1)
        else:
            brand.completion_rate = 0
    
    # Calculate summary statistics 
    total_platforms = sum(brand.platform_count for brand in brands)
    total_committed_all = sum(brand.total_committed for brand in brands)
    total_published_all = sum(brand.total_published for brand in brands)
    
    context = {
        'brands': brands,
        'search_query': search_query,
        'sort_by': sort_by,
        'total_brands': brands.count(),
        'total_platforms': total_platforms,
        'total_committed_all': total_committed_all, 
        'total_published_all': total_published_all,
    }
    
    return render(request, 'manager/dashboard.html', context)


@user_passes_test(is_staff_user)
def brand_detail(request, brand_id):
    """Brand detail page with tabs for management"""
    brand = get_object_or_404(BrandProfile, id=brand_id)
    
    # Get platform progress for this brand
    platforms = ClientPlatformProgress.objects.filter(brand=brand).order_by('platform')
    
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


@user_passes_test(is_staff_user)
def generate_public_link(request, brand_id):
    """Generate or retrieve public dashboard link for a brand"""
    brand = get_object_or_404(BrandProfile, id=brand_id)
    
    if request.method == 'POST':
        # Generate UUID if not exists
        if not brand.public_uuid:
            brand.generate_public_uuid()
        
        # Enable public access and track who enabled it
        brand.is_public_enabled = True
        brand.public_link_created_by = request.user
        if not brand.public_link_created_at:
            brand.public_link_created_at = timezone.now()
        brand.save(update_fields=['is_public_enabled', 'public_link_created_by', 'public_link_created_at'])
        
        # Build full URL for the public dashboard
        public_url = request.build_absolute_uri(
            reverse('dashboard:public_dashboard', kwargs={'uuid': brand.public_uuid})
        )
        
        return JsonResponse({
            'success': True,
            'public_url': public_url,
            'uuid': str(brand.public_uuid),
            'enabled_at': brand.public_link_created_at.isoformat(),
            'enabled_by': brand.public_link_created_by.username
        })
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)


@user_passes_test(is_staff_user)
def toggle_public_access(request, brand_id):
    """Toggle public dashboard access for a brand"""
    brand = get_object_or_404(BrandProfile, id=brand_id)
    
    if request.method == 'POST':
        brand.is_public_enabled = not brand.is_public_enabled
        
        if brand.is_public_enabled:
            # Generate UUID if enabling and doesn't exist
            if not brand.public_uuid:
                brand.generate_public_uuid()
            if not brand.public_link_created_at:
                brand.public_link_created_at = timezone.now()
            brand.public_link_created_by = request.user
        
        brand.save(update_fields=['is_public_enabled', 'public_link_created_by', 'public_link_created_at'])
        
        return JsonResponse({
            'success': True,
            'is_enabled': brand.is_public_enabled,
            'public_uuid': str(brand.public_uuid) if brand.public_uuid else None
        })
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)


@user_passes_test(is_staff_user)
def regenerate_public_uuid(request, brand_id):
    """Regenerate UUID for public dashboard link (revokes old link)"""
    brand = get_object_or_404(BrandProfile, id=brand_id)
    
    if request.method == 'POST':
        # Force generate new UUID
        import uuid
        brand.public_uuid = uuid.uuid4()
        brand.public_link_created_by = request.user
        brand.public_link_created_at = timezone.now()
        brand.save(update_fields=['public_uuid', 'public_link_created_by', 'public_link_created_at'])
        
        # Build new public URL
        public_url = request.build_absolute_uri(
            reverse('dashboard:public_dashboard', kwargs={'uuid': brand.public_uuid})
        )
        
        return JsonResponse({
            'success': True,
            'public_url': public_url,
            'uuid': str(brand.public_uuid),
            'regenerated_at': brand.public_link_created_at.isoformat()
        })
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)


@user_passes_test(is_staff_user)
@require_POST
def toggle_platform_visibility(request, platform_id):
    """Toggle visibility of a specific platform"""
    try:
        from dashboard.models import ClientPlatformProgress
        platform = get_object_or_404(ClientPlatformProgress, id=platform_id)
        
        # Toggle visibility
        platform.is_visible = not platform.is_visible
        platform.save()
        
        return JsonResponse({
            'success': True,
            'is_visible': platform.is_visible,
            'platform_name': platform.get_platform_display()
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@user_passes_test(is_staff_user)
@require_POST 
def bulk_platform_visibility(request, brand_id):
    """Bulk update platform visibility"""
    try:
        from dashboard.models import ClientPlatformProgress
        from profiles.models import BrandProfile
        
        brand = get_object_or_404(BrandProfile, id=brand_id)
        
        action = request.POST.get('action')
        
        if action == 'show_all':
            ClientPlatformProgress.objects.filter(brand=brand).update(is_visible=True)
            message = "All platforms are now visible"
        elif action == 'hide_inactive':
            ClientPlatformProgress.objects.filter(brand=brand, committed=0).update(is_visible=False)
            message = "Inactive platforms are now hidden"
        else:
            return JsonResponse({'error': 'Invalid action'}, status=400)
        
        return JsonResponse({
            'success': True,
            'message': message
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@user_passes_test(is_staff_user)
@require_POST
def toggle_platform_active(request, platform_id):
    """Toggle active status of a specific platform"""
    try:
        from dashboard.models import ClientPlatformProgress
        platform = get_object_or_404(ClientPlatformProgress, id=platform_id)
        
        # Toggle active status
        platform.is_active = not platform.is_active
        platform.save()
        
        return JsonResponse({
            'success': True,
            'is_active': platform.is_active,
            'platform_name': platform.get_platform_display()
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@user_passes_test(is_staff_user)
def platform_update(request):
    """Simple platform progress update page"""
    brands = BrandProfile.objects.select_related('user').all().order_by('brand_name')
    
    context = {
        'brands': brands,
    }
    
    return render(request, 'manager/platform_update.html', context)


@user_passes_test(is_staff_user)
def get_brand_platforms(request, brand_id):
    """AJAX endpoint to get platforms for a specific brand"""
    try:
        brand = get_object_or_404(BrandProfile, id=brand_id)
        platforms = ClientPlatformProgress.objects.filter(brand=brand).order_by('platform')
        
        platforms_data = []
        for platform in platforms:
            platforms_data.append({
                'id': platform.id,
                'platform': platform.platform,
                'platform_display': platform.get_platform_display(),
                'committed': platform.committed,
                'drafted': platform.drafted,
                'published': platform.published,
                'notes': platform.notes,
                'is_visible': platform.is_visible,
                'is_active': platform.is_active,
                'content_links': [
                    {'id': link.id, 'title': link.title, 'url': link.url}
                    for link in platform.content_links.all()
                ]
            })
        
        return JsonResponse({
            'success': True,
            'platforms': platforms_data,
            'brand_name': brand.brand_name
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@user_passes_test(is_staff_user)
@require_POST
def update_platform_progress(request):
    """AJAX endpoint to update platform progress"""
    try:
        platform_id = request.POST.get('platform_id')
        committed = int(request.POST.get('committed', 0))
        drafted = int(request.POST.get('drafted', 0))
        published = int(request.POST.get('published', 0))
        notes = request.POST.get('notes', '')
        platform_link = request.POST.get('platform_link', '').strip()
        
        # Validation
        if drafted > committed:
            return JsonResponse({'error': 'Drafted cannot be more than committed'}, status=400)
        if published > drafted:
            return JsonResponse({'error': 'Published cannot be more than drafted'}, status=400)
        
        platform = get_object_or_404(ClientPlatformProgress, id=platform_id)
        platform.committed = committed
        platform.drafted = drafted
        platform.published = published
        platform.notes = notes
        platform.save()
        
        # Handle platform link - create/update/delete Platform Profile content link
        platform_profile_link = ContentLink.objects.filter(
            platform_progress=platform, 
            title='Platform Profile'
        ).first()
        
        if platform_link:
            # Create or update platform profile link
            if platform_profile_link:
                platform_profile_link.url = platform_link
                platform_profile_link.save()
            else:
                ContentLink.objects.create(
                    platform_progress=platform,
                    title='Platform Profile',
                    url=platform_link
                )
        else:
            # Delete platform profile link if empty
            if platform_profile_link:
                platform_profile_link.delete()
        
        return JsonResponse({
            'success': True,
            'completion_percentage': platform.completion_percentage,
            'draft_percentage': platform.draft_percentage,
            'message': f'{platform.get_platform_display()} updated successfully'
        })
        
    except ValueError as e:
        return JsonResponse({'error': 'Please enter valid numbers'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@user_passes_test(is_staff_user)
@require_POST
def add_content_link(request):
    """AJAX endpoint to add a content link to a platform"""
    try:
        platform_id = request.POST.get('platform_id')
        title = request.POST.get('title', '').strip()
        url = request.POST.get('url', '').strip()
        
        if not title or not url:
            return JsonResponse({'error': 'Title and URL are required'}, status=400)
        
        platform = get_object_or_404(ClientPlatformProgress, id=platform_id)
        content_link = ContentLink.objects.create(
            platform_progress=platform,
            title=title,
            url=url
        )
        
        return JsonResponse({
            'success': True,
            'link': {
                'id': content_link.id,
                'title': content_link.title,
                'url': content_link.url
            },
            'message': 'Content link added successfully'
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@user_passes_test(is_staff_user)
@require_POST
def delete_content_link(request, link_id):
    """AJAX endpoint to delete a content link"""
    try:
        content_link = get_object_or_404(ContentLink, id=link_id)
        content_link.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Content link deleted successfully'
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@user_passes_test(is_staff_user)
def brand_quick_update(request, brand_id):
    """Brand-specific quick update page showing all platforms in a table"""
    brand = get_object_or_404(BrandProfile, id=brand_id)
    
    # Get all platforms for this brand
    platforms = ClientPlatformProgress.objects.filter(brand=brand).order_by('platform')
    
    # Add platform links and content links to each platform
    for platform in platforms:
        # Get platform profile link
        platform_profile = ContentLink.objects.filter(
            platform_progress=platform, 
            title='Platform Profile'
        ).first()
        platform.platform_link = platform_profile.url if platform_profile else ''
        
        # Get other content links (excluding platform profile)
        platform.other_content_links = ContentLink.objects.filter(
            platform_progress=platform
        ).exclude(title='Platform Profile')
    
    context = {
        'brand': brand,
        'platforms': platforms,
    }
    
    return render(request, 'manager/brand_quick_update.html', context)
