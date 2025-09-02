# 🚨 Disaster Recovery Guide - Quantum Digital

## 📋 **Current System Configuration**

### **Server Details:**
- **VPS IP:** 69.62.81.168
- **CapRover Domain:** https://captain.69.62.81.168.nip.io
- **SSL Email:** thecyberlearn@gmail.com

### **Deployed Applications:**
- **quantum-digital:** https://quantum-digital.69.62.81.168.nip.io
- **quantum-digital-db:** PostgreSQL 14.5 (srv-captain--quantum-digital-db:5432)
- **pgadmin:** https://pgadmin.69.62.81.168.nip.io
- **netdata:** https://netdata.69.62.81.168.nip.io

### **Critical Environment Variables:**
```bash
# Django App Environment Variables
SECRET_KEY=(jo-zd_n!1%ccwgj#c6s2$-d!jvuzxfxvsmp!&_((-l48jl!l3
DEBUG=false
ALLOWED_HOSTS=quantum-digital.69.62.81.168.nip.io
DATABASE_URL=postgres://quantum_user:7e9f4e144881879c@srv-captain--quantum-digital-db:5432/postgres
SECURE_SSL_REDIRECT=true
```

### **Database Configuration:**
```bash
# PostgreSQL Details
Host: srv-captain--quantum-digital-db
Port: 5432
Username: quantum_user
Password: 7e9f4e144881879c
Database: postgres
```

### **pgAdmin Access:**
```bash
Email: admin@quantum-digital.com
Password: AdminPass123!
```

---

## 🔄 **Complete Recovery Procedure**

### **Phase 1: Fresh CapRover Installation**

#### **1.1 Server Setup:**
```bash
# Install Docker
curl -fsSL https://get.docker.com | sh

# Install CapRover
docker run -p 80:80 -p 443:443 -p 3000:3000 -v /var/run/docker.sock:/var/run/docker.sock -v /captain:/captain caprover/caprover
```

#### **1.2 CapRover Initial Setup:**
1. Access: http://[NEW-IP]:3000
2. Password: `captain42`
3. Set root domain: `captain.[NEW-IP].nip.io`
4. Enable HTTPS with email: `thecyberlearn@gmail.com`
5. Force HTTPS for root domain

### **Phase 2: Database Recovery**

#### **2.1 Deploy PostgreSQL:**
1. Apps → One-Click Apps → PostgreSQL
2. Configuration:
   ```
   App Name: quantum-digital-db
   Version: 14.5
   Username: quantum_user
   Password: 7e9f4e144881879c
   Default Database: postgres
   ```
3. Deploy and wait for completion

#### **2.2 Restore Database:**
```bash
# Method 1: Via pgAdmin (Deploy pgAdmin first)
1. Deploy pgAdmin from One-Click Apps
2. Connect to PostgreSQL server
3. Right-click database → Restore
4. Upload backup file

# Method 2: Via Command Line
docker exec -i [postgres-container-id] psql -U quantum_user -d postgres < backup.sql
```

### **Phase 3: Django App Deployment**

#### **3.1 Create Django App:**
1. Apps → Create New App → `quantum-digital`
2. Has Persistent Data: ✅
3. Deployment → Method 3: Git Repository
4. Repository: `https://github.com/quantumtaskai/quantum-digital.git`
5. Branch: `main`

#### **3.2 Configure Environment Variables:**
```bash
SECRET_KEY=(jo-zd_n!1%ccwgj#c6s2$-d!jvuzxfxvsmp!&_((-l48jl!l3
DEBUG=false
ALLOWED_HOSTS=quantum-digital.[NEW-IP].nip.io
DATABASE_URL=postgres://quantum_user:7e9f4e144881879c@srv-captain--quantum-digital-db:5432/postgres
SECURE_SSL_REDIRECT=true
```

#### **3.3 Deploy and Setup:**
1. Force Build
2. Enable HTTPS + Force HTTPS
3. Run migrations via Portainer:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser --noinput --username admin --email admin@example.com
   python manage.py shell -c "from django.contrib.auth.models import User; u=User.objects.get(username='admin'); u.set_password('admin123'); u.save(); print('Password set')"
   ```

### **Phase 4: Support Tools Recovery**

#### **4.1 Deploy pgAdmin:**
```bash
App Name: pgadmin
Email: admin@quantum-digital.com
Password: AdminPass123!
```

#### **4.2 Deploy Netdata:**
```bash
App Name: netdata
Default settings
```

#### **4.3 Deploy Portainer (Optional):**
```bash
App Name: portainer
Default settings
```

---

## 📊 **Recovery Time Estimates**

| Phase | Task | Time | Critical |
|-------|------|------|----------|
| 1 | Fresh CapRover Setup | 30 min | ✅ |
| 2 | Database Recovery | 20 min | ✅ |
| 3 | Django App Deployment | 15 min | ✅ |
| 4 | Support Tools | 15 min | ⚠️ |
| **Total** | **Complete Recovery** | **80 min** | |

---

## 🔐 **Security Notes**

### **Secrets to Rotate After Recovery:**
- [ ] Django SECRET_KEY (generate new)
- [ ] Database passwords (if compromised)
- [ ] Admin passwords
- [ ] SSL certificates (auto-renew)

### **Post-Recovery Checklist:**
- [ ] Test all application functionality
- [ ] Verify database data integrity
- [ ] Check SSL certificates
- [ ] Test user authentication
- [ ] Verify email functionality
- [ ] Update DNS if IP changed
- [ ] Test backup procedures

---

## 📧 **Emergency Contacts & Access**

### **Critical Access Information:**
- **GitHub Repository:** https://github.com/quantumtaskai/quantum-digital
- **Email for SSL:** thecyberlearn@gmail.com
- **VPS Provider:** [Document your VPS provider details]

### **Backup Locations:**
- **Database Backups:** GitHub Releases (encrypted)
- **Code Repository:** GitHub
- **Configuration:** This document

---

## 🚨 **Emergency Procedures**

### **If Database is Corrupted:**
1. Stop Django application
2. Deploy fresh PostgreSQL
3. Restore from latest backup
4. Run Django migrations
5. Test data integrity

### **If Application Won't Start:**
1. Check container logs in CapRover
2. Verify environment variables
3. Check database connectivity
4. Rebuild from Git repository

### **If CapRover is Unreachable:**
1. SSH into server
2. Check Docker status: `docker ps`
3. Restart CapRover: `docker restart captain-captain`
4. Check server resources: `htop`, `df -h`

---

## 📝 **Recovery Validation Tests**

### **After Recovery, Test:**
1. **Frontend Access:** Visit Django app URL
2. **Admin Access:** Login to /admin/
3. **Database:** Create/read/update data
4. **Authentication:** User login/logout
5. **SSL:** Verify HTTPS working
6. **Monitoring:** Check Netdata
7. **Management:** Access pgAdmin

### **Success Criteria:**
- ✅ All URLs responding with HTTPS
- ✅ Database queries working
- ✅ User authentication functional
- ✅ Admin panel accessible
- ✅ No console errors

---

## 🔄 **Maintenance Schedule**

### **Weekly:**
- [ ] Database backup via pgAdmin (manual)
- [ ] Check application health via Netdata
- [ ] Verify SSL certificate status

### **Monthly:**
- [ ] Test recovery procedures
- [ ] Update this documentation
- [ ] Review and rotate secrets

### **Before Major Changes:**
- [ ] Create database backup
- [ ] Document current working state
- [ ] Test rollback procedures

---

*Last Updated: 2025-09-02*
*Next Review: 2025-10-02*