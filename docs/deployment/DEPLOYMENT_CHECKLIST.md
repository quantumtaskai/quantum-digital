# Dokploy Deployment Checklist

## 1. Pre-Deployment: Environment Configuration

### 1. Environment Variables ✓
- [ ] `SECRET_KEY` set in Dokploy environment
- [ ] `DATABASE_URL` configured for PostgreSQL
- [ ] `DEBUG=False` in production
- [ ] `ALLOWED_HOSTS` includes `digital.quantumtaskai.com`
- [ ] Google OAuth credentials configured (if using OAuth)
- [ ] `CSRF_TRUSTED_ORIGINS` includes `https://digital.quantumtaskai.com,https://quantum-digital.dokploy.site`

### 2. Database Configuration ✓
- [ ] PostgreSQL database created
- [ ] `DATABASE_URL` is correctly formatted: `postgresql://user:password@host:port/dbname`
- [ ] Database credentials tested

---

## 2. Deployment: Dokploy `docker-compose.yml`

Create a new application in Dokploy using Git, and use the following `docker-compose.yml` content. This defines three services:
1.  `web`: Your Django application, run with Gunicorn.
2.  `nginx`: A web server to handle incoming traffic and serve static files.
3.  `migrate`: A one-off job to run database migrations on deployment.

```yaml
version: '3.8'

services:
  web:
    build: .
    command: gunicorn quantum_digital.wsgi:application --bind 0.0.0.0:8000 --workers 3
    volumes:
      - static_volume:/app/staticfiles
    expose:
      - 8000
    environment:
      - SECRET_KEY=${SECRET_KEY}
      - DEBUG=${DEBUG}
      - DATABASE_URL=${DATABASE_URL}
      - ALLOWED_HOSTS=${ALLOWED_HOSTS}
      - CSRF_TRUSTED_ORIGINS=${CSRF_TRUSTED_ORIGINS}
      - GOOGLE_OAUTH2_CLIENT_ID=${GOOGLE_OAUTH2_CLIENT_ID}
      - GOOGLE_OAUTH2_CLIENT_SECRET=${GOOGLE_OAUTH2_CLIENT_SECRET}

  nginx:
    image: nginx:1.25-alpine
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
      - static_volume:/app/staticfiles
    depends_on:
      - web

  migrate:
    build: .
    command: python manage.py migrate --noinput
    environment:
      - DATABASE_URL=${DATABASE_URL}

volumes:
  static_volume:
```

### 3. Create `nginx.conf`

Create a file named `nginx.conf` in the root of your project with this content. It tells Nginx how to route traffic to Django and where to find static files.

```bash
## nginx.conf

upstream django_server {
    server web:8000;
}

server {
    listen 80;

    location /static/ {
        alias /app/staticfiles/;
    }

    location / {
        proxy_pass http://django_server;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
    }
}
```

### Step 2: SSH into Dokploy Server
```bash
ssh root@31.97.62.205
cd /path/to/quantum-digital
```

### Step 3: Pull Latest Changes
```bash
git pull origin main
```

### Step 4: Rebuild and Deploy
```bash
# Stop existing containers
docker compose down

# Rebuild with no cache (if Dockerfile changed)
docker compose build --no-cache

# Start services
docker compose up -d

# Watch logs
docker compose logs -f
```

### Step 5: Run Migrations
```bash
# Migrations run automatically via docker-compose command
# But you can manually run if needed:
docker exec <web-container-name> python manage.py migrate
```

### Step 6: Verify Deployment
```bash
# Check containers are running
docker compose ps

# Check logs for errors
docker compose logs web --tail=50
docker compose logs nginx --tail=50

# Test application
curl -I https://digital.quantumtaskai.com
curl -I https://digital.quantumtaskai.com/static/css/auth.css
```

---

## Post-Deployment Verification

### 1. Application Health ✓
```bash
# Check container health
docker ps

# Verify Django is responding
docker exec <web-container> python manage.py check

# Test homepage
curl https://digital.quantumtaskai.com
```

### 2. Static Files ✓
```bash
# Test static CSS
curl -I https://digital.quantumtaskai.com/static/css/auth.css
# Should return: HTTP/2 200

# Test static images
curl -I https://digital.quantumtaskai.com/static/images/logo.png
# Should return: HTTP/2 200
```

### 3. Database Connectivity ✓
```bash
# Check database connection
docker exec <web-container> python manage.py dbshell
# Should connect successfully

# Run a test query
# \dt (list tables)
# \q (quit)
```

### 4. Authentication ✓
- [ ] Login page loads correctly
- [ ] Email/password login works
- [ ] Google OAuth login works (if configured)
- [ ] Logout works correctly
- [ ] Session persistence works

### 5. Dashboard Access ✓
- [ ] New users can access onboarding
- [ ] Completed onboarding redirects to dashboard
- [ ] Dashboard displays correctly
- [ ] All tabs load without errors

---

## Common Deployment Issues

### Issue 1: Container Won't Start
**Symptoms:** `docker compose up` fails immediately

**Diagnosis:**
```bash
docker compose logs web
docker compose logs nginx
```

**Common Causes:**
- Syntax error in docker-compose.yml
- Missing environment variables
- Port already in use
- Volume permission issues

**Fix:**
```bash
# Check syntax
docker compose config

# Check environment
docker compose config | grep -A 5 environment

# Free up ports
docker compose down
sudo lsof -i :80
sudo lsof -i :443
```

---

### Issue 2: Nginx Returns 502 Bad Gateway
**Symptoms:** Site loads but returns 502 error

**Diagnosis:**
```bash
docker compose logs nginx
docker compose logs web
```

**Common Causes:**
- Django container not running
- Wrong upstream server in nginx.conf
- Django not binding to correct port

**Fix:**
```bash
# Verify web container is running
docker compose ps

# Check Django is listening on port 8000
docker exec <web-container> netstat -tlnp | grep 8000

# Restart services
docker compose restart
```

---

### Issue 3: Static Files Return 404
**Symptoms:** CSS/JS/images don't load

**Diagnosis:**
```bash
# Check static files exist
docker exec <web-container> ls -la /app/staticfiles/

# Check nginx volume mount
docker inspect <nginx-container> | grep -A 10 Mounts

# Check nginx config
docker exec <nginx-container> cat /etc/nginx/nginx.conf | grep static
```

**Fix:**
```bash
# Rebuild static files
docker exec <web-container> python manage.py collectstatic --noinput --clear

# Restart nginx
docker compose restart nginx

# Verify volume mount
docker volume ls
docker volume inspect <static-volume-name>
```

---

### Issue 4: Database Migration Fails
**Symptoms:** Container starts but migrations don't run

**Diagnosis:**
```bash
docker compose logs web | grep migrate
```

**Common Causes:**
- Database not accessible
- Wrong DATABASE_URL
- Missing database tables
- Migration conflicts

**Fix:**
```bash
# Test database connection
docker exec <web-container> python manage.py dbshell

# Show migration status
docker exec <web-container> python manage.py showmigrations

# Run migrations manually
docker exec <web-container> python manage.py migrate

# If stuck, fake migrate (CAREFUL!)
docker exec <web-container> python manage.py migrate --fake
```

---

## Rollback Procedure

### If Deployment Fails:

```bash
# 1. Stop current deployment
docker compose down

# 2. Checkout previous working commit
git log --oneline | head -10
git checkout <previous-commit-hash>

# 3. Rebuild and deploy
docker compose build
docker compose up -d

# 4. Verify rollback
docker compose logs -f

# 5. Once verified, force push (or create revert commit)
git revert HEAD
git push origin main
```

---

## Monitoring & Logs

### Real-time Monitoring
```bash
# Watch all logs
docker compose logs -f

# Watch only web container
docker compose logs -f web

# Watch only nginx
docker compose logs -f nginx

# Filter for errors
docker compose logs web | grep -i error
docker compose logs web | grep 404
```

### Log Files
```bash
# Nginx access logs
docker exec <nginx-container> tail -f /var/log/nginx/access.log

# Nginx error logs
docker exec <nginx-container> tail -f /var/log/nginx/error.log

# Django logs (console)
docker compose logs web
```

---

## Performance Optimization

### After Successful Deployment:

1. **Enable Nginx Caching**
   - Update nginx.conf with cache settings
   - Add cache headers for static files

2. **Optimize Gunicorn Workers**
   - Current: 3 workers
   - Recommended: (2 x CPU cores) + 1
   - Monitor memory usage

3. **Database Connection Pooling**
   - Consider adding pgbouncer
   - Optimize query performance

4. **Static File CDN**
   - Consider using CDN for static files
   - Update STATIC_URL in settings

---

## Backup Verification

### After Deployment:
```bash
# Verify backup system is working
docker exec <web-container> python manage.py production_backup

# Check backup files
ls -lh /path/to/backups/

# Test restoration (on dev server!)
# docker exec <web-container> python manage.py loaddata /path/to/backup.json
```

---

## Security Checklist Post-Deployment

- [ ] DEBUG=False verified in production
- [ ] Secret key is unique and not in version control
- [ ] ALLOWED_HOSTS restricted to production domains
- [ ] CSRF protection enabled
- [ ] SSL/HTTPS working correctly
- [ ] Admin panel accessible only to superusers
- [ ] Database credentials secure
- [ ] File upload size limits configured
- [ ] Rate limiting considered (if needed)

---

## Final Verification URLs

Test these URLs after deployment:

- [ ] https://digital.quantumtaskai.com (Homepage)
- [ ] https://digital.quantumtaskai.com/accounts/login/ (Login)
- [ ] https://digital.quantumtaskai.com/accounts/signup/ (Signup)
- [ ] https://digital.quantumtaskai.com/dashboard/ (Dashboard)
- [ ] https://digital.quantumtaskai.com/profiles/onboarding/ (Onboarding)
- [ ] https://digital.quantumtaskai.com/admin/ (Admin)
- [ ] https://digital.quantumtaskai.com/static/css/auth.css (Static CSS)
- [ ] https://digital.quantumtaskai.com/static/images/logo.png (Static Image)

---

## Support & Documentation

**Key Documentation:**
- [Troubleshooting 404 Errors](./TROUBLESHOOTING_404.md)
- [Database Management](../../DATABASE_MANAGEMENT.md)
- [Main README](../../README.md)

**Server Access:**
- SSH: `ssh root@31.97.62.205`
- Dokploy Dashboard: Check your Dokploy URL
- Database: `31.97.62.205:5433`

**Emergency Contacts:**
- Project maintainer: [Your contact info]
- Server provider: [Hosting provider contact]

---

*Last updated: 2025-10-02*
*Production Domain: https://digital.quantumtaskai.com*
