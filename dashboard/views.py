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
    
    # Parse profile data for dashboard
    context = {
        'profile': profile,
        'brand_name': profile.brand_name,
        'metrics': calculate_metrics(profile),
        'platforms': get_platform_data(profile),
        'social_platforms': get_social_platforms(profile),
        'kpis': get_kpis(profile),
        'swot': get_swot_analysis(profile),
        'business_intel': get_business_intelligence(profile),
        'platform_progress': get_platform_progress(request.user),
    }
    
    return render(request, 'dashboard/dashboard.html', context)


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
        {'name': 'Instagram', 'url': profile.instagram, 'icon': 'instagram'},
        {'name': 'Facebook', 'url': profile.facebook, 'icon': 'facebook'},
        {'name': 'Twitter/X', 'url': profile.twitter, 'icon': 'twitter'},
        {'name': 'LinkedIn', 'url': profile.linkedin, 'icon': 'linkedin'},
        {'name': 'TikTok', 'url': profile.tiktok, 'icon': 'tiktok'},
        {'name': 'YouTube', 'url': profile.youtube, 'icon': 'youtube'},
        {'name': 'Pinterest', 'url': profile.pinterest, 'icon': 'pinterest'},
        {'name': 'Snapchat', 'url': profile.snapchat, 'icon': 'snapchat'},
        {'name': 'Telegram', 'url': profile.telegram, 'icon': 'telegram'},
        {'name': 'Medium', 'url': profile.medium, 'icon': 'medium'},
        {'name': 'Quora', 'url': profile.quora, 'icon': 'quora'},
        {'name': 'Reddit', 'url': profile.reddit, 'icon': 'reddit'},
        {'name': 'Tumblr', 'url': profile.tumblr, 'icon': 'tumblr'},
        {'name': 'Threads', 'url': profile.threads, 'icon': 'threads'},
        {'name': 'BlueSky', 'url': profile.bluesky, 'icon': 'bluesky'},
        {'name': 'WhatsApp Business', 'url': profile.whatsapp_business, 'icon': 'whatsapp'},
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
    platform_progress = ClientPlatformProgress.objects.filter(user=user)
    
    total_committed = sum(p.committed for p in platform_progress)
    total_drafted = sum(p.drafted for p in platform_progress)
    total_published = sum(p.published for p in platform_progress)
    completion_rate = (total_published / total_committed * 100) if total_committed > 0 else 0
    
    return {
        'platforms': platform_progress,
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
