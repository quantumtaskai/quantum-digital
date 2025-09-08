from django.db import models
from django.contrib.auth.models import User
import uuid


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
    
    # Public Dashboard Sharing
    public_uuid = models.UUIDField(null=True, blank=True, unique=True, editable=False)
    is_public_enabled = models.BooleanField(default=False, help_text="Allow public access to dashboard via shareable link")
    public_link_created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_public_links', help_text="Manager who enabled public access")
    public_link_created_at = models.DateTimeField(null=True, blank=True, help_text="When public access was first enabled")
    
    # System Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.brand_name} - {self.user.username}"
    
    def generate_public_uuid(self):
        """Generate a unique UUID for public dashboard access"""
        if not self.public_uuid:
            self.public_uuid = uuid.uuid4()
            self.save(update_fields=['public_uuid'])
        return self.public_uuid
    
    def create_default_platform_records(self):
        """Create ClientPlatformProgress records for all available platforms"""
        from dashboard.models import ClientPlatformProgress
        
        # Get all platform choices
        platforms_to_create = []
        existing_platforms = set(
            ClientPlatformProgress.objects.filter(brand=self).values_list('platform', flat=True)
        )
        
        # Create records for platforms that don't exist yet
        for platform_code, platform_name in ClientPlatformProgress.PLATFORM_CHOICES:
            if platform_code not in existing_platforms:
                platforms_to_create.append(
                    ClientPlatformProgress(
                        brand=self,
                        platform=platform_code,
                        committed=0,
                        drafted=0,
                        published=0,
                        notes=f"Auto-created for {platform_name}"
                    )
                )
        
        # Bulk create all missing platform records
        if platforms_to_create:
            ClientPlatformProgress.objects.bulk_create(platforms_to_create)
            return len(platforms_to_create)
        return 0

    class Meta:
        verbose_name = "Brand Profile"
        verbose_name_plural = "Brand Profiles"
