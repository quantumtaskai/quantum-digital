from django import forms
from .models import BrandProfile


class BrandProfileForm(forms.ModelForm):
    class Meta:
        model = BrandProfile
        exclude = ['user', 'created_at', 'updated_at']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Prefill required fields for testing
        self.fields['brand_name'].initial = 'Test Brand Co.'
        self.fields['primary_contact_first_name'].initial = 'John'
        self.fields['primary_contact_last_name'].initial = 'Doe'
        self.fields['primary_official_email'].initial = 'john@testbrand.com'
        self.fields['primary_phone_number'].initial = '(555) 123-4567'
        self.fields['brand_vision'].initial = 'To revolutionize digital branding through innovative solutions.'
        self.fields['brand_mission'].initial = 'We empower brands to connect with their audience through meaningful digital experiences.'
        self.fields['brand_core_values'].initial = 'Innovation, Quality, Customer Focus, Integrity'
        widgets = {
            'brand_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your brand name'}),
            'primary_contact_first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'primary_contact_last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'primary_official_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'official@email.com'}),
            'primary_phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(123) 456-7890'}),
            'secondary_contact_first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name (Optional)'}),
            'secondary_contact_last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name (Optional)'}),
            'secondary_official_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'official@email.com (Optional)'}),
            'secondary_phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(123) 456-7890 (Optional)'}),
            'brand_vision': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describe your brand vision...'}),
            'brand_mission': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describe your brand mission...'}),
            'brand_core_values': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'List your core values...'}),
            'brand_visual_verbal_dna_guidelines': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://example.com/guidelines.pdf'}),
            'brand_website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://yourwebsite.com'}),
            'brand_presence': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Describe your current brand presence...'}),
            'website_traffic_kpis': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 1000 visitors/month'}),
            'instagram_reach_kpis': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 2.0M reach'}),
            'google_sepr_rank_kpis': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Page 1 for main keywords'}),
            'review_rating_kpis': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 4.4/5 stars'}),
            'social_media_posts_per_week_kpis': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 5 posts'}),
            'videos_per_week_kpis': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 3 videos'}),
            'shorts_per_week_kpis': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 4 shorts'}),
            'strengths': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'List your brand strengths...'}),
            'weaknesses': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'List your brand weaknesses...'}),
            'opportunities': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'List market opportunities...'}),
            'threats': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'List potential threats...'}),
            'instagram': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://instagram.com/yourprofile'}),
            'facebook': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://facebook.com/yourpage'}),
            'twitter': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://twitter.com/yourhandle'}),
            'linkedin': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://linkedin.com/company/yourcompany'}),
            'tiktok': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://tiktok.com/@yourhandle'}),
            'youtube': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://youtube.com/@yourchannel'}),
            'pinterest': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://pinterest.com/yourprofile'}),
            'snapchat': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://snapchat.com/add/yourhandle'}),
            'telegram': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://t.me/yourhandle'}),
            'medium': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://medium.com/@yourhandle'}),
            'quora': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://quora.com/profile/yourprofile'}),
            'reddit': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://reddit.com/u/yourhandle'}),
            'tumblr': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://yourhandle.tumblr.com'}),
            'threads': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://threads.net/@yourhandle'}),
            'bluesky': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://bsky.app/profile/yourhandle'}),
            'whatsapp_business': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'WhatsApp Business link'}),
            'website_blogs': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://yourwebsite.com/blog'}),
            'top_10_partners': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'List your top 10 partners (one per line)'}),
            'top_10_competitors': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'List your top 10 competitors (one per line)'}),
            'additional_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Any additional information worth mentioning...'}),
        }