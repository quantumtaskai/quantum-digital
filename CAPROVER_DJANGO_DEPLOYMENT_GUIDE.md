# Complete Guide: Deploying Django Apps on CapRover

## Prerequisites
- CapRover installed and running on your VPS
- Git repository with your Django project
- Basic understanding of Django project structure

---

## Part 1: Prepare Your Django Project

### 1.1 Required Files Structure
Your Django project should have these files in the root directory:
```
your-django-project/
├── manage.py
├── requirements.txt
├── captain-definition
├── Dockerfile.captain
├── .dockerignore
├── your_project/
│   ├── settings.py
│   ├── wsgi.py
│   └── ...
└── your_apps/
```

### 1.2 Create `requirements.txt`
```txt
Django>=4.0
gunicorn>=21.0
psycopg2-binary>=2.9
whitenoise>=6.0
python-dotenv>=1.0
dj-database-url>=2.0
```

### 1.3 Create `captain-definition`
```json
{
  "schemaVersion": 2,
  "dockerfilePath": "./Dockerfile.captain"
}
```

### 1.4 Create `Dockerfile.captain`
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Create a non-root user
RUN useradd --create-home --shell /bin/bash app
RUN chown -R app:app /app
USER app

# Expose port
EXPOSE 80

# Start the application
CMD ["gunicorn", "--bind", "0.0.0.0:80", "your_project.wsgi:application"]
```

### 1.5 Create `.dockerignore`
```
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
.env
.venv/
.git/
.gitignore
README.md
.DS_Store
.coverage
.pytest_cache/
.tox/
db.sqlite3
*.log
node_modules/
.vscode/
.idea/
```

### 1.6 Update Django Settings

#### In `settings.py`:
```python
import os
from dotenv import load_dotenv
import dj_database_url

load_dotenv()

# Security settings
SECRET_KEY = os.getenv('SECRET_KEY', 'your-fallback-key')
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# CapRover auto-detection
if os.getenv('CAPROVER_GIT_COMMIT_SHA'):
    ALLOWED_HOSTS = ['*']  # Restrict this in production

# Database configuration
if os.getenv('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.parse(os.getenv('DATABASE_URL'))
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Static files (WhiteNoise)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this
    # ... your other middleware
]

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

---

## Part 2: Deploy PostgreSQL Database

### 2.1 Deploy PostgreSQL
1. **CapRover Dashboard** → **Apps** → **One-Click Apps/Databases**
2. **Search:** `PostgreSQL`
3. **Configure:**
   - App Name: `postgres-db` (or `yourapp-db`)
   - Version: `14.5` (recommended)
   - Username: `your_db_user`
   - Password: `secure_password_123`
   - Default Database: `postgres`
4. **Click Deploy**

### 2.2 Note Connection Details
After deployment, note the internal hostname:
- Format: `srv-captain--postgres-db:5432`
- Full URL: `postgres://username:password@srv-captain--postgres-db:5432/database_name`

---

## Part 3: Deploy Django Application

### 3.1 Create Django App
1. **CapRover Dashboard** → **Apps** → **Create New App**
2. **App Name:** `your-django-app`
3. **Check:** "Has Persistent Data" (if storing files)
4. **Click:** "Create New App"

### 3.2 Configure Git Deployment
1. **Go to your app** → **Deployment tab**
2. **Select:** "Method 3: Deploy from Github/Bitbucket/Gitlab"
3. **Repository URL:** `https://github.com/username/your-repo.git`
4. **Branch:** `main`
5. **Click:** "Save & Update"

### 3.3 Set Environment Variables
**Go to:** App Configs → Environment Variables

**Add these variables:**
```
SECRET_KEY = your-generated-secret-key
DEBUG = false
ALLOWED_HOSTS = your-app.captain.your-domain.com
DATABASE_URL = postgres://your_db_user:secure_password_123@srv-captain--postgres-db:5432/postgres
```

**Generate SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 3.4 Deploy Application
1. **Deployment tab** → **Force Build**
2. **Monitor logs** for successful deployment

---

## Part 4: Post-Deployment Setup

### 4.1 Install Portainer (For Easy Management)
1. **Apps** → **One-Click Apps** → Search `Portainer`
2. **Deploy** with default settings
3. **Access:** `https://portainer.captain.your-domain.com`
4. **Create admin account**

### 4.2 Run Django Setup Commands

#### Via Portainer:
1. **Containers** → Find your Django container
2. **Console** → `/bin/bash` → **Connect**
3. **Run commands:**
```bash
python manage.py migrate
python manage.py createsuperuser --noinput --username admin --email admin@example.com
python manage.py shell -c "from django.contrib.auth.models import User; u=User.objects.get(username='admin'); u.set_password('admin123'); u.save(); print('Password set')"
```

#### Via SSH (Alternative):
```bash
# SSH into your server
ssh root@your-server-ip

# Find container ID
docker ps | grep your-django-app

# Run commands
docker exec -it [container-id] python manage.py migrate
docker exec -it [container-id] python manage.py createsuperuser
```

### 4.3 Install pgAdmin (Database Management)
1. **Apps** → **One-Click Apps** → Search `pgAdmin`
2. **Configure:**
   - Email: `admin@example.com`
   - Password: `secure_password`
3. **Deploy**
4. **Access:** `https://pgadmin.captain.your-domain.com`

### 4.4 Connect pgAdmin to PostgreSQL
1. **Login to pgAdmin**
2. **Add Server:**
   - Name: `Your App DB`
   - Host: `srv-captain--postgres-db`
   - Port: `5432`
   - Username: `your_db_user`
   - Password: `secure_password_123`

---

## Part 5: Production Optimization

### 5.1 Enable HTTPS
1. **Your app** → **HTTP Settings**
2. **Enable:** Force HTTPS
3. **Enable:** Websocket Support (if needed)

### 5.2 Configure Custom Domain
1. **Your app** → **HTTP Settings**
2. **Add:** Custom Domain
3. **Update ALLOWED_HOSTS** environment variable

### 5.3 Set up Monitoring
1. **Your app** → **App Configs**
2. **Enable:** Monitoring and logging
3. **Set up:** Health check endpoint in Django

---

## Part 6: Managing Multiple Apps

### 6.1 Shared PostgreSQL Strategy
```
Single PostgreSQL Container:
├── database1 (app1_db)
├── database2 (app2_db)
└── database3 (app3_db)
```

**Create new databases:**
```sql
-- In pgAdmin Query Tool
CREATE DATABASE app2_db;
CREATE DATABASE app3_db;
```

**New app DATABASE_URL:**
```
postgres://username:password@srv-captain--postgres-db:5432/app2_db
```

### 6.2 Deployment Checklist for New Apps

**For each new Django app:**
- [ ] Add required files (captain-definition, Dockerfile.captain, etc.)
- [ ] Update settings.py with environment variable support
- [ ] Create new CapRover app
- [ ] Set environment variables
- [ ] Deploy from Git
- [ ] Run migrations via Portainer
- [ ] Create admin user
- [ ] Test application

---

## Part 7: Troubleshooting

### 7.1 Common Issues

**Build Failures:**
- Check Dockerfile.captain syntax
- Verify requirements.txt dependencies
- Check captain-definition format

**Database Connection Errors:**
- Verify DATABASE_URL format
- Check PostgreSQL container is running
- Confirm environment variables

**Static Files Not Loading:**
- Ensure WhiteNoise is configured
- Run `collectstatic` command
- Check STATIC_ROOT settings

### 7.2 Useful Commands

**Check container logs:**
```bash
docker logs [container-id]
```

**Restart app:**
- CapRover Dashboard → Your App → Save & Update

**Database backup:**
```bash
docker exec [postgres-container] pg_dump -U username database_name > backup.sql
```

---

## Part 8: Security Best Practices

### 8.1 Environment Variables
- Never commit secrets to Git
- Use strong passwords
- Rotate SECRET_KEY regularly

### 8.2 Database Security
- Use specific database users per app
- Restrict database permissions
- Enable connection encryption

### 8.3 Application Security
- Keep Django updated
- Use HTTPS in production
- Configure proper ALLOWED_HOSTS
- Enable security middleware

---

## Quick Reference

### Essential URLs:
- **CapRover:** `https://captain.your-domain.com`
- **Your App:** `https://your-app.captain.your-domain.com`
- **Portainer:** `https://portainer.captain.your-domain.com`
- **pgAdmin:** `https://pgadmin.captain.your-domain.com`

### Key Commands:
```bash
# Django management
python manage.py migrate
python manage.py collectstatic
python manage.py createsuperuser

# Docker
docker ps
docker logs [container-id]
docker exec -it [container-id] /bin/bash
```

This guide provides a complete, reusable process for deploying Django applications on CapRover with proper database management and development tools.