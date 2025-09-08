from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from profiles.models import BrandProfile
from .models import ClientPlatformProgress
import re


@login_required
def dashboard_view(request):
    try:
        profile = BrandProfile.objects.get(user=request.user)
    except BrandProfile.DoesNotExist:
        return redirect('profiles:onboarding')
    
    try:
        # Parse profile data for dashboard with individual error handling
        context = {
            'profile': profile,
            'brand_name': getattr(profile, 'brand_name', 'Unknown Brand'),
        }
        
        # Add each context item with error handling
        try:
            context['metrics'] = calculate_metrics(profile)
        except Exception as e:
            print(f"Error calculating metrics: {e}")
            context['metrics'] = {'total_platforms': 0, 'active_platforms': 0}
        
        try:
            context['platforms'] = get_platform_data(profile)
        except Exception as e:
            print(f"Error getting platform data: {e}")
            context['platforms'] = {}
        
        try:
            context['social_platforms'] = get_social_platforms(profile)
        except Exception as e:
            print(f"Error getting social platforms: {e}")
            context['social_platforms'] = []
        
        try:
            context['kpis'] = get_kpis(profile)
        except Exception as e:
            print(f"Error getting KPIs: {e}")
            context['kpis'] = {}
        
        try:
            context['swot'] = get_swot_analysis(profile)
        except Exception as e:
            print(f"Error getting SWOT: {e}")
            context['swot'] = {'strengths': [], 'weaknesses': [], 'opportunities': [], 'threats': []}
        
        try:
            context['business_intel'] = get_business_intelligence(profile)
        except Exception as e:
            print(f"Error getting business intel: {e}")
            context['business_intel'] = {'partners': [], 'competitors': [], 'notes': ''}
        
        try:
            context['platform_progress'] = get_platform_progress(profile.user)
        except Exception as e:
            print(f"Error getting platform progress: {e}")
            context['platform_progress'] = {
                'platforms': [], 
                'platform_names': [],
                'total_committed': 0,
                'total_drafted': 0,
                'total_published': 0,
                'completion_rate': 0,
                'active_platforms_count': 0,
                'inactive_platforms_count': 0,
                'in_progress_count': 0,
            }
        
        return render(request, 'dashboard/dashboard.html', context)
        
    except Exception as e:
        print(f"Dashboard view error: {e}")
        import traceback
        print(traceback.format_exc())
        # Return a minimal context to prevent total failure
        return render(request, 'dashboard/dashboard.html', {
            'profile': profile,
            'brand_name': getattr(profile, 'brand_name', 'Unknown Brand'),
            'metrics': {'total_platforms': 0, 'active_platforms': 0},
            'platforms': {},
            'social_platforms': [],
            'kpis': {},
            'swot': {'strengths': [], 'weaknesses': [], 'opportunities': [], 'threats': []},
            'business_intel': {'partners': [], 'competitors': [], 'notes': ''},
            'platform_progress': {
                'platforms': [], 
                'platform_names': [],
                'total_committed': 0,
                'total_drafted': 0,
                'total_published': 0,
                'completion_rate': 0,
                'active_platforms_count': 0,
                'inactive_platforms_count': 0,
                'in_progress_count': 0,
            },
        })


def calculate_metrics(profile):
    """Calculate key metrics for the dashboard"""
    social_platforms = get_social_platforms(profile)
    active_platforms = sum(1 for platform in social_platforms if platform['url'])
    total_platforms = len(social_platforms)
    
    # Extract numeric values from KPIs
    posts_per_week = extract_number(profile.social_media_posts_per_week_kpis) or 0
    videos_per_week = extract_number(profile.videos_per_week_kpis) or 0
    shorts_per_week = extract_number(profile.shorts_per_week_kpis) or 0
    
    total_content_per_week = posts_per_week + videos_per_week + shorts_per_week
    
    return {
        'total_platforms': total_platforms,
        'active_platforms': active_platforms,
        'inactive_platforms': total_platforms - active_platforms,
        'total_content_per_week': total_content_per_week,
        'posts_per_week': posts_per_week,
        'videos_per_week': videos_per_week,
        'shorts_per_week': shorts_per_week,
        'website_traffic': profile.website_traffic_kpis or 'N/A',
        'instagram_reach': profile.instagram_reach_kpis or 'N/A',
        'review_rating': profile.review_rating_kpis or 'N/A',
    }


def get_social_platforms(profile):
    """Get social media platforms data"""
    platforms = [
        {'name': 'Instagram', 'url': profile.instagram, 'icon': 'instagram', 'field_name': 'instagram'},
        {'name': 'Facebook', 'url': profile.facebook, 'icon': 'facebook', 'field_name': 'facebook'},
        {'name': 'Twitter/X', 'url': profile.twitter, 'icon': 'twitter', 'field_name': 'twitter'},
        {'name': 'LinkedIn', 'url': profile.linkedin, 'icon': 'linkedin', 'field_name': 'linkedin'},
        {'name': 'TikTok', 'url': profile.tiktok, 'icon': 'tiktok', 'field_name': 'tiktok'},
        {'name': 'YouTube', 'url': profile.youtube, 'icon': 'youtube', 'field_name': 'youtube'},
        {'name': 'Pinterest', 'url': profile.pinterest, 'icon': 'pinterest', 'field_name': 'pinterest'},
        {'name': 'Snapchat', 'url': profile.snapchat, 'icon': 'snapchat', 'field_name': 'snapchat'},
        {'name': 'Telegram', 'url': profile.telegram, 'icon': 'telegram', 'field_name': 'telegram'},
        {'name': 'Medium', 'url': profile.medium, 'icon': 'medium', 'field_name': 'medium'},
        {'name': 'Quora', 'url': profile.quora, 'icon': 'quora', 'field_name': 'quora'},
        {'name': 'Reddit', 'url': profile.reddit, 'icon': 'reddit', 'field_name': 'reddit'},
        {'name': 'Tumblr', 'url': profile.tumblr, 'icon': 'tumblr', 'field_name': 'tumblr'},
        {'name': 'Threads', 'url': profile.threads, 'icon': 'threads', 'field_name': 'threads'},
        {'name': 'BlueSky', 'url': profile.bluesky, 'icon': 'bluesky', 'field_name': 'bluesky'},
        {'name': 'WhatsApp Business', 'url': profile.whatsapp_business, 'icon': 'whatsapp', 'field_name': 'whatsapp_business'},
        {'name': 'Website Blogs', 'url': profile.website_blogs, 'icon': 'globe', 'field_name': 'website_blogs'},
    ]
    
    for platform in platforms:
        platform['status'] = 'active' if platform['url'] else 'inactive'
    
    return platforms


def get_platform_data(profile):
    """Get platform performance data"""
    return {
        'website': profile.brand_website,
        'blog': profile.website_blogs,
        'guidelines': profile.brand_visual_verbal_dna_guidelines,
    }


def get_kpis(profile):
    """Get KPI data"""
    return {
        'website_traffic': profile.website_traffic_kpis,
        'instagram_reach': profile.instagram_reach_kpis,
        'google_rank': profile.google_sepr_rank_kpis,
        'review_rating': profile.review_rating_kpis,
        'posts_per_week': profile.social_media_posts_per_week_kpis,
        'videos_per_week': profile.videos_per_week_kpis,
        'shorts_per_week': profile.shorts_per_week_kpis,
    }


def get_swot_analysis(profile):
    """Get SWOT analysis data"""
    return {
        'strengths': parse_list_field(profile.strengths),
        'weaknesses': parse_list_field(profile.weaknesses),
        'opportunities': parse_list_field(profile.opportunities),
        'threats': parse_list_field(profile.threats),
    }


def get_business_intelligence(profile):
    """Get business intelligence data"""
    return {
        'partners': parse_list_field(profile.top_10_partners),
        'competitors': parse_list_field(profile.top_10_competitors),
        'notes': profile.additional_notes,
    }


def get_platform_progress(user):
    """Get platform progress data from admin updates"""
    # Get existing progress records - need to get brand first, then filter by brand
    try:
        from profiles.models import BrandProfile
        brand = BrandProfile.objects.get(user=user)
        all_platforms = ClientPlatformProgress.objects.filter(brand=brand).order_by('platform')
        
        # Ensure all platforms exist (auto-create if missing for existing brands)
        if all_platforms.count() < len(ClientPlatformProgress.PLATFORM_CHOICES):
            created_count = brand.create_default_platform_records()
            if created_count > 0:
                # Re-fetch after creating missing records
                all_platforms = ClientPlatformProgress.objects.filter(brand=brand).order_by('platform')
                
    except BrandProfile.DoesNotExist:
        all_platforms = ClientPlatformProgress.objects.none()
    
    # Convert to list and extract platform names
    all_platforms = list(all_platforms)
    platform_names = [p.platform for p in all_platforms]
    
    # Calculate totals from all platforms
    total_committed = sum(p.committed for p in all_platforms)
    total_drafted = sum(p.drafted for p in all_platforms)
    total_published = sum(p.published for p in all_platforms)
    completion_rate = (total_published / total_committed * 100) if total_committed > 0 else 0
    
    # Calculate chart-specific metrics for pie chart
    active_platforms_count = sum(1 for p in all_platforms if p.committed > 0)
    inactive_platforms_count = sum(1 for p in all_platforms if p.committed == 0)
    in_progress_count = sum(1 for p in all_platforms if p.drafted > 0 and p.published < p.committed)
    
    return {
        'platforms': all_platforms,
        'platform_names': platform_names,
        'total_committed': total_committed,
        'total_drafted': total_drafted,
        'total_published': total_published,
        'completion_rate': round(completion_rate, 1),
        'active_platforms_count': active_platforms_count,
        'inactive_platforms_count': inactive_platforms_count,
        'in_progress_count': in_progress_count,
    }


def extract_number(text):
    """Extract number from text"""
    if not text:
        return 0
    match = re.search(r'(\d+(?:\.\d+)?)', str(text))
    return float(match.group(1)) if match else 0


def parse_list_field(field_text):
    """Parse list field into array"""
    if not field_text:
        return []
    return [item.strip() for item in field_text.split('\n') if item.strip()]


def public_dashboard_view(request, uuid):
    """Public dashboard view - accessible without login via UUID"""
    try:
        profile = get_object_or_404(BrandProfile, public_uuid=uuid)
        
        # Check if public access is enabled
        if not profile.is_public_enabled:
            raise Http404("Public access to this dashboard is not enabled")
        
        # Use the same data processing as regular dashboard
        try:
            context = {
                'profile': profile,
                'brand_name': getattr(profile, 'brand_name', 'Unknown Brand'),
                'is_public_view': True,  # Flag to indicate this is public view
            }
            
            # Add each context item with error handling (same as regular dashboard)
            try:
                context['metrics'] = calculate_metrics(profile)
            except Exception as e:
                print(f"Error calculating metrics: {e}")
                context['metrics'] = {'total_platforms': 0, 'active_platforms': 0}
            
            try:
                context['platforms'] = get_platform_data(profile)
            except Exception as e:
                print(f"Error getting platform data: {e}")
                context['platforms'] = {}
            
            try:
                context['social_platforms'] = get_social_platforms(profile)
            except Exception as e:
                print(f"Error getting social platforms: {e}")
                context['social_platforms'] = []
            
            try:
                context['kpis'] = get_kpis(profile)
            except Exception as e:
                print(f"Error getting KPIs: {e}")
                context['kpis'] = {}
            
            try:
                context['swot'] = get_swot_analysis(profile)
            except Exception as e:
                print(f"Error getting SWOT: {e}")
                context['swot'] = {'strengths': [], 'weaknesses': [], 'opportunities': [], 'threats': []}
            
            try:
                context['business_intel'] = get_business_intelligence(profile)
            except Exception as e:
                print(f"Error getting business intel: {e}")
                context['business_intel'] = {'partners': [], 'competitors': [], 'notes': ''}
            
            try:
                # For public dashboard, pass the user from the profile
                context['platform_progress'] = get_platform_progress(profile.user)
            except Exception as e:
                print(f"Error getting platform progress: {e}")
                context['platform_progress'] = {
                    'platforms': [], 
                    'platform_names': [],
                    'total_committed': 0,
                    'total_drafted': 0,
                    'total_published': 0,
                    'completion_rate': 0,
                    'active_platforms_count': 0,
                    'inactive_platforms_count': 0,
                    'in_progress_count': 0,
                }
            
            return render(request, 'dashboard/public_dashboard.html', context)
            
        except Exception as e:
            print(f"Public dashboard view error: {e}")
            import traceback
            print(traceback.format_exc())
            # Return a minimal context to prevent total failure
            return render(request, 'dashboard/public_dashboard.html', {
                'profile': profile,
                'brand_name': getattr(profile, 'brand_name', 'Unknown Brand'),
                'is_public_view': True,
                'metrics': {'total_platforms': 0, 'active_platforms': 0},
                'platforms': {},
                'social_platforms': [],
                'kpis': {},
                'swot': {'strengths': [], 'weaknesses': [], 'opportunities': [], 'threats': []},
                'business_intel': {'partners': [], 'competitors': [], 'notes': ''},
                'platform_progress': {
                    'platforms': [], 
                    'platform_names': [],
                    'total_committed': 0,
                    'total_drafted': 0,
                    'total_published': 0,
                    'completion_rate': 0,
                    'active_platforms_count': 0,
                    'inactive_platforms_count': 0,
                    'in_progress_count': 0,
                },
            })
            
    except BrandProfile.DoesNotExist:
        raise Http404("Public dashboard not found")
