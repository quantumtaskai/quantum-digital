# Dokploy Deployment Guide - Quantum Digital

Complete guide for deploying the Quantum Digital Django application on Dokploy using Docker Compose.

## 📋 Prerequisites

- Dokploy instance running and accessible
- Domain name configured (e.g., `digital.quantumtaskai.com`)
- GitHub repository access
- PostgreSQL database (managed by Dokploy)

## 🚀 Deployment Steps

### 1. Create PostgreSQL Database in Dokploy

1. Log into your Dokploy dashboard
2. Create a new **Database** service:
   - Click **"+ Create Service"** → **"Database"**
   - Select **PostgreSQL**
   - Choose PostgreSQL version (recommended: 15 or 16)
   - Set database name: `quantum_digital`
   - Configure credentials (username/password)
   - Click **"Create"**
3. Copy the **DATABASE_URL** from the database screen
   - Format: `postgresql://user:password@host:5432/quantum_digital`

### 2. Create Docker Compose Application

1. In Dokploy, create a new **Compose** service:
   - Click **"+ Create Service"** → **"Compose"**
   - Select **"Docker Compose"** type (not Stack)

2. Configure Repository:
   - **Provider**: GitHub
   - **Repository**: Select your quantum-digital repo
   - **Branch**: `main`
   - **Compose Path**: `./docker-compose.yml`
   - Click **"Save"**

### 3. Configure Environment Variables

Go to the **Environment** tab and add these variables:

```bash
# Required Variables
SECRET_KEY=<generate-using-python-get-random-secret-key>
DEBUG=False
DOMAIN=digital.quantumtaskai.com
ALLOWED_HOSTS=digital.quantumtaskai.com,www.digital.quantumtaskai.com
CSRF_TRUSTED_ORIGINS=https://digital.quantumtaskai.com,https://www.digital.quantumtaskai.com

# Database (from Step 1)
DATABASE_URL=postgresql://user:password@postgres-host:5432/quantum_digital

# OAuth (Optional - can be configured in Django admin later)
GOOGLE_OAUTH2_CLIENT_ID=your-google-client-id
GOOGLE_OAUTH2_CLIENT_SECRET=your-google-client-secret
```

**To generate SECRET_KEY:**
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### 4. Configure Domain

**Option A: Using Traefik Labels (Recommended)**
- Labels are already configured in `docker-compose.yml`
- Set the `DOMAIN` environment variable
- Dokploy/Traefik will automatically handle SSL

**Option B: Using Dokploy Domain Tab**
1. Go to **Domain** tab
2. Click **"Add Domain"**
3. Enter your domain: `digital.quantumtaskai.com`
4. Select service: `web`
5. Port: `8000`
6. Enable **HTTPS/SSL** (Let's Encrypt automatic)

### 5. Deploy Application

1. Go to **General** tab
2. Click **"Deploy"** button
3. Monitor deployment in **Deployments** tab
4. Check logs for any errors

### 6. Post-Deployment Setup

#### Create Superuser (First Time Only)

**Option 1: Using Django Shell**
```bash
# In Dokploy, go to Terminal tab
python manage.py createsuperuser
```

**Option 2: Using Environment Variables**
Uncomment these lines in `.env`:
```bash
DJANGO_SUPERUSER_EMAIL=admin@your-domain.com
DJANGO_SUPERUSER_PASSWORD=secure-password
```
Then redeploy.

#### Configure Google OAuth (Optional)

1. Access Django admin: `https://digital.quantumtaskai.com/admin/`
2. Go to **Social Applications**
3. Add Google OAuth provider:
   - Provider: Google
   - Name: Google
   - Client ID: (from Google Console)
   - Secret: (from Google Console)
   - Sites: Select your site
   - Save

## 📊 Monitoring & Logs

### View Application Logs
- Go to **Logs** tab in Dokploy
- Real-time logs from Gunicorn and Django

### View Deployment History
- Go to **Deployments** tab
- See all deployment history and status

### Monitor Resources
- Go to **Monitoring** tab
- View CPU, Memory, Disk, Network usage

## 🔧 Troubleshooting

### Issue: 502 Bad Gateway

**Cause**: Application not starting or crashed

**Solution**:
1. Check logs in **Logs** tab
2. Verify DATABASE_URL is correct
3. Check if migrations ran successfully
4. Restart deployment

### Issue: Static Files Not Loading

**Cause**: WhiteNoise not serving files correctly

**Solution**:
1. Check that `collectstatic` ran in logs
2. Verify `STATIC_ROOT` permissions in container
3. Check browser console for 404 errors

### Issue: Database Connection Failed

**Cause**: DATABASE_URL incorrect or database not accessible

**Solution**:
1. Verify DATABASE_URL format
2. Check PostgreSQL service is running
3. Ensure network `dokploy-network` is configured
4. Test database connection from terminal

### Issue: CSRF Token Errors

**Cause**: CSRF_TRUSTED_ORIGINS misconfigured

**Solution**:
1. Add your domain to `CSRF_TRUSTED_ORIGINS`
2. Must include `https://` prefix
3. Redeploy after changes

## 🔄 Updating the Application

### Automatic Deployment (Recommended)

1. Push changes to GitHub
2. Dokploy webhook triggers automatic rebuild
3. Zero-downtime deployment

### Manual Deployment

1. Go to Dokploy dashboard
2. Click **"Deploy"** button
3. Wait for build to complete

## 🔐 Security Checklist

- [ ] `DEBUG=False` in production
- [ ] Strong `SECRET_KEY` generated
- [ ] Database credentials secure
- [ ] HTTPS enabled (automatic with Let's Encrypt)
- [ ] `ALLOWED_HOSTS` configured correctly
- [ ] `CSRF_TRUSTED_ORIGINS` configured
- [ ] OAuth credentials stored securely
- [ ] Regular database backups enabled in Dokploy

## 📁 Volume Persistence

Dokploy automatically persists data in `../files/` directory:

```yaml
volumes:
  - ../files/staticfiles:/app/staticfiles    # Static files
  - ../files/mediafiles:/app/mediafiles      # User uploads
  - ../files/backups:/app/backups            # Database backups
```

These volumes survive deployments and container restarts.

## 🗄️ Database Backups

### Automated Backups (Dokploy)

1. Go to PostgreSQL database service
2. Click **Backups** tab
3. Configure automated backups:
   - Frequency: Daily
   - Retention: 30 days
   - Destination: S3 (optional)

### Manual Backup

```bash
# In Dokploy terminal
python manage.py dbbackup
```

### Restore from Backup

```bash
python manage.py dbrestore
```

## 📞 Support Resources

- **Dokploy Documentation**: https://docs.dokploy.com
- **Django Documentation**: https://docs.djangoproject.com
- **Project README**: [README.md](README.md)
- **Database Management**: [DATABASE_MANAGEMENT.md](DATABASE_MANAGEMENT.md)

## 🎯 Production URLs

After successful deployment:

- **Application**: https://digital.quantumtaskai.com
- **Admin Panel**: https://digital.quantumtaskai.com/admin/
- **Login**: https://digital.quantumtaskai.com/accounts/login/
- **Dashboard**: https://digital.quantumtaskai.com/dashboard/

---

**Quantum Digital** - Deployed with Dokploy

*Last updated: 2025-10-02*
