# Database Management Guide

## Overview
This guide covers all database management tools and procedures for the Quantum Digital application.

## Tools Installed

### 1. django-dbbackup
Automated database backup and restore functionality.

### 2. django-extensions  
Enhanced Django management commands and utilities.

## Database Backup System

### Manual Backup Commands

```bash
# Create a backup of the database
python manage.py dbbackup

# Create a backup with verbose output
python manage.py dbbackup --verbosity=2

# Create media backup (if needed)
python manage.py mediabackup

# Clean up old backups (keeps last 30 days)
python manage.py dbbackup --clean
```

### Automated Daily Backup

```bash
# Run daily backup with cleanup
python manage.py daily_backup --cleanup

# Run daily backup without cleanup
python manage.py daily_backup
```

### Restore from Backup

```bash
# List available backups
ls -la *.sqlite3 *.tar

# Restore from specific backup
python manage.py dbrestore

# Restore from specific file
python manage.py dbrestore --input-filename=default-ark-2025-09-15-033915.sqlite3
```

## Enhanced Django Commands

### Shell Plus (Auto-imports all models)
```bash
# Enhanced shell with all models imported
python manage.py shell_plus

# Shell with SQL query logging
python manage.py shell_plus --print-sql

# IPython shell (if installed)
python manage.py shell_plus --ipython
```

### URL Management
```bash
# Show all URL patterns
python manage.py show_urls

# Show URLs for specific app
python manage.py show_urls --format=table
```

### Database Information
```bash
# Show database schema
python manage.py graph_models --output=db_schema.png

# Reset database (DANGEROUS - use only in development)
python manage.py reset_db
```

## Production Database Management

### Backup Configuration
- **Storage**: Local filesystem with 30-day retention
- **Frequency**: Daily automated backups
- **Location**: `/backups/` directory
- **Format**: SQLite for development, PostgreSQL dump for production

### Production Backup Setup
1. **Environment Variables**: Set `DATABASE_URL` for production
2. **Storage**: Configure cloud storage for production backups
3. **Scheduling**: Set up cron job for daily backups

```bash
# Add to production crontab
0 2 * * * cd /app && python manage.py daily_backup --cleanup
```

## Emergency Procedures

### Database Corruption Recovery
1. **Stop the application**
2. **Restore from latest backup**:
   ```bash
   python manage.py dbrestore
   ```
3. **Verify data integrity**:
   ```bash
   python manage.py check --database=default
   ```
4. **Restart application**

### Migration Rollback
1. **Backup current state**:
   ```bash
   python manage.py dbbackup
   ```
2. **Rollback to previous migration**:
   ```bash
   python manage.py migrate app_name 0004  # Replace with target migration
   ```
3. **Verify application works**

### Site Framework Issues
If Site conflicts occur:
```bash
python manage.py setup_production
```

## Monitoring and Maintenance

### Daily Checks
- [ ] Backup completion status
- [ ] Database connection health
- [ ] Storage space usage
- [ ] Error logs review

### Weekly Maintenance
- [ ] Review backup retention
- [ ] Check database performance
- [ ] Clean up old log files
- [ ] Update backup storage if needed

### Monthly Reviews
- [ ] Database size growth analysis
- [ ] Backup strategy evaluation
- [ ] Security audit of database access
- [ ] Performance optimization review

## Security Best Practices

### Backup Security
- Store backups in secure, encrypted location
- Limit access to backup files
- Regular backup restoration testing
- Off-site backup storage for production

### Database Access
- Use strong database passwords
- Limit database user permissions
- Enable connection logging
- Regular security updates

## Troubleshooting

### Common Issues

**Backup fails with permission error**:
```bash
# Check backup directory permissions
chmod 755 backups/
```

**Restore fails with encoding error**:
```bash
# Use specific encoding
python manage.py dbrestore --input-encoding=utf-8
```

**Site framework conflicts**:
```bash
# Run production setup
python manage.py setup_production
```

### Getting Help
- Check Django logs: `python manage.py check`
- Database status: `python manage.py dbshell`
- System status: Review application logs

## Contact and Support
- **Database Issues**: Check logs first, then escalate
- **Backup Problems**: Verify storage space and permissions
- **Performance Issues**: Run `python manage.py shell_plus --print-sql` to debug

---
*Last updated: 2025-09-15*
*Version: 1.0*