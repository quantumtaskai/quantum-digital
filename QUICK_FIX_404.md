# Quick Fix Guide for 404 Errors

## 🚨 Immediate Actions

### 1. Restart Services
```bash
ssh root@31.97.62.205
cd /path/to/quantum-digital
docker compose restart
```

### 2. Check Container Status
```bash
docker compose ps
# Both 'web' and 'nginx' should be running
```

### 3. Rebuild Static Files
```bash
docker exec <web-container-name> python manage.py collectstatic --noinput --clear
docker compose restart nginx
```

### 4. View Logs
```bash
# Check for 404 errors
docker compose logs web | grep 404

# Check nginx errors
docker compose logs nginx | tail -50
```

---

## ✅ What Changed to Fix 404 Issues

### 1. Added Nginx Service
**File:** [docker-compose.yml](docker-compose.yml)

**Before:** Only Django/Gunicorn container (no static file serving)
**After:** Nginx container added to serve static files properly

### 2. Added Shared Volumes
- `static_volume` - Shared between Django and Nginx for CSS/JS/images
- `media_volume` - Shared for user-uploaded files
- `nginx_logs` - For monitoring nginx access/error logs

### 3. Improved Logging
**File:** [quantum_digital/settings.py](quantum_digital/settings.py:299-313)

Django now logs 404 errors at WARNING level to help diagnose issues.

---

## 🔧 Testing After Fix

### Test Static Files
```bash
# Should return HTTP 200
curl -I https://digital.quantumtaskai.com/static/css/auth.css
curl -I https://digital.quantumtaskai.com/static/images/logo.png
```

### Test Application Routes
```bash
# Homepage
curl -I https://digital.quantumtaskai.com/

# Login
curl -I https://digital.quantumtaskai.com/accounts/login/

# Dashboard (requires auth)
curl -I https://digital.quantumtaskai.com/dashboard/
```

---

## 📋 Deployment Steps

### Option 1: Dokploy Dashboard
1. Go to Dokploy dashboard
2. Select your application
3. Click "Redeploy"
4. Monitor build logs
5. Verify deployment success

### Option 2: SSH Manual Deployment
```bash
# 1. SSH into server
ssh root@31.97.62.205

# 2. Navigate to project
cd /path/to/quantum-digital

# 3. Pull latest changes
git pull origin main

# 4. Rebuild containers
docker compose down
docker compose up -d --build

# 5. Monitor logs
docker compose logs -f
```

---

## 🔍 Verification Checklist

After deployment, verify:

- [ ] Both containers running: `docker compose ps`
- [ ] Homepage loads: Visit https://digital.quantumtaskai.com
- [ ] Static files load: Check CSS/images in browser DevTools
- [ ] Login works: Test authentication
- [ ] No 502/504 errors
- [ ] No console errors in browser

---

## 📞 Still Having Issues?

### Check Detailed Documentation
- [Troubleshooting 404 Errors](docs/deployment/TROUBLESHOOTING_404.md)
- [Deployment Checklist](docs/deployment/DEPLOYMENT_CHECKLIST.md)

### Common Issues

**502 Bad Gateway:**
- Django container not running
- Check: `docker compose restart web`

**Static Files 404:**
- Nginx volume mount issue
- Fix: `docker compose down -v && docker compose up -d`

**Database Errors:**
- Connection string wrong
- Check: `docker exec <web-container> python manage.py check --database=default`

---

## 🎯 Root Cause

The original setup was missing the **Nginx service** in docker-compose.yml.

Gunicorn (Django's app server) does not serve static files in production, so all CSS/JS/image requests were returning 404. The fix adds a proper Nginx reverse proxy that:

1. Serves static files from shared volume
2. Proxies dynamic requests to Django/Gunicorn
3. Provides proper caching and performance optimization

---

*For detailed troubleshooting, see [docs/deployment/TROUBLESHOOTING_404.md](docs/deployment/TROUBLESHOOTING_404.md)*
