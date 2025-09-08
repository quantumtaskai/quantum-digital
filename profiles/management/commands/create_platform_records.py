from django.core.management.base import BaseCommand
from django.db import transaction
from profiles.models import BrandProfile
from dashboard.models import ClientPlatformProgress


class Command(BaseCommand):
    help = 'Create platform progress records for existing brands that don\'t have them'

    def add_arguments(self, parser):
        parser.add_argument(
            '--brand-id',
            type=int,
            help='Create platform records for specific brand ID only',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be created without actually creating records',
        )

    def handle(self, *args, **options):
        # Get brands to process
        if options['brand_id']:
            try:
                brands = [BrandProfile.objects.get(id=options['brand_id'])]
                self.stdout.write(f"Processing single brand: {brands[0].brand_name}")
            except BrandProfile.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Brand with ID {options["brand_id"]} does not exist')
                )
                return
        else:
            brands = BrandProfile.objects.all()
            self.stdout.write(f"Processing all {brands.count()} brands")

        total_created = 0
        brands_updated = 0

        with transaction.atomic():
            for brand in brands:
                # Check how many platform records this brand already has
                existing_count = ClientPlatformProgress.objects.filter(brand=brand).count()
                total_platforms = len(ClientPlatformProgress.PLATFORM_CHOICES)
                
                if existing_count < total_platforms:
                    missing_count = total_platforms - existing_count
                    
                    if options['dry_run']:
                        self.stdout.write(
                            f"[DRY RUN] Would create {missing_count} platform records for {brand.brand_name}"
                        )
                        total_created += missing_count
                        brands_updated += 1
                    else:
                        # Create missing platform records
                        created_count = brand.create_default_platform_records()
                        
                        if created_count > 0:
                            self.stdout.write(
                                self.style.SUCCESS(
                                    f"Created {created_count} platform records for {brand.brand_name}"
                                )
                            )
                            total_created += created_count
                            brands_updated += 1
                        else:
                            self.stdout.write(
                                f"No new records needed for {brand.brand_name} (already has {existing_count} platforms)"
                            )
                else:
                    self.stdout.write(
                        f"✓ {brand.brand_name} already has all {total_platforms} platform records"
                    )

        # Summary
        if options['dry_run']:
            self.stdout.write(
                self.style.WARNING(
                    f"\n[DRY RUN] Would create {total_created} platform records across {brands_updated} brands"
                )
            )
            self.stdout.write("Run without --dry-run to actually create the records")
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f"\nCompleted! Created {total_created} platform records across {brands_updated} brands"
                )
            )
            
            if brands_updated == 0:
                self.stdout.write("All brands already have complete platform records.")