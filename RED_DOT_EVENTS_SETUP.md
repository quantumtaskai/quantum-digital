# Red Dot Events Brand Setup

This document explains how to create the "Red Dot Events" brand with complete platform data that matches the dashboard screenshot provided.

## Quick Setup

When the database is available, run this management command to create the complete Red Dot Events brand:

```bash
# Activate virtual environment
source venv/bin/activate

# Create Red Dot Events brand with all data
python manage.py create_red_dot_events

# Verify creation (dry run first)
python manage.py create_red_dot_events --dry-run
```

## What Gets Created

### Brand Profile
- **Brand Name**: Red Dot Events
- **Contact**: Sarah Johnson (sarah@reddotevents.com)
- **Website**: https://reddotevents.com
- **Vision**: Creating unforgettable experiences through innovative event planning and digital marketing
- **Public Dashboard**: Enabled with UUID `12345678-1234-5678-9abc-123456789abc`

### Platform Progress Data (Matching Screenshot)

#### Header Metrics
- **Total Platforms**: 13 active platforms (out of 22 total)
- **Active Platforms**: 6 (platforms with committed > 0)
- **Content Committed**: 1,030 total pieces
- **Total Drafted**: 109 pieces

#### Platform Details

**High Activity Platforms:**
- **Instagram**: 160 committed, 45 drafted, 0 published (ACTIVE)
- **Pinterest**: 180 committed, 0 drafted, 1 published (ACTIVE)
- **Twitter/X**: 180 committed, 10 drafted, 1 published (ACTIVE)
- **Facebook**: 180 committed, 10 drafted, 0 published (ACTIVE)

**Medium Activity Platforms:**
- **Google Business**: 100 committed, 11 drafted, 0 published (ACTIVE)
- **Website Blogs**: 50 committed, 10 drafted, 0 published (ACTIVE)
- **LinkedIn**: 45 committed, 10 drafted, 0 published (NOT ACTIVE)

**Low Activity Platforms:**
- **Medium**: 30 committed, 0 drafted, 2 published (ACTIVE)
- **Threads**: 30 committed, 0 drafted, 0 published (NOT ACTIVE)
- **Tumblr**: 30 committed, 10 drafted, 1 published (ACTIVE)
- **Website Downloadable**: 10 committed, 1 drafted, 0 published (NOT ACTIVE)
- **TikTok**: 10 committed, 1 drafted, 0 published (NOT ACTIVE)
- **YouTube**: 5 committed, 1 drafted, 0 published (NOT ACTIVE)

### Content Links (Blue Buttons)

The following platforms have content links matching the screenshot:
- **Website Blogs**: "View Content Plan" → Content planning spreadsheet
- **Google Business**: "Visit Platform" → Google Business profile
- **LinkedIn**: "View Content Plan" → LinkedIn content strategy
- **Instagram**: "View Content Plan" → Instagram content calendar
- **Pinterest**: "Visit Platform" → Pinterest profile
- **Twitter**: "Visit Platform" → Twitter profile
- **Facebook**: "Visit Platform" → Facebook page
- **Medium**: "View Content Plan" → Medium publication strategy
- **Tumblr**: "Visit Platform" → Tumblr blog

## Dashboard URLs

After creation, access the dashboards at:

### Manager Dashboard
```
http://localhost:8000/manager/brand/{brand_id}/
```

### Public Dashboard
```
http://localhost:8000/dashboard/public/12345678-1234-5678-9abc-123456789abc/
```

## Verification Checklist

After running the command, verify the following match the screenshot:

✅ **Header Metrics**
- [ ] Total Platforms: 13+ (should show active platforms)
- [ ] Active: 6 (platforms with committed > 0)
- [ ] Content Committed: 1030
- [ ] Total Drafted: 109

✅ **Platform Status Overview (Pie Chart)**
- [ ] Active platforms: 6 (green)
- [ ] Inactive platforms: 7+ (red) 
- [ ] Chart displays correctly with proper colors

✅ **Content Metrics Card**
- [ ] Committed: 1030
- [ ] Drafted: 109
- [ ] Rate: ~11% (109/1030 * 100)

✅ **Platform Details**
- [ ] All platforms show correct committed/drafted/published numbers
- [ ] Status badges show ACTIVE/NOT ACTIVE correctly
- [ ] Content links appear as blue buttons where specified
- [ ] Platform categories display properly

## Troubleshooting

### Database Connection Issues
If you get database connection errors, ensure:
1. PostgreSQL service is running
2. Database credentials are correct in settings
3. Network connectivity to database server

### Missing Platform Records
If some platforms are missing:
```bash
# Run the platform creation command for existing brands
python manage.py create_platform_records
```

### Incorrect Data
To reset and recreate:
```bash
# Delete the brand (if needed)
python manage.py shell -c "
from profiles.models import BrandProfile
BrandProfile.objects.filter(brand_name='Red Dot Events').delete()
"

# Recreate with fresh data
python manage.py create_red_dot_events
```

## Notes

- The brand uses realistic data that matches the screenshot exactly
- All platform records are created even if not shown in screenshot
- Content links are actual URLs that can be updated to real resources
- The public dashboard UUID is fixed for consistent testing
- Platform progress data reflects a real event marketing agency workflow