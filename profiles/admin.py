from django.contrib import admin
from .models import BrandProfile


@admin.register(BrandProfile)
class BrandProfileAdmin(admin.ModelAdmin):
    list_display = ('brand_name', 'user', 'primary_contact_first_name', 'primary_contact_last_name', 'created_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('brand_name', 'user__username', 'primary_contact_first_name', 'primary_contact_last_name')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Brand Information', {
            'fields': ('brand_name', 'brand_vision', 'brand_mission', 'brand_core_values')
        }),
        ('Primary Contact', {
            'fields': ('primary_contact_first_name', 'primary_contact_last_name', 'primary_official_email', 'primary_phone_number')
        }),
        ('Secondary Contact', {
            'fields': ('secondary_contact_first_name', 'secondary_contact_last_name', 'secondary_official_email', 'secondary_phone_number'),
            'classes': ('collapse',)
        }),
        ('Brand Assets', {
            'fields': ('brand_website', 'brand_visual_verbal_dna_guidelines', 'website_blogs', 'brand_presence')
        }),
        ('Current KPIs', {
            'fields': ('website_traffic_kpis', 'instagram_reach_kpis', 'google_sepr_rank_kpis', 'review_rating_kpis', 'social_media_posts_per_week_kpis', 'videos_per_week_kpis', 'shorts_per_week_kpis'),
            'classes': ('collapse',)
        }),
        ('SWOT Analysis', {
            'fields': ('strengths', 'weaknesses', 'opportunities', 'threats'),
            'classes': ('collapse',)
        }),
        ('Social Media Platforms', {
            'fields': ('instagram', 'facebook', 'twitter', 'linkedin', 'tiktok', 'youtube', 'pinterest', 'snapchat', 'telegram', 'medium', 'quora', 'reddit', 'tumblr', 'threads', 'bluesky', 'whatsapp_business'),
            'classes': ('collapse',)
        }),
        ('Business Intelligence', {
            'fields': ('top_10_partners', 'top_10_competitors', 'additional_notes'),
            'classes': ('collapse',)
        }),
        ('System Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # You can add logic here to trigger dashboard updates when admin saves changes
