# Troubleshooting 404 Errors on Dokploy

## Overview
This guide helps diagnose and fix intermittent 404 errors on https://digital.quantumtaskai.com deployed on Dokploy.

## Common Causes of 404 Errors

### 1. Static Files Not Being Served ⚠️ CRITICAL

**Symptoms:**
- CSS/JS files return 404
- Images don't load
- Site works but styling is broken

**Root Cause:**
- Nginx not configured properly
- Static files not collected during deployment
- Volume mounts missing between Django and Nginx containers

**Fix:**
```bash
# SSH into Dokploy server
ssh root@31.97.62.205

# Check if nginx container is running
docker ps | grep nginx

# Check static files volume
docker volume ls | grep static

# Restart containers to rebuild volumes
docker compose down
docker compose up -d

# Check nginx logs
docker logs <nginx-container-name>
```

**Prevention:**
- Ensure `docker-compose.yml` has nginx service with proper volume mounts
- Verify `collectstatic` runs during container startup
- Check nginx.conf has correct paths to static files

---

### 2. Missing Nginx Container

**Symptoms:**
- Gunicorn serves requests directly on port 8000
- Static files return 404
- Site is slow under load

**Root Cause:**
- `docker-compose.yml` missing nginx service
- Dokploy configuration not set up correctly

**Fix:**
The updated `docker-compose.yml` now includes:
- Nginx service with Alpine Linux image
- Shared volumes for static and media files
- Proper networking between Django and Nginx

**Verification:**
```bash
# Check both containers are running
docker compose ps

# Should see:
# - web (Django/Gunicorn)
# - nginx (Nginx reverse proxy)

# Test static file access
curl -I https://digital.quantumtaskai.com/static/css/auth.css
# Should return 200 OK
```

---

### 3. URL Routing Issues

**Symptoms:**
- Specific pages return 404
- Homepage works but other routes don't
- User gets 404 after login

**Root Cause:**
- Django URL patterns misconfigured
- Middleware redirecting incorrectly
- OnboardingMiddleware causing redirect loops

**Diagnosis:**
```bash
# Check Django URL patterns
docker exec <web-container> python manage.py show_urls

# Check logs for redirect loops
docker logs <web-container> | grep 404

# Test specific URL
curl -I https://digital.quantumtaskai.com/dashboard/
```

**Fix:**
Check `quantum_digital/middleware.py` for OnboardingMiddleware issues:
- Ensure it doesn't redirect admin/staff users incorrectly
- Verify BrandProfile checks work properly
- Add exception handling for database queries

---

### 4. Database Connection Issues

**Symptoms:**
- Random 500 or 404 errors
- Middleware crashes causing 404 fallback
- Site works intermittently

**Root Cause:**
- Database connection pool exhausted
- Middleware queries failing silently
- OnboardingMiddleware can't query BrandProfile

**Diagnosis:**
```bash
# Check database connection
docker exec <web-container> python manage.py check --database=default

# Monitor database connections
docker exec <web-container> python manage.py dbshell
# Then run: SELECT count(*) FROM pg_stat_activity;

# Check middleware errors
docker logs <web-container> | grep "BrandProfile"
```

**Fix:**
- Increase database connection pool size
- Add proper error handling in middleware
- Use connection pooling (pgbouncer)

---

### 5. Static File Manifest Issues

**Symptoms:**
- CSS/JS files have hashed names
- Files return 404 after deployment
- Site worked before, broken after update

**Root Cause:**
- `CompressedManifestStaticFilesStorage` cache issues
- Manifest file not generated correctly
- Old manifest cached by browser/CDN

**Fix:**
```bash
# Rebuild static files manifest
docker exec <web-container> python manage.py collectstatic --clear --noinput

# Restart nginx to clear cache
docker restart <nginx-container>

# Verify manifest file exists
docker exec <web-container> ls -la /app/staticfiles/staticfiles.json
```

---

## Debugging Workflow

### Step 1: Check Container Status
```bash
ssh root@31.97.62.205
docker compose ps
docker compose logs --tail=100
```

### Step 2: Check Nginx Configuration
```bash
docker exec <nginx-container> nginx -t
docker logs <nginx-container> | tail -50
```

### Step 3: Check Django Application
```bash
docker exec <web-container> python manage.py check
docker logs <web-container> | grep -i error
```

### Step 4: Test Static File Access
```bash
# Test from server
curl -I http://localhost/static/css/auth.css

# Test from outside
curl -I https://digital.quantumtaskai.com/static/css/auth.css
```

### Step 5: Check Django Logs for 404s
```bash
docker logs <web-container> | grep "GET.*404"
```

---

## Monitoring & Prevention

### 1. Set Up Log Monitoring
```bash
# Create log monitoring script
cat > /root/monitor-404.sh << 'EOF'
#!/bin/bash
echo "Monitoring 404 errors..."
docker logs -f <web-container> 2>&1 | grep --line-buffered "404"
EOF

chmod +x /root/monitor-404.sh
```

### 2. Add Healthcheck Endpoints
The application already has a healthcheck in the Dockerfile:
```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000', timeout=10)"
```

### 3. Check Container Health
```bash
# View health status
docker ps --format "table {{.Names}}\t{{.Status}}"

# Unhealthy containers will show in status
```

### 4. Enable Django 404 Logging
The settings have been updated to log 404 errors:
```python
'django.request': {
    'handlers': ['console'],
    'level': 'WARNING',  # Catches 404s
    'propagate': False,
},
```

---

## Quick Fixes

### Restart Everything
```bash
cd /path/to/project
docker compose down
docker compose up -d
docker compose logs -f
```

### Rebuild Static Files
```bash
docker exec <web-container> python manage.py collectstatic --noinput --clear
docker restart <nginx-container>
```

### Clear All Volumes and Rebuild
```bash
docker compose down -v
docker compose up -d --build
```

### Check Dokploy Dashboard
1. Go to Dokploy dashboard
2. Check application logs
3. View deployment history
4. Check SSL certificate status

---

## Updated Architecture

```
┌─────────────────────────────────────┐
│  Dokploy (Traefik Reverse Proxy)   │
│  SSL Termination & Load Balancing   │
└─────────────────┬───────────────────┘
                  │
                  ▼
┌─────────────────────────────────────┐
│         Nginx Container              │
│  - Serves static files (/static/)   │
│  - Serves media files (/media/)     │
│  - Proxies to Gunicorn              │
└─────────────────┬───────────────────┘
                  │
                  ▼
┌─────────────────────────────────────┐
│      Django/Gunicorn Container      │
│  - Handles dynamic requests         │
│  - Port 8000 (internal)             │
│  - Whitenoise fallback enabled      │
└─────────────────┬───────────────────┘
                  │
                  ▼
┌─────────────────────────────────────┐
│      PostgreSQL Database            │
│  - Port 5433                        │
│  - Automated backups                │
└─────────────────────────────────────┘
```

---

## Contact & Support

**Server Details:**
- Domain: https://digital.quantumtaskai.com
- Server IP: 31.97.62.205
- Database Port: 5433

**Key Files:**
- [docker-compose.yml](../../docker-compose.yml)
- [nginx.conf](../../nginx.conf)
- [settings.py](../../quantum_digital/settings.py)
- [Dockerfile](../../Dockerfile)

**Monitoring:**
- Container logs: `docker compose logs -f`
- Nginx logs: Mounted at `nginx_logs` volume
- Django logs: Console output in web container

---

*Last updated: 2025-10-02*
*Version: 1.0*
