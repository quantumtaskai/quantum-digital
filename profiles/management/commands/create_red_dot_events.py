from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction
from profiles.models import BrandProfile
from dashboard.models import ClientPlatformProgress, ContentLink
import uuid


class Command(BaseCommand):
    help = 'Create Red Dot Events brand with complete platform data matching the dashboard screenshot'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be created without actually creating records',
        )

    def handle(self, *args, **options):
        if options['dry_run']:
            self.stdout.write(self.style.WARNING("[DRY RUN] Would create Red Dot Events brand with platform data"))
            return

        try:
            with transaction.atomic():
                # Create user for Red Dot Events
                user, created = User.objects.get_or_create(
                    username='reddotevents',
                    defaults={
                        'email': 'contact@reddotevents.com',
                        'first_name': 'Red Dot',
                        'last_name': 'Events'
                    }
                )
                
                if created:
                    user.set_password('password123')
                    user.save()
                    self.stdout.write(f"✓ Created user: {user.username}")
                else:
                    self.stdout.write(f"✓ User already exists: {user.username}")

                # Create brand profile
                brand, created = BrandProfile.objects.get_or_create(
                    user=user,
                    defaults={
                        'brand_name': 'Red Dot Events',
                        'primary_contact_first_name': 'Sarah',
                        'primary_contact_last_name': 'Johnson',
                        'primary_official_email': 'sarah@reddotevents.com',
                        'primary_phone_number': '+1-555-0123',
                        'brand_website': 'https://reddotevents.com',
                        'brand_vision': 'Creating unforgettable experiences through innovative event planning and digital marketing',
                        'brand_mission': 'To deliver exceptional event experiences that exceed expectations through strategic digital presence',
                        'brand_core_values': 'Creativity, Excellence, Innovation, Customer Focus, Digital Excellence',
                        'is_public_enabled': True,
                        'public_uuid': uuid.UUID('12345678-1234-5678-9abc-123456789abc')
                    }
                )
                
                if created:
                    self.stdout.write(f"✓ Created brand: {brand.brand_name}")
                    # Auto-create platform records (will be updated below)
                    created_count = brand.create_default_platform_records()
                    self.stdout.write(f"✓ Created {created_count} default platform records")
                else:
                    self.stdout.write(f"✓ Brand already exists: {brand.brand_name}")

                # Platform data matching the screenshot (visible platforms have committed > 0)
                platform_data = [
                    # Visible platforms matching screenshot - 13 total
                    ('website_blogs', 50, 10, 0, 'Professional blog content for event marketing', True),
                    ('website_downloadable', 10, 1, 0, 'Event guides and downloadable resources', True),
                    ('google_business', 100, 11, 0, 'Google Business profile optimization', True),
                    ('linkedin', 45, 10, 0, 'Professional networking and B2B content', True),
                    ('youtube', 5, 1, 0, 'Event highlight videos and tutorials', True),
                    ('tiktok', 10, 1, 3, 'Short-form event highlights and behind-the-scenes', True),
                    ('instagram', 180, 45, 3, 'Visual event content, stories, and reels', True),
                    ('pinterest', 180, 0, 4, 'Event inspiration boards and planning content', True),
                    ('twitter', 180, 10, 4, 'Real-time event updates and engagement', True),
                    ('facebook', 180, 10, 3, 'Community building and event promotion', True),
                    ('medium', 30, 0, 2, 'Long-form thought leadership articles', True),
                    ('threads', 30, 0, 3, 'Text-based social engagement', True),
                    ('tumblr', 30, 10, 4, 'Creative visual content and storytelling', True),
                    
                    # Hidden platforms - not relevant for Red Dot Events
                    ('quora', 0, 0, 0, 'Q&A engagement', False),
                    ('reddit', 0, 0, 0, 'Community discussions', False),
                    ('bluesky', 0, 0, 3, 'Alternative social platform', False),
                    ('email_marketing', 0, 0, 0, 'Email campaigns', False),
                    ('twitch', 0, 0, 0, 'Live streaming', False),
                    ('bereal', 0, 0, 0, 'Authentic moments sharing', False),
                    ('vimeo', 0, 0, 0, 'Professional video hosting', False),
                    ('dailymotion', 0, 0, 0, 'Video content sharing', False),
                    ('rumble', 0, 0, 0, 'Alternative video platform', False),
                ]

                # Update platform progress data
                updated_count = 0
                for platform_code, committed, drafted, published, notes, is_visible in platform_data:
                    progress, created = ClientPlatformProgress.objects.get_or_create(
                        brand=brand,
                        platform=platform_code,
                        defaults={
                            'committed': committed,
                            'drafted': drafted, 
                            'published': published,
                            'notes': notes,
                            'is_visible': is_visible,
                            'is_active': True  # Default for new platforms
                        }
                    )
                    
                    if not created:
                        # Update existing record - preserve is_active value
                        progress.committed = committed
                        progress.drafted = drafted
                        progress.published = published
                        progress.notes = notes
                        progress.is_visible = is_visible
                        # Note: is_active is NOT updated to preserve manual changes
                        progress.save()
                    
                    updated_count += 1

                self.stdout.write(f"✓ Updated {updated_count} platform progress records")

                # Create content links with real URLs from CSV
                content_links = [
                    # Content Created Links (Google Docs from CSV)
                    ('website_blogs', 'View Content Plan', 'https://docs.google.com/document/d/13JSIXHTsARsDDTkbEegV3VN3vpvBaldHqa9XLQjTb1c/edit?usp=drive_link'),
                    ('website_downloadable', 'View Content Plan', 'https://docs.google.com/document/d/1wNXUmUtpAIFkJKSsigESAWQ3iyfiBaMO-upq6PHseRg/edit?usp=drive_link'),
                    ('google_business', 'View Content Plan', 'https://docs.google.com/document/d/13CfHO2BSMQ-hIZ-Ix05vzKa6c02Cq1zoxN4TlquH7Sw/edit?usp=drive_link'),
                    ('linkedin', 'View Content Plan', 'https://docs.google.com/document/d/1nMDbcpbB0bQ90P8guHZE3iy6m827Jcve4DqV3uJYWFU/edit?usp=drive_link'),
                    ('youtube', 'View Content Plan', 'https://drive.google.com/drive/folders/1VjLK1PtsG1A4cdGsDmRWRdNkr3AJA2Md?usp=drive_link'),
                    ('instagram', 'View Content Plan', 'https://docs.google.com/document/d/1wbCr8wavITL10BnEAdURYDKzqgsIEbPnoyo6vjnD9co/edit?usp=drive_link'),
                    ('pinterest', 'View Content Plan', 'https://docs.google.com/document/d/1qmdzoOdBIFu-ZKsmVfg85ugij4isTlN7rzeMRp3pFOU/edit?usp=drive_link'),
                    ('twitter', 'View Content Plan', 'https://docs.google.com/document/d/106-J7VxbGOcmcUYL32L4Wx9Cefk8FawMA0Vi9rbHITI/edit?usp=drive_link'),
                    ('facebook', 'View Content Plan', 'https://docs.google.com/document/d/1cw5TJhTsuIbNSEkMYGp6xrhHBTPQi6J1QNGKrE_97fU/edit?usp=drive_link'),
                    ('medium', 'View Content Plan', 'https://docs.google.com/document/d/1zxVTTTxG3-M5NIQJwElBlmD9kusruLawBJHvpsc8a5E/edit?usp=drive_link'),
                    ('threads', 'View Content Plan', 'https://docs.google.com/document/d/16rUK1zYdRsW2OcvCpcxIHyYNfF2dPL9fVIvoUkm_pIw/edit?usp=drive_link'),
                    
                    # Platform Links (Social Media URLs from CSV)
                    ('linkedin', 'Visit Platform', 'https://www.linkedin.com/company/red-dot-events-exhibitions-sp-llc/'),
                    ('instagram', 'Visit Platform', 'https://www.instagram.com/reddot_event/'),
                    ('pinterest', 'Visit Platform', 'https://www.pinterest.com/reddoteventssocial/'),
                    ('twitter', 'Visit Platform', 'https://x.com/EventsRedd60567'),
                    ('facebook', 'Visit Platform', 'https://www.facebook.com/people/Red-Dot-Events/61560412568254/'),
                    ('medium', 'Visit Platform', 'https://medium.com/@reddotevents.social'),
                    ('tumblr', 'Visit Platform', 'https://www.tumblr.com/blog/reddotevents'),
                ]

                link_count = 0
                for platform_code, title, url in content_links:
                    try:
                        platform_progress = ClientPlatformProgress.objects.get(
                            brand=brand, 
                            platform=platform_code
                        )
                        
                        link, created = ContentLink.objects.get_or_create(
                            platform_progress=platform_progress,
                            title=title,
                            defaults={'url': url}
                        )
                        
                        if not created:
                            # Update existing link URL
                            link.url = url
                            link.save()
                        
                        link_count += 1
                    except ClientPlatformProgress.DoesNotExist:
                        self.stdout.write(
                            self.style.WARNING(f"Platform {platform_code} not found")
                        )

                self.stdout.write(f"✓ Created {link_count} content links")

                # Summary
                total_committed = sum(data[1] for data in platform_data)
                total_drafted = sum(data[2] for data in platform_data) 
                total_published = sum(data[3] for data in platform_data)
                active_platforms = sum(1 for data in platform_data if data[1] > 0)
                visible_platforms = sum(1 for data in platform_data if data[5])  # is_visible is index 5
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f"\n🎉 Red Dot Events brand created successfully!"
                        f"\n   Brand ID: {brand.id}"
                        f"\n   Public UUID: {brand.public_uuid}"
                        f"\n   Total Committed: {total_committed}"
                        f"\n   Total Drafted: {total_drafted}"
                        f"\n   Total Published: {total_published}"
                        f"\n   Active Platforms: {active_platforms}"
                        f"\n   Visible Platforms: {visible_platforms} (matching screenshot)"
                        f"\n   Hidden Platforms: {len(platform_data) - visible_platforms}"
                    )
                )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Error creating Red Dot Events: {str(e)}")
            )
            raise