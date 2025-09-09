import csv
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from profiles.models import BrandProfile
from dashboard.models import ClientPlatformProgress, ContentLink
import os


class Command(BaseCommand):
    help = 'Create Digital Marketing TTG brand and import platform data from CSV'

    def handle(self, *args, **options):
        self.stdout.write('Creating Digital Marketing TTG brand profile and importing data...')
        
        # Create or get user for Digital Marketing TTG
        user, created = User.objects.get_or_create(
            username='ttg_digital',
            defaults={
                'email': 'ttg.digital@example.com',
                'first_name': 'Digital Marketing',
                'last_name': 'TTG'
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
                'brand_name': 'Digital Marketing TTG',
                'primary_contact_first_name': 'Digital Marketing',
                'primary_contact_last_name': 'TTG',
                'primary_official_email': 'contact@ttgdigital.com',
                'primary_phone_number': '+1-555-TTG-DIGI',
                'brand_vision': 'To transform businesses through strategic digital marketing excellence.',
                'brand_mission': 'Delivering cutting-edge digital marketing solutions that accelerate business growth.',
                'brand_core_values': 'Excellence, Innovation, Partnership, Results',
                'brand_website': 'https://ttgdigital.com',
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
        csv_file_path = '/home/amit/projects/quantum-digital/Digital Marketing TTG - Platforms.csv'
        
        updated_count = 0
        
        try:
            with open(csv_file_path, 'r', encoding='utf-8') as file:
                # Skip the first row (header info) and read from row 2
                lines = file.readlines()
                csv_data = lines[1:]  # Skip first line
                
                reader = csv.DictReader(csv_data)
                
                for row in reader:
                    platform_name = row['Platform'].strip()
                    
                    # Skip empty rows or Website row
                    if not platform_name or platform_name == 'Website':
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
                    is_active = past_status == 'Active'
                    
                    # Special case for Website Blogs with high committed content
                    if platform_name == 'Website- blogs' and committed > 0:
                        is_active = True
                    
                    # Special case for Google Business (Not Available)
                    if past_status == 'Not Available':
                        is_active = False
                        is_visible = False
                    else:
                        is_visible = is_active  # Show active platforms by default
                    
                    # Create notes with status info
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
        
        # Create content links from CSV data (TTG has different Google Doc URLs than Farway)
        self.stdout.write('Creating content links...')
        content_links_data = [
            # Content Created Links (Google Docs from CSV - TTG specific URLs)
            ('website_blogs', 'View Content Plan', 'https://docs.google.com/document/d/13JSIXHTsARsDDTkbEegV3VN3vpvBaldHqa9XLQjTb1c/edit?usp=drive_link'),
            ('google_business', 'View Setup Guide', 'https://docs.google.com/document/d/1rdSnXZIZnxQp9JXLPwFQHdxz_jUj4JF-_VJ_23WSu8k/edit?usp=drive_link'),
            ('linkedin', 'View Content Strategy', 'https://docs.google.com/document/d/1TH_uIxnpil-Qfq-olxqvAwymSFLF6Kq3MQZLqLUUaik/edit?usp=drive_link'),
            ('youtube', 'View Video Content', 'https://drive.google.com/drive/folders/12sqQc9RSHFNcFKAI2CoB1aZd8-BYdM8N?usp=drive_link'),
            ('instagram', 'View Content Plan', 'https://docs.google.com/document/d/1DvL1LqnQuxcd2DYExyEATZ--7kCA8nMTGVDk_UEVKYM/edit?usp=drive_link'),
            ('pinterest', 'View Content Plan', 'https://docs.google.com/document/d/1hI6QYAvW7ZLrVxl6ifJViaXsCP3u3q70BpQyLgcWqOo/edit?usp=drive_link'),
            ('twitter', 'View Content Strategy', 'https://docs.google.com/document/d/1MoloWzcC6vcZQ48fRo4u7RfKe2Rs76dvqQFDTY6ay3M/edit?usp=drive_link'),
            ('facebook', 'View Content Plan', 'https://docs.google.com/document/d/1CxUze-vctsXMw9UIWEtWFPAvvcd5XfvlRe9q26gw6Fw/edit?usp=drive_link'),
            ('medium', 'View Content Plan', 'https://docs.google.com/document/d/1rjiB3V_xxt2tfwg9SVbbMUWSlMbskIqKbJ6BMLH4vKs/edit?usp=drive_link'),
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
                f'Successfully imported Digital Marketing TTG data:\n'
                f'- Brand: {brand.brand_name}\n'
                f'- Platforms processed: {updated_count}\n'
                f'- User ID: {user.id}\n'
                f'- Brand ID: {brand.id}'
            )
        )