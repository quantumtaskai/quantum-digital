# Quantum Digital - AI Digital Branding Platform

A comprehensive Django web application for digital branding and marketing strategy management. This platform provides businesses with personalized dashboards, automated backup systems, and comprehensive brand management tools.

## 📦 Quick Deployment

**Ready for Dokploy deployment!** See [DOKPLOY_DEPLOYMENT.md](DOKPLOY_DEPLOYMENT.md) for complete deployment instructions.

- ✅ Docker & Docker Compose configured
- ✅ WhiteNoise for static files (no nginx needed)
- ✅ Gunicorn production server
- ✅ PostgreSQL ready
- ✅ Automatic migrations & collectstatic
- ✅ SSL/HTTPS via Traefik

## 🚀 Features

### 🔐 Authentication & User Flow
- **Social Authentication**: Google OAuth integration with django-allauth
- **User Registration**: Email + password registration system  
- **Smart Redirect**: New users → Onboarding → Dashboard
- **Returning Users**: Direct dashboard access after login
- **Secure Session Management**: Enterprise-grade security

### 📋 Brand Onboarding System
Complete brand profile creation with:
- **Brand Information**: Name, vision, mission, core values
- **Contact Management**: Primary and secondary contacts
- **Digital Assets**: Website, guidelines, blog integration
- **KPIs Tracking**: Traffic, reach, ratings, content metrics
- **SWOT Analysis**: Strategic planning visualization
- **Social Media**: 16+ platform integrations
- **Business Intelligence**: Partners, competitors analysis

### 📊 Personalized Dashboard
- **Multi-Tab Interface**: Overview, Performance, Analytics, Strategy
- **Real-Time Metrics**: Dynamic KPI calculations
- **Platform Status**: Social media platform tracking
- **Content Analytics**: Production and publication metrics
- **Strategic Planning**: SWOT visualization and insights

### 🛡️ Enterprise Backup System
- **Automated Daily Backups**: Server (2 AM) + Local (3 AM)
- **7-Day Retention**: Optimized storage management
- **Multiple Formats**: Django JSON + PostgreSQL dumps
- **Zero Maintenance**: Fully automated with cleanup
- **Download Tools**: One-command backup retrieval

## 🏗️ Architecture

### Project Structure
```
quantum-digital/
├── quantum_digital/          # Django project configuration
├── accounts/                 # Authentication & user management
├── profiles/                 # Brand profile management
├── dashboard/               # Dashboard & analytics
│   └── management/commands/ # Backup & maintenance tools
├── manager/                 # Admin management interface
├── templates/               # HTML templates with modern UI
├── static/                  # CSS, JS, images
├── docs/                    # Organized documentation
│   └── setup/              # Setup instructions
└── DATABASE_MANAGEMENT.md   # Backup system documentation
```

### Technology Stack
- **Backend**: Django 5.2.5 with PostgreSQL
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Authentication**: django-allauth with Google OAuth
- **Backup**: django-dbbackup with automated scheduling
- **Tools**: django-extensions for enhanced management

## ⚡ Quick Start

### 1. Environment Setup
```bash
# Clone and setup
git clone <repository-url>
cd quantum-digital
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Database Configuration
```bash
# Development (SQLite)
python manage.py migrate
python manage.py createsuperuser

# Production (PostgreSQL)
export DATABASE_URL="postgresql://user:password@host:port/dbname"
python manage.py migrate
python manage.py setup_production
```

### 3. Run Application
```bash
# Development
python manage.py runserver

# Enhanced shell with auto-imports
python manage.py shell_plus

# View all URLs
python manage.py show_urls
```

## 🔧 Database Management

### Automated Backup System
```bash
# Manual backup
python manage.py production_backup

# Daily automated backups (configured)
# Server: 2:00 AM - Creates backup with 7-day cleanup
# Local: 3:00 AM - Downloads and stores locally

# Download latest backup
cd /mnt/sdd2/projects_db_backup/quantum_digital
./quick_backup.sh
```

### Restoration
```bash
# Restore from backup
python manage.py loaddata /path/to/quantum_digital_backup_YYYYMMDD_HHMMSS.json

# Emergency production setup
python manage.py setup_production
```


## 👥 User Workflows

### For End Users
1. **Register/Login**: Email+password or Google OAuth
2. **Complete Onboarding**: Comprehensive brand profile form
3. **Access Dashboard**: Personalized analytics and insights
4. **Platform Management**: Track social media and content metrics

### For Administrators  
1. **Admin Panel**: Django admin at `/admin/`
2. **Brand Management**: Full CRUD operations on brand profiles
3. **User Management**: Account management and permissions
4. **System Monitoring**: Backup status and application health

## 🔒 Security Features

### Authentication & Authorization
- **OAuth Integration**: Secure Google authentication
- **CSRF Protection**: All forms protected
- **Session Security**: Secure session management
- **Password Validation**: Django security standards

### Data Protection
- **Daily Backups**: Automated with 7-day retention
- **Environment Variables**: Secure configuration management
- **HTTPS Enforcement**: Production SSL/TLS
- **Input Validation**: Comprehensive form validation

## 📈 Performance & Monitoring

### Database Optimization
- **Connection Pooling**: Efficient database connections
- **Query Optimization**: django-extensions for debugging
- **Backup Management**: Automated cleanup and storage
- **Migration Safety**: Bulletproof migration system

### Development Tools
```bash
# Performance analysis
python manage.py shell_plus --print-sql

# Database backup
python manage.py production_backup --cleanup

# URL debugging
python manage.py show_urls
```

## 🆘 Troubleshooting

### Common Issues
- **Backup Problems**: Check backup logs in `/backups/` directory
- **Authentication Issues**: Verify OAuth configuration in admin
- **Database Conflicts**: Run `python manage.py setup_production`

### Support Resources
- **Documentation**: `/docs/` directory for detailed guides
- **Database Guide**: [DATABASE_MANAGEMENT.md](DATABASE_MANAGEMENT.md)

## 📊 Current Statistics
- **Users**: 16+ registered users
- **Brand Profiles**: 10+ active brands
- **Platform Progress**: 200+ tracking records
- **Backup System**: Automated retention management

## 🔄 Backup & Maintenance

### Automated Systems
- **Database Backups**: Automated backup system
- **Cleanup**: Automated old file removal
- **Monitoring**: Comprehensive logging and alerts

### Manual Operations
```bash
# Database health check
python manage.py check --database=default

# Manual backup
python manage.py production_backup
```

---

**Quantum Digital** - Professional digital branding platform with enterprise-grade backup systems.

*Last updated: 2025-09-15 | Version: 2.0 | Production Ready*