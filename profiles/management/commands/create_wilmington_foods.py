import csv
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from profiles.models import BrandProfile
from dashboard.models import ClientPlatformProgress, ContentLink
import os


class Command(BaseCommand):
    help = 'Create Wilmington Foods brand and import platform data from CSV'

    def handle(self, *args, **options):
        self.stdout.write('Creating Wilmington Foods brand profile and importing data...')
        
        # Create or get user for Wilmington Foods
        user, created = User.objects.get_or_create(
            username='wilmington_foods',
            defaults={
                'email': 'wilmington.foods@example.com',
                'first_name': 'Wilmington',
                'last_name': 'Foods'
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
                'brand_name': 'Wilmington Foods',
                'primary_contact_first_name': 'Wilmington',
                'primary_contact_last_name': 'Foods',
                'primary_official_email': 'contact@wilmingtonfoods.com',
                'primary_phone_number': '+1-302-555-0100',
                'brand_vision': 'To provide the finest quality food products to our community.',
                'brand_mission': 'Bringing fresh, quality food products to families across Delaware.',
                'brand_core_values': 'Quality, Freshness, Community, Trust',
                'brand_website': 'https://wilmingtonfoods.com',
            }
        )
        
        if created:
            self.stdout.write(f'Created brand profile: {brand.brand_name}')
        else:
            self.stdout.write(f'Using existing brand profile: {brand.brand_name}')
        
        # Platform mapping for CSV to database field names
        platform_mapping = {
            'Website- blogs': 'website_blogs',
            'Google Business': 'google_business',
            'Linkedin': 'linkedin',
            'YouTube': 'youtube',
            'Tiktok': 'tiktok',
            'Instagram': 'instagram',
            'PinInterest': 'pinterest',
            'X (Twitter)': 'twitter',
            'Facebook': 'facebook',
            'Medium': 'medium',
            'Threads': 'threads',
            'Tumblr': 'tumblr',
        }
        
        # CSV file path
        csv_file_path = '/home/amit/projects/quantum-digital/wilmingtonfoods - Sheet1 (1).csv'
        
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
                    platform_links = row['Platform Links'].strip()
                    
                    # Determine platform status
                    is_active = past_status == 'Active'
                    is_visible = is_active  # Show active platforms by default
                    
                    # Create notes with status info
                    notes = f"Status: {past_status}"
                    if platform_links:
                        notes += f"\nPlatform URL: {platform_links}"
                    
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
            # Content Created Links (Google Docs from CSV)
            ('website_blogs', 'View Content Plan', 'https://docs.google.com/document/d/13JSIXHTsARsDDTkbEegV3VN3vpvBaldHqa9XLQjTb1c/edit?usp=drive_link'),
            ('google_business', 'View Content Plan', 'https://docs.google.com/document/d/13CfHO2BSMQ-hIZ-Ix05vzKa6c02Cq1zoxN4TlquH7Sw/edit?usp=drive_link'),
            ('linkedin', 'View Content Plan', 'https://docs.google.com/document/d/1nMDbcpbB0bQ90P8guHZE3iy6m827Jcve4DqV3uJYWFU/edit?usp=drive_link'),
            ('youtube', 'View Video Content', 'https://drive.google.com/drive/folders/1VjLK1PtsG1A4cdGsDmRWRdNkr3AJA2Md?usp=drive_link'),
            ('instagram', 'View Content Plan', 'https://docs.google.com/document/d/1wbCr8wavITL10BnEAdURYDKzqgsIEbPnoyo6vjnD9co/edit?usp=drive_link'),
            ('pinterest', 'View Content Plan', 'https://docs.google.com/document/d/1qmdzoOdBIFu-ZKsmVfg85ugij4isTlN7rzeMRp3pFOU/edit?usp=drive_link'),
            ('twitter', 'View Content Plan', 'https://docs.google.com/document/d/106-J7VxbGOcmcUYL32L4Wx9Cefk8FawMA0Vi9rbHITI/edit?usp=drive_link'),
            ('facebook', 'View Content Plan', 'https://docs.google.com/document/d/1cw5TJhTsuIbNSEkMYGp6xrhHBTPQi6J1QNGKrE_97fU/edit?usp=drive_link'),
            ('medium', 'View Content Plan', 'https://docs.google.com/document/d/1zxVTTTxG3-M5NIQJwElBlmD9kusruLawBJHvpsc8a5E/edit?usp=drive_link'),
            ('threads', 'View Content Plan', 'https://docs.google.com/document/d/16rUK1zYdRsW2OcvCpcxIHyYNfF2dPL9fVIvoUkm_pIw/edit?usp=drive_link'),
            
            # Platform Links (Social Media URLs from CSV)
            ('linkedin', 'Visit Platform', 'https://www.linkedin.com/company/wilmington-foods/'),
            ('instagram', 'Visit Platform', 'https://www.instagram.com/wilmingtonfoods/'),
            ('twitter', 'Visit Platform', 'https://x.com/WilmingtonFoods'),
            ('facebook', 'Visit Platform', 'https://www.facebook.com/WilmingtonFoods/'),
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
                f'Successfully imported Wilmington Foods data:\n'
                f'- Brand: {brand.brand_name}\n'
                f'- Platforms processed: {updated_count}\n'
                f'- User ID: {user.id}\n'
                f'- Brand ID: {brand.id}'
            )
        )