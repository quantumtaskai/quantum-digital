# 🔄 Automated Backup Setup Guide

## 📋 **Overview**

This repository includes an automated backup system that:
- ✅ Runs daily at 2 AM UTC
- ✅ Creates compressed PostgreSQL dumps
- ✅ Stores backups as GitHub Releases
- ✅ Keeps last 30 backups automatically
- ✅ Sends email notifications on success/failure
- ✅ Includes checksums for integrity verification

## ⚙️ **Setup Instructions**

### **Step 1: Configure GitHub Secrets**

Go to your GitHub repository: **Settings → Secrets and variables → Actions**

Add these **Repository Secrets:**

#### **Database Connection:**
```
DB_HOST = 69.62.81.168
DB_PORT = 5432
DB_USER = quantum_user
DB_PASSWORD = 7e9f4e144881879c
DB_NAME = postgres
```

#### **Email Notifications:**
```
EMAIL_USERNAME = thecyberlearn@gmail.com
EMAIL_PASSWORD = your-gmail-app-password
```

> **Note:** For Gmail, you need an "App Password", not your regular password.  
> Generate at: https://myaccount.google.com/apppasswords

### **Step 2: Test the Backup**

1. **Manual Test:**
   - Go to **Actions** tab in GitHub
   - Click **"Automated Database Backup"**
   - Click **"Run workflow"** → **"Run workflow"**

2. **Wait for completion** (2-3 minutes)

3. **Check Results:**
   - **Success:** Check **Releases** tab for backup file
   - **Failure:** Check **Actions** logs for errors

### **Step 3: Verify Backup**

1. **Go to Releases:** https://github.com/quantumtaskai/quantum-digital/releases
2. **Download latest backup:** `quantum-digital-backup-YYYYMMDD_HHMMSS.sql.gz`
3. **Verify checksum:** Compare with `backup-checksum.txt`

---

## 🔧 **Usage**

### **Automatic Backups:**
- **Schedule:** Daily at 2 AM UTC
- **Location:** GitHub Releases
- **Retention:** Last 30 backups
- **Format:** Compressed SQL dump

### **Manual Backups:**
```bash
# Via GitHub Actions
1. Go to Actions → "Automated Database Backup"
2. Click "Run workflow"

# Via Command Line (on server)
pg_dump -h 69.62.81.168 -U quantum_user postgres > backup.sql
```

### **Restore Procedure:**
```bash
# Download backup from GitHub Releases
wget https://github.com/quantumtaskai/quantum-digital/releases/download/backup-YYYYMMDD_HHMMSS/quantum-digital-backup-YYYYMMDD_HHMMSS.sql.gz

# Decompress
gunzip quantum-digital-backup-YYYYMMDD_HHMMSS.sql.gz

# Restore to database
psql -h HOST -U quantum_user -d postgres < quantum-digital-backup-YYYYMMDD_HHMMSS.sql
```

---

## 🔍 **Monitoring**

### **Success Indicators:**
- ✅ **Email notification** received
- ✅ **New release** appears in GitHub
- ✅ **Backup file** size is reasonable (>1MB)
- ✅ **Checksum file** included

### **Troubleshooting:**

#### **Backup Failed:**
1. Check GitHub Actions logs
2. Verify database is accessible from internet
3. Confirm GitHub secrets are correct
4. Test database connection manually

#### **No Email Notifications:**
1. Verify Gmail app password
2. Check spam folder
3. Confirm EMAIL_USERNAME/EMAIL_PASSWORD secrets

#### **Large Backup Size:**
- Normal: 1-50MB
- Large: >100MB (check for unnecessary data)

---

## 📊 **Backup Schedule**

| Time | Action | Retention |
|------|--------|-----------|
| Daily 2 AM UTC | Automated backup | 30 days |
| Manual | On-demand backup | 30 days |
| Before deployments | Manual backup | Keep important ones |

---

## 🔐 **Security**

### **Data Protection:**
- Backups stored in private GitHub repository
- Database credentials in encrypted secrets
- No plaintext passwords in code

### **Access Control:**
- Only repository collaborators can access backups
- GitHub token permissions limited to releases
- Email notifications only to authorized email

---

## ⚠️ **Important Notes**

1. **Database Access:** Server must allow external PostgreSQL connections
2. **GitHub Storage:** Free tier has storage limits (check usage)
3. **Email Limits:** Gmail has sending limits (100 emails/day)
4. **Time Zone:** All times in UTC (adjust for your local time)

---

## 🔧 **Customization**

### **Change Backup Schedule:**
Edit `.github/workflows/backup.yml`:
```yaml
schedule:
  - cron: '0 2 * * *'  # Daily at 2 AM UTC
  - cron: '0 14 * * 0' # Weekly on Sunday at 2 PM UTC
```

### **Change Retention:**
Edit cleanup section in workflow:
```bash
tail -n +31  # Keep last 30 (change 31 to keep different amount)
```

### **Add More Notifications:**
- Slack notifications
- Discord webhooks  
- SMS notifications (via services like Twilio)

---

*Setup Date: 2025-09-02*  
*Next Review: Check weekly for first month*