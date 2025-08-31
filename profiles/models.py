from django.db import models
from django.contrib.auth.models import User


class BrandProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Brand Information
    brand_name = models.CharField(max_length=200)
    
    # Primary Contact
    primary_contact_first_name = models.CharField(max_length=100)
    primary_contact_last_name = models.CharField(max_length=100)
    primary_official_email = models.EmailField()
    primary_phone_number = models.CharField(max_length=20)
    
    # Secondary Contact (Optional)
    secondary_contact_first_name = models.CharField(max_length=100, blank=True, null=True)
    secondary_contact_last_name = models.CharField(max_length=100, blank=True, null=True)
    secondary_official_email = models.EmailField(blank=True, null=True)
    secondary_phone_number = models.CharField(max_length=20, blank=True, null=True)
    
    # Brand Strategy
    brand_vision = models.TextField()
    brand_mission = models.TextField()
    brand_core_values = models.TextField()
    brand_visual_verbal_dna_guidelines = models.URLField(blank=True, null=True)
    brand_website = models.URLField(blank=True, null=True)
    brand_presence = models.TextField(blank=True, null=True)
    
    # Current KPIs
    website_traffic_kpis = models.TextField(blank=True, null=True)
    instagram_reach_kpis = models.TextField(blank=True, null=True)
    google_sepr_rank_kpis = models.TextField(blank=True, null=True)
    review_rating_kpis = models.TextField(blank=True, null=True)
    social_media_posts_per_week_kpis = models.TextField(blank=True, null=True)
    videos_per_week_kpis = models.TextField(blank=True, null=True)
    shorts_per_week_kpis = models.TextField(blank=True, null=True)
    
    # SWOT Analysis
    strengths = models.TextField(blank=True, null=True)
    weaknesses = models.TextField(blank=True, null=True)
    opportunities = models.TextField(blank=True, null=True)
    threats = models.TextField(blank=True, null=True)
    
    # Social Media Platforms
    instagram = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    tiktok = models.URLField(blank=True, null=True)
    youtube = models.URLField(blank=True, null=True)
    pinterest = models.URLField(blank=True, null=True)
    snapchat = models.URLField(blank=True, null=True)
    telegram = models.URLField(blank=True, null=True)
    medium = models.URLField(blank=True, null=True)
    quora = models.URLField(blank=True, null=True)
    reddit = models.URLField(blank=True, null=True)
    tumblr = models.URLField(blank=True, null=True)
    threads = models.URLField(blank=True, null=True)
    bluesky = models.URLField(blank=True, null=True)
    whatsapp_business = models.URLField(blank=True, null=True)
    website_blogs = models.URLField(blank=True, null=True)
    
    # Business Intelligence
    top_10_partners = models.TextField(blank=True, null=True, help_text="List of top 10 partners")
    top_10_competitors = models.TextField(blank=True, null=True, help_text="List of top 10 competitors")
    additional_notes = models.TextField(blank=True, null=True)
    
    # System Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.brand_name} - {self.user.username}"

    class Meta:
        verbose_name = "Brand Profile"
        verbose_name_plural = "Brand Profiles"
