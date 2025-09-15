# Dockploy Deployment Guide

Deploy Django Quantum Digital app to `digital.quantumtaskai.com` using Dockploy.

## 🚀 **Prerequisites**

- Dockploy instance running
- Domain `digital.quantumtaskai.com` pointing to your server
- Git repository accessible to Dockploy
- OAuth credentials for social login

## 📁 **Files Created for Deployment**

✅ `Dockerfile` - Production Docker image  
✅ `docker-compose.yml` - Multi-service configuration  
✅ `.env.production` - Production environment variables  
✅ `nginx.conf` - Reverse proxy configuration  

## 🔧 **Deployment Steps**

### **Step 1: Push Code to Repository**

```bash
git add .
git commit -m "Add production deployment files"
git push origin main
```

### **Step 2: Set Up Environment Variables in Dockploy**

In Dockploy, add these environment variables:

```env
# Django Configuration
SECRET_KEY=s6z3(uzpvy7!z$&i7@yxtx*)agy1bw@k65ok_6^v2&bs^q3mo6
DEBUG=False
ALLOWED_HOSTS=digital.quantumtaskai.com,localhost,127.0.0.1

# Neon Database
DATABASE_URL=postgresql://neondb_owner:npg_vAPIG7tm1hQB@ep-winter-queen-a17omo4b-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require

# OAuth Credentials (Update with real values)
GOOGLE_OAUTH2_CLIENT_ID=your-production-google-client-id
GOOGLE_OAUTH2_CLIENT_SECRET=your-production-google-client-secret
FACEBOOK_APP_ID=your-production-facebook-app-id
FACEBOOK_APP_SECRET=your-production-facebook-app-secret
GITHUB_CLIENT_ID=your-production-github-client-id
GITHUB_CLIENT_SECRET=your-production-github-client-secret
LINKEDIN_OAUTH2_CLIENT_ID=your-production-linkedin-client-id
LINKEDIN_OAUTH2_CLIENT_SECRET=your-production-linkedin-client-secret
```

### **Step 3: Create Application in Dockploy**

1. **Create New Application**
   - Name: `quantum-digital`
   - Type: `Docker Compose`
   - Repository: Your Git repository URL
   - Branch: `main`

2. **Domain Configuration**
   - Primary domain: `digital.quantumtaskai.com`
   - Enable SSL/TLS (Let's Encrypt)
   - Enable automatic certificate renewal

3. **Port Configuration**
   - Container port: `8000`
   - Public port: `80/443` (handled by nginx)

### **Step 4: Deploy**

1. Click **"Deploy"** in Dockploy
2. Monitor deployment logs
3. Wait for all services to start

### **Step 5: Update OAuth Redirect URIs**

Update your OAuth providers with production URLs:

**Google OAuth2:**
- Authorized redirect URIs: `https://digital.quantumtaskai.com/accounts/google/login/callback/`

**Facebook:**
- Valid OAuth Redirect URIs: `https://digital.quantumtaskai.com/accounts/facebook/login/callback/`

**GitHub:**
- Authorization callback URL: `https://digital.quantumtaskai.com/accounts/github/login/callback/`

**LinkedIn:**
- Authorized redirect URLs: `https://digital.quantumtaskai.com/accounts/linkedin_oauth2/login/callback/`

### **Step 6: Configure OAuth in Django Admin**

1. Go to: `https://digital.quantumtaskai.com/admin/`
2. Login with your superuser account
3. Go to **"Social Applications"**
4. Update each OAuth application with production credentials

## 🏗️ **Architecture Overview**

```
Internet → Dockploy Load Balancer → Nginx → Django App → Neon Database
                                 ↳ Static Files
```

## 🔍 **Health Check**

After deployment, verify:

- ✅ `https://digital.quantumtaskai.com/` - App loads
- ✅ `https://digital.quantumtaskai.com/admin/` - Admin accessible
- ✅ `https://digital.quantumtaskai.com/accounts/login/` - Login page with Google button
- ✅ SSL certificate valid
- ✅ Static files loading

## 🐛 **Troubleshooting**

### **Database Connection Issues**
```bash
# Check if Neon database is accessible
docker exec -it quantum-digital_web_1 python manage.py dbshell
```

### **Static Files Not Loading**
```bash
# Rebuild static files
docker exec -it quantum-digital_web_1 python manage.py collectstatic --noinput
```

### **SSL Certificate Issues**
- Verify domain DNS points to your server
- Check Dockploy SSL configuration
- Ensure ports 80/443 are open

### **Check Logs**
```bash
# View application logs
docker logs quantum-digital_web_1

# View nginx logs
docker logs quantum-digital_nginx_1
```

## 📈 **Post-Deployment**

1. **Monitor Performance**
   - Check response times
   - Monitor database connections
   - Review error logs

2. **Set Up Backups**
   - Database backups (Neon handles this)
   - Media files backup
   - Configuration backup

3. **Security Hardening**
   - Update OAuth secrets regularly
   - Monitor access logs
   - Keep dependencies updated

## 🎯 **Expected URLs**

- **Main App**: `https://digital.quantumtaskai.com/`
- **Admin**: `https://digital.quantumtaskai.com/admin/`
- **Login**: `https://digital.quantumtaskai.com/accounts/login/`
- **API**: `https://digital.quantumtaskai.com/api/` (if implemented)

Your Django app with social login is now production-ready! 🚀
