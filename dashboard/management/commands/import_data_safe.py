from django.core.management.base import BaseCommand
from django.core import serializers
from django.db import transaction
import json


class Command(BaseCommand):
    help = 'Safely import data excluding conflicting models'
    
    def add_arguments(self, parser):
        parser.add_argument('fixture_file', type=str, help='Path to the fixture file')
        parser.add_argument(
            '--exclude-models',
            nargs='*',
            default=['sites.site'],
            help='Models to exclude from import (default: sites.site)'
        )
    
    def handle(self, *args, **options):
        fixture_file = options['fixture_file']
        exclude_models = options['exclude_models']
        
        self.stdout.write(f'Importing data from: {fixture_file}')
        self.stdout.write(f'Excluding models: {exclude_models}')
        
        try:
            with open(fixture_file, 'r') as f:
                data = json.load(f)
            
            # Filter out excluded models
            filtered_data = []
            excluded_count = 0
            
            for item in data:
                if item.get('model') in exclude_models:
                    excluded_count += 1
                    continue
                filtered_data.append(item)
            
            self.stdout.write(f'Original objects: {len(data)}')
            self.stdout.write(f'Excluded objects: {excluded_count}')
            self.stdout.write(f'Objects to import: {len(filtered_data)}')
            
            # Import the filtered data
            with transaction.atomic():
                for obj_data in serializers.deserialize('json', json.dumps(filtered_data)):
                    try:
                        obj_data.save()
                    except Exception as e:
                        self.stdout.write(
                            self.style.WARNING(
                                f'⚠️  Warning: Failed to import {obj_data.object}: {e}'
                            )
                        )
                        # Continue with other objects
                        continue
            
            self.stdout.write(
                self.style.SUCCESS(f'✅ Successfully imported {len(filtered_data)} objects!')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error importing data: {e}')
            )
            raise