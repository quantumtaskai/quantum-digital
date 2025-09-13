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
                        notes=f"Auto-created for {platform_name}",
                        is_visible=True,
                        is_active=True
                    )
                )
        
        # Bulk create all missing platform records
        if platforms_to_create:
            ClientPlatformProgress.objects.bulk_create(platforms_to_create)
            return len(platforms_to_create)
        return 0

    @classmethod
    def create_from_red_dot_template(cls, brand_name, created_by_user):
        """Create a new brand using Red Dot Events as template"""
        from django.contrib.auth.models import User
        from dashboard.models import ClientPlatformProgress
        
        try:
            # Get Red Dot Events brand as template
            template_brand = cls.objects.get(brand_name__icontains='red dot events')
        except cls.DoesNotExist:
            raise ValueError("Red Dot Events template brand not found")
        
        # Create username from brand name
        username = brand_name.lower().replace(' ', '_').replace('-', '_')
        # Ensure username is unique
        counter = 1
        original_username = username
        while User.objects.filter(username=username).exists():
            username = f"{original_username}_{counter}"
            counter += 1
        
        # Create user account for the brand
        user = User.objects.create_user(
            username=username,
            email=f"{username}@example.com",  # Dummy email, can be updated later
            first_name=template_brand.primary_contact_first_name,
            last_name=template_brand.primary_contact_last_name,
        )
        
        # Create new brand profile by copying from template
        new_brand = cls.objects.create(
            user=user,
            brand_name=brand_name,
            
            # Copy contact information from template
            primary_contact_first_name=template_brand.primary_contact_first_name,
            primary_contact_last_name=template_brand.primary_contact_last_name,
            primary_official_email=template_brand.primary_official_email,
            primary_phone_number=template_brand.primary_phone_number,
            
            # Copy secondary contact if exists
            secondary_contact_first_name=template_brand.secondary_contact_first_name,
            secondary_contact_last_name=template_brand.secondary_contact_last_name,
            secondary_official_email=template_brand.secondary_official_email,
            secondary_phone_number=template_brand.secondary_phone_number,
            
            # Copy brand strategy
            brand_vision=template_brand.brand_vision,
            brand_mission=template_brand.brand_mission,
            brand_core_values=template_brand.brand_core_values,
            brand_visual_verbal_dna_guidelines=template_brand.brand_visual_verbal_dna_guidelines,
            brand_website=template_brand.brand_website,
            brand_presence=template_brand.brand_presence,
            
            # Copy KPIs
            website_traffic_kpis=template_brand.website_traffic_kpis,
            instagram_reach_kpis=template_brand.instagram_reach_kpis,
            google_sepr_rank_kpis=template_brand.google_sepr_rank_kpis,
            review_rating_kpis=template_brand.review_rating_kpis,
            social_media_posts_per_week_kpis=template_brand.social_media_posts_per_week_kpis,
            videos_per_week_kpis=template_brand.videos_per_week_kpis,
            shorts_per_week_kpis=template_brand.shorts_per_week_kpis,
            
            # Copy SWOT analysis
            strengths=template_brand.strengths,
            weaknesses=template_brand.weaknesses,
            opportunities=template_brand.opportunities,
            threats=template_brand.threats,
            
            # Copy social media platforms (will be updated with brand-specific URLs later)
            instagram=template_brand.instagram,
            facebook=template_brand.facebook,
            twitter=template_brand.twitter,
            linkedin=template_brand.linkedin,
            tiktok=template_brand.tiktok,
            youtube=template_brand.youtube,
            pinterest=template_brand.pinterest,
            snapchat=template_brand.snapchat,
            telegram=template_brand.telegram,
            medium=template_brand.medium,
            quora=template_brand.quora,
            reddit=template_brand.reddit,
            tumblr=template_brand.tumblr,
            threads=template_brand.threads,
            bluesky=template_brand.bluesky,
            whatsapp_business=template_brand.whatsapp_business,
            website_blogs=template_brand.website_blogs,
            
            # Copy business intelligence
            top_10_partners=template_brand.top_10_partners,
            top_10_competitors=template_brand.top_10_competitors,
            additional_notes=f"Created from Red Dot Events template by {created_by_user.username}",
        )
        
        # Copy platform progress records with same committed values
        template_platforms = ClientPlatformProgress.objects.filter(brand=template_brand)
        platforms_to_create = []
        
        for template_platform in template_platforms:
            platforms_to_create.append(
                ClientPlatformProgress(
                    brand=new_brand,
                    platform=template_platform.platform,
                    committed=template_platform.committed,  # Copy exact committed values
                    drafted=0,  # Start fresh
                    published=0,  # Start fresh
                    notes=f"Committed values copied from Red Dot Events template",
                    is_visible=template_platform.is_visible,
                    is_active=template_platform.is_active
                )
            )
        
        # Bulk create all platform records
        if platforms_to_create:
            ClientPlatformProgress.objects.bulk_create(platforms_to_create)
        
        return new_brand

    class Meta:
        verbose_name = "Brand Profile"
        verbose_name_plural = "Brand Profiles"
