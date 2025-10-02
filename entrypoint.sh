#!/bin/bash
set -e

echo "========================================="
echo "Quantum Digital - Django Startup Script"
echo "========================================="

# Wait for database to be ready (PostgreSQL only)
echo "⏳ Checking database connection..."
python << END
import sys
import time
import os

db_url = os.getenv('DATABASE_URL', '')

# Only check PostgreSQL connections
if db_url and db_url.startswith('postgres'):
    try:
        import psycopg2
        from urllib.parse import urlparse

        result = urlparse(db_url)
        max_tries = 30
        tries = 0

        print("⏳ Waiting for PostgreSQL connection...")
        while tries < max_tries:
            try:
                conn = psycopg2.connect(
                    database=result.path[1:],
                    user=result.username,
                    password=result.password,
                    host=result.hostname,
                    port=result.port
                )
                conn.close()
                print("✅ PostgreSQL database is ready!")
                break
            except psycopg2.OperationalError as e:
                tries += 1
                print(f"⏳ Database not ready yet ({tries}/{max_tries})... waiting")
                time.sleep(2)

        if tries >= max_tries:
            print("❌ Could not connect to PostgreSQL after 30 attempts")
            sys.exit(1)
    except ImportError:
        print("⚠️  psycopg2 not available, skipping database check")
else:
    print("⚠️  Using SQLite or DATABASE_URL not set")
END

# Apply database migrations
echo "🔧 Applying database migrations..."
python manage.py migrate --noinput

# Create production site if needed
echo "🌐 Setting up production site..."
python manage.py setup_production --noinput || echo "⚠️  setup_production command not found or failed, continuing..."

# Collect static files
echo "📦 Collecting static files..."
python manage.py collectstatic --noinput --clear

# Create superuser if needed (optional, for first deployment)
# Uncomment and set environment variables if you want auto-superuser creation
# python manage.py shell << END
# from django.contrib.auth import get_user_model
# User = get_user_model()
# if not User.objects.filter(email='${DJANGO_SUPERUSER_EMAIL}').exists():
#     User.objects.create_superuser('${DJANGO_SUPERUSER_EMAIL}', '${DJANGO_SUPERUSER_PASSWORD}')
#     print('✅ Superuser created')
# END

echo "========================================="
echo "🚀 Starting Gunicorn server..."
echo "========================================="

# Start Gunicorn with production settings
exec gunicorn quantum_digital.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --threads 2 \
    --worker-class gthread \
    --worker-tmp-dir /dev/shm \
    --max-requests 1000 \
    --max-requests-jitter 50 \
    --timeout 60 \
    --graceful-timeout 30 \
    --keep-alive 5 \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    --capture-output \
    --enable-stdio-inheritance
