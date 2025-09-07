from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
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
            context['platform_progress'] = get_platform_progress(profile)
        except Exception as e:
            print(f"Error getting platform progress: {e}")
            context['platform_progress'] = {'platforms': [], 'platform_names': []}
        
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
            'platform_progress': {'platforms': [], 'platform_names': []},
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
    # Get existing progress records
    existing_progress = ClientPlatformProgress.objects.filter(user=user)
    existing_platforms = {p.platform: p for p in existing_progress}
    
    # Create full platform list with defaults for missing ones
    all_platforms = []
    platform_names = []
    
    for platform_code, platform_name in ClientPlatformProgress.PLATFORM_CHOICES:
        if platform_code in existing_platforms:
            # Use existing data
            progress = existing_platforms[platform_code]
        else:
            # Create default data structure (not saved to DB)
            class DefaultProgress:
                def __init__(self, platform_code, platform_name):
                    self.platform = platform_code
                    self.committed = 0
                    self.drafted = 0
                    self.published = 0
                    self.completion_percentage = 0
                    self.content_links = type('MockManager', (), {'all': lambda: []})()
                
                def get_platform_display(self):
                    return dict(ClientPlatformProgress.PLATFORM_CHOICES)[self.platform]
            
            progress = DefaultProgress(platform_code, platform_name)
        
        all_platforms.append(progress)
        platform_names.append(platform_code)
    
    # Calculate totals from existing progress only
    total_committed = sum(p.committed for p in existing_progress)
    total_drafted = sum(p.drafted for p in existing_progress)
    total_published = sum(p.published for p in existing_progress)
    completion_rate = (total_published / total_committed * 100) if total_committed > 0 else 0
    
    return {
        'platforms': all_platforms,
        'platform_names': platform_names,
        'total_committed': total_committed,
        'total_drafted': total_drafted,
        'total_published': total_published,
        'completion_rate': round(completion_rate, 1),
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
