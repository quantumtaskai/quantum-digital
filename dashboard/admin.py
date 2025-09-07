from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import ClientPlatformProgress, ContentLink


class ContentLinkInline(admin.TabularInline):
    """Inline to add multiple content links per platform"""
    model = ContentLink
    extra = 1
    fields = ['title', 'url']
    verbose_name = "Content Link"
    verbose_name_plural = "Content Links"


@admin.register(ClientPlatformProgress)
class ClientPlatformProgressAdmin(admin.ModelAdmin):
    """Super simple admin interface for updating platform progress"""
    
    list_display = ['brand_link', 'platform_display', 'committed', 'drafted', 'published', 'progress_bar', 'links_count']
    list_filter = ['platform', 'brand']
    search_fields = ['brand__brand_name', 'brand__user__username', 'brand__user__email']
    inlines = [ContentLinkInline]
    
    fieldsets = (
        ('Client & Platform', {
            'fields': ('brand', 'platform')
        }),
        ('Content Numbers', {
            'fields': ('committed', 'drafted', 'published'),
            'description': 'Just update these numbers as content gets completed'
        }),
        ('Notes', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )
    
    def brand_link(self, obj):
        """Link to brand admin page"""
        return format_html('<a href="{}">{}</a>', 
                          reverse('admin:profiles_brandprofile_change', args=[obj.brand.pk]), 
                          obj.brand.brand_name)
    brand_link.short_description = 'Brand'
    
    def platform_display(self, obj):
        """Show platform name nicely"""
        return obj.get_platform_display()
    platform_display.short_description = 'Platform'
    
    def progress_bar(self, obj):
        """Visual progress bar"""
        if obj.committed > 0:
            percentage = obj.completion_percentage
            draft_percentage = obj.draft_percentage
            
            return format_html(
                '<div style="width: 120px;">'
                '<div style="background: #e9ecef; border-radius: 3px; height: 16px;">'
                '<div style="background: #28a745; width: {}%; height: 16px; border-radius: 3px;"></div>'
                '</div>'
                '<small>{}% published, {}% drafted</small>'
                '</div>',
                percentage, percentage, draft_percentage
            )
        return '-'
    progress_bar.short_description = 'Progress'
    
    def links_count(self, obj):
        """Show number of content links"""
        count = obj.content_links.count()
        if count > 0:
            return format_html('<span class="badge" style="background: #17a2b8; color: white;">{} links</span>', count)
        return 'No links'
    links_count.short_description = 'Content Links'
    
    # Make it easy to create progress records for all platforms
    actions = ['create_all_platforms']
    
    def create_all_platforms(self, request, queryset):
        """Create platform progress records for selected brands across all platforms"""
        platform_choices = ClientPlatformProgress.PLATFORM_CHOICES
        created_count = 0
        
        for progress in queryset:
            brand = progress.brand
            for platform_code, platform_name in platform_choices:
                obj, created = ClientPlatformProgress.objects.get_or_create(
                    brand=brand,
                    platform=platform_code,
                    defaults={'committed': 0, 'drafted': 0, 'published': 0}
                )
                if created:
                    created_count += 1
        
        self.message_user(request, f'Created {created_count} platform progress records')
    create_all_platforms.short_description = "Create all platforms for selected brands"


@admin.register(ContentLink)
class ContentLinkAdmin(admin.ModelAdmin):
    """Manage content links separately if needed"""
    list_display = ['platform_progress', 'title', 'url_link']
    list_filter = ['platform_progress__platform', 'platform_progress__brand']
    search_fields = ['title', 'platform_progress__brand__brand_name']
    
    def url_link(self, obj):
        return format_html('<a href="{}" target="_blank">Open Link</a>', obj.url)
    url_link.short_description = 'Link'
