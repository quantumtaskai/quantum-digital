from django.db import models
from django.contrib.auth.models import User


class ClientPlatformProgress(models.Model):
    """Simple model to track content progress per client per platform"""
    
    PLATFORM_CHOICES = [
        ('website_blogs', 'Website Blogs'),
        ('website_downloadable', 'Website Downloadable'),
        ('google_business', 'Google Business'),
        ('linkedin', 'LinkedIn'),
        ('youtube', 'YouTube'),
        ('tiktok', 'TikTok'),
        ('instagram', 'Instagram'),
        ('pinterest', 'Pinterest'),
        ('twitter', 'Twitter/X'),
        ('facebook', 'Facebook'),
        ('medium', 'Medium'),
        ('tumblr', 'Tumblr'),
        ('threads', 'Threads'),
        ('quora', 'Quora'),
        ('reddit', 'Reddit'),
        ('bluesky', 'Blue Sky'),
        ('email_marketing', 'Email Marketing'),
        ('twitch', 'Twitch'),
        ('bereal', 'BeReal'),
        ('vimeo', 'Vimeo'),
        ('dailymotion', 'Daily Motion'),
        ('rumble', 'Rumble'),
        ('linktree', 'Linktree'),
    ]
    
    brand = models.ForeignKey('profiles.BrandProfile', on_delete=models.CASCADE, related_name='platform_progress')
    platform = models.CharField(max_length=50, choices=PLATFORM_CHOICES)
    
    # Content numbers - admin just updates these
    committed = models.IntegerField(default=0, help_text="Total content promised to client")
    drafted = models.IntegerField(default=0, help_text="Content currently drafted")
    published = models.IntegerField(default=0, help_text="Content completed and published")
    
    # Notes for admin team
    notes = models.TextField(blank=True, help_text="Internal notes for this platform")
    
    # Platform visibility control
    is_visible = models.BooleanField(default=True, help_text="Show this platform in dashboards")
    
    # Platform activity control
    is_active = models.BooleanField(default=True, help_text="Mark this platform as active or inactive")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['brand', 'platform']
        verbose_name = 'Client Platform Progress'
        verbose_name_plural = 'Client Platform Progress'
    
    def __str__(self):
        return f"{self.brand.brand_name} - {self.get_platform_display()}"
    
    @property
    def completion_percentage(self):
        if self.committed > 0:
            return round((self.published / self.committed) * 100, 1)
        return 0
    
    @property
    def draft_percentage(self):
        if self.committed > 0:
            return round((self.drafted / self.committed) * 100, 1)
        return 0


class ContentLink(models.Model):
    """Multiple content links per platform - admin can add as many as needed"""
    
    platform_progress = models.ForeignKey(ClientPlatformProgress, on_delete=models.CASCADE, related_name='content_links')
    title = models.CharField(max_length=200, help_text="Description of this link (e.g., 'Content Calendar', 'Draft Folder')")
    url = models.URLField(help_text="Google Doc, Drive folder, or any resource URL")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.platform_progress} - {self.title}"
    
    class Meta:
        verbose_name = 'Content Link'
        verbose_name_plural = 'Content Links'
