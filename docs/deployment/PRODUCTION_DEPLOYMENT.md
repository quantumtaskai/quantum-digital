# Production Deployment Guide

## Database Migration: Neon → Dokploy PostgreSQL

### Pre-deployment Checklist

1. **Dokploy Database Setup**: ✅ Complete
   - PostgreSQL database created
   - External port 5433 configured
   - Internal connection available

2. **Environment Variables**: ✅ Ready
   ```
   DATABASE_URL=postgresql://postgres:Og4My!W6i%lt4U@quantumdigitalproject-quantumdigitaldb-gysrdh:5432/quantum_digital
   ```

3. **Migrations**: ✅ Available
   - All migrations committed to repository
   - Missing dashboard migration added

### Deployment Process

#### Step 1: Deploy Application
1. Update Dokploy application environment variables
2. Deploy/redeploy the application
3. Migrations will run automatically (including Site setup migration)

#### Step 2: Setup Production Environment
After deployment, run this command in Dokploy terminal:
```bash
python manage.py setup_production
```

This will:
- Remove default example.com site
- Ensure production site exists
- Prevent Site domain conflicts

#### Step 3: Import Data (Optional)
If you need to import backup data, use the safe import command:
```bash
# Upload backup file to production environment first
python manage.py import_data_safe neon_backup_clean.json
```

This will:
- Exclude conflicting models (sites.site)
- Import data safely without conflicts
- Continue on errors (non-critical)

### Troubleshooting

#### Issue: "duplicate key value violates unique constraint"
**Solution**: This should be resolved automatically by migration `0007_ensure_site_setup`. If it still occurs, run:
```bash
python manage.py setup_production
```

#### Issue: Missing migrations
**Solution**: Ensure latest code is deployed:
- Check that migrations are in the repository
- Redeploy application to pull latest changes

#### Issue: Site domain conflicts
**Solution**: The setup_production command handles this automatically

### Verification

After deployment, verify:
1. Application loads without errors
2. User authentication works
3. Dashboard displays correctly
4. Admin panel accessible

### Rollback Plan

If issues occur:
1. **Database**: Original Dokploy PostgreSQL is preserved
2. **Code**: Revert to previous commit
3. **Environment**: Restore previous DATABASE_URL if needed

---

## Migration Summary

- **FROM**: Neon Database (quota exceeded)
- **TO**: Dokploy PostgreSQL (fully functional)
- **DATA**: Preserved in backup files
- **STATUS**: Ready for production deployment

All conflicts resolved and production-ready! 🚀