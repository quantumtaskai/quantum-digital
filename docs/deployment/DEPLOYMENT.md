# CapRover Deployment Guide

## Prerequisites
- CapRover instance running on your VPS
- Git repository with your Django app
- PostgreSQL database (optional, can use SQLite)

## Deployment Steps

### 1. CapRover App Setup
1. Login to your CapRover dashboard
2. Go to "Apps" and click "Create New App"
3. Enter app name (e.g., `quantum-digital`)
4. Choose "Has Persistent Data" if using database

### 2. Connect Git Repository
1. Go to your app's "Deployment" tab
2. Select "Method 3: Deploy from Github/Bitbucket/Gitlab"
3. Enter your repository URL
4. Set branch to `main`
5. Click "Save & Update"

### 3. Environment Variables
Go to "App Configs" > "Environment Variables" and set:

```
SECRET_KEY=your-secret-key-here
DEBUG=false
ALLOWED_HOSTS=your-domain.com
DATABASE_URL=postgres://user:password@host:port/dbname
```

### 4. Database Setup (Optional)
If using PostgreSQL:
1. Go to "Apps" > "One-Click Apps/Databases"
2. Select "PostgreSQL"
3. Deploy and get connection details
4. Update DATABASE_URL environment variable

### 5. Deploy
1. Push changes to your Git repository
2. In CapRover, go to your app's "Deployment" tab
3. Click "Force Build"
4. Monitor deployment logs

### 6. Post-Deployment
After successful deployment:
```bash
# SSH into your CapRover container
docker exec -it $(docker ps | grep quantum-digital | awk '{print $1}') /bin/bash

# Run Django migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### 7. Enable HTTPS
1. Go to "App Configs" > "HTTP Settings"
2. Enable "HTTPS" and "Force HTTPS"
3. Enable "Websocket Support" if needed

## Important Notes
- The app automatically detects CapRover environment using `CAPROVER_GIT_COMMIT_SHA`
- Static files are collected during build process
- Gunicorn serves the application on port 80
- Database migrations must be run manually after deployment

## Troubleshooting
- Check deployment logs in CapRover dashboard
- Ensure all environment variables are set correctly
- Verify database connectivity
- Check static files are being served correctly