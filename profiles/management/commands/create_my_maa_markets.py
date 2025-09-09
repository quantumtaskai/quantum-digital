import csv
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from profiles.models import BrandProfile
from dashboard.models import ClientPlatformProgress, ContentLink
import os


class Command(BaseCommand):
    help = 'Create My Maa Markets brand and import platform data from CSV'

    def handle(self, *args, **options):
        self.stdout.write('Creating My Maa Markets brand profile and importing data...')
        
        # Create or get user for My Maa Markets
        user, created = User.objects.get_or_create(
            username='my_maa_markets',
            defaults={
                'email': 'my.maa.markets@example.com',
                'first_name': 'My Maa',
                'last_name': 'Markets'
            }
        )
        
        if created:
            self.stdout.write(f'Created user: {user.username}')
        else:
            self.stdout.write(f'Using existing user: {user.username}')
        
        # Create or get brand profile
        brand, created = BrandProfile.objects.get_or_create(
            user=user,
            defaults={
                'brand_name': 'My Maa Markets',
                'primary_contact_first_name': 'My Maa',
                'primary_contact_last_name': 'Markets',
                'primary_official_email': 'contact@mymaamarkets.com',
                'primary_phone_number': '+1-234-567-8900',
                'brand_vision': 'To be the leading marketplace for fresh, organic, and specialty food items.',
                'brand_mission': 'Connecting communities with premium quality food products.',
                'brand_core_values': 'Quality, Freshness, Community, Sustainability',
                'brand_website': 'https://mymaamarkets.com',
            }
        )
        
        if created:
            self.stdout.write(f'Created brand profile: {brand.brand_name}')
        else:
            self.stdout.write(f'Using existing brand profile: {brand.brand_name}')
        
        # Platform mapping for CSV to database field names
        platform_mapping = {
            'Website- blogs': 'website_blogs',
            'Website Downloadable': 'website_downloadable', 
            'Google Business': 'google_business',
            'Linkedin': 'linkedin',
            'YouTube': 'youtube',
            'Tiktok': 'tiktok',
            'Instagram': 'instagram',
            'PinInterest': 'pinterest',
            'X (Twitter)': 'twitter',
            'Facebook': 'facebook',
            'Medium': 'medium',
            'Tumblr': 'tumblr',
            'Threads': 'threads',
            'Quora': 'quora',
            'Reddit': 'reddit',
            'Blue Sky': 'bluesky',
            'Email Marketing': 'email_marketing',
        }
        
        # CSV file path
        csv_file_path = '/home/amit/projects/quantum-digital/My Maa Markets - Sheet1.csv'
        
        updated_count = 0
        
        try:
            with open(csv_file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row in reader:
                    platform_name = row['Platform'].strip()
                    
                    # Skip the Website row (not a content platform)
                    if platform_name == 'Website':
                        continue
                    
                    # Get platform code from mapping
                    platform_code = platform_mapping.get(platform_name)
                    if not platform_code:
                        self.stdout.write(f'Warning: Unknown platform "{platform_name}"')
                        continue
                    
                    # Parse data from CSV
                    past_status = row['Past Status'].strip()
                    committed = int(row['Commited']) if row['Commited'] and row['Commited'] != '--' else 0
                    drafted = int(row['Drafted']) if row['Drafted'] and row['Drafted'] != '--' else 0
                    published = int(row['Published']) if row['Published'] and row['Published'] != '--' else 0
                    content_created = row['Content Created'].strip()
                    
                    # Determine platform status
                    is_active = past_status in ['Active', 'Already in Place']
                    
                    # Special cases
                    if past_status == 'Not Available':
                        is_active = False
                        is_visible = False
                    elif platform_name == 'Website- blogs' and committed > 0:
                        # Website blogs should be active if it has committed content
                        is_active = True
                        is_visible = True
                    else:
                        is_visible = is_active  # Show active platforms by default
                    
                    # Create notes with status info (content links are now separate ContentLink objects)
                    notes = f"Status: {past_status}"
                    
                    # Create or update platform progress
                    progress, created = ClientPlatformProgress.objects.get_or_create(
                        brand=brand,
                        platform=platform_code,
                        defaults={
                            'committed': committed,
                            'drafted': drafted, 
                            'published': published,
                            'notes': notes,
                            'is_visible': is_visible,
                            'is_active': is_active
                        }
                    )
                    
                    if not created:
                        # Update existing record
                        progress.committed = committed
                        progress.drafted = drafted
                        progress.published = published
                        progress.notes = notes
                        progress.is_visible = is_visible
                        progress.is_active = is_active
                        progress.save()
                    
                    updated_count += 1
                    
                    status = "created" if created else "updated"
                    self.stdout.write(f'{status.capitalize()}: {platform_name} - {committed}C/{drafted}D/{published}P ({"active" if is_active else "inactive"})')
        
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'CSV file not found: {csv_file_path}'))
            return
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error processing CSV: {str(e)}'))
            return
        
        # Create content links from CSV data
        self.stdout.write('Creating content links...')
        content_links_data = [
            # Extract content links from the CSV data
            ('website_blogs', 'View Content Plan', 'https://docs.google.com/document/d/1c0RsII34aNQJ4h9Y5AHgByUN7ps_P0bXKA5NL61uqjU/edit?usp=sharing'),
            ('google_business', 'View Setup Guide', 'https://docs.google.com/document/d/1hSQzW6w6C6qWw6UN7OpJUq6E30Ss5zzUubJxJEsC26c/edit?usp=sharing'),
            ('linkedin', 'View Content Strategy', 'https://docs.google.com/document/d/1CY2CiIdXTxirPnDmXBnuQgQBT0gncRK_cFQv1MmFOGk/edit?usp=sharing'),
            ('youtube', 'View Video Content', 'https://drive.google.com/drive/folders/1gz1Oy7r17SNGcTGGZ0H4HkR8c29xy1Fl?usp=drive_link'),
            ('tiktok', 'View Video Content', 'https://drive.google.com/drive/folders/1gz1Oy7r17SNGcTGGZ0H4HkR8c29xy1Fl?usp=drive_link'),
            ('twitter', 'View Content Strategy', 'https://docs.google.com/document/d/1dhUIMupIYOM1YVBedT8KsREFHPQwThZ4mLP0g4zjuLM/edit?usp=sharing'),
        ]
        
        link_count = 0
        for platform_code, title, url in content_links_data:
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
                status = "created" if created else "updated"
                self.stdout.write(f'  {status.capitalize()}: {platform_progress.get_platform_display()} - {title}')
                
            except ClientPlatformProgress.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f"Platform {platform_code} not found for content link")
                )
        
        self.stdout.write(f'✓ Created {link_count} content links')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully imported My Maa Markets data:\n'
                f'- Brand: {brand.brand_name}\n'
                f'- Platforms processed: {updated_count}\n'
                f'- User ID: {user.id}\n'
                f'- Brand ID: {brand.id}'
            )
        )