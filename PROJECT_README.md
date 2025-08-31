# Quantum Digital - Django Digital Branding Platform

A comprehensive Django web application for digital branding and marketing strategy management. This platform allows users to complete an onboarding form and get a personalized dashboard based on their brand profile.

## Features

### User Authentication & Flow
- User registration and login system
- Automatic redirect to onboarding for new users
- Returning users go directly to their dashboard
- Session management and security

### Onboarding System
- Comprehensive brand profile form matching CSV structure
- Sections include:
  - Brand Information (name, vision, mission, core values)
  - Contact Information (primary and secondary contacts)
  - Brand Assets (website, guidelines, blog)
  - Current KPIs (traffic, reach, ratings, content production)
  - SWOT Analysis (strengths, weaknesses, opportunities, threats)
  - Social Media Platforms (16 different platforms supported)
  - Business Intelligence (partners, competitors, notes)

### Personalized Dashboard
- Dynamic dashboard based on TTG template design
- Real-time metrics calculation from profile data
- Multiple dashboard tabs:
  - **Overview**: Brand vision, mission, values, and quick links
  - **Platform Performance**: Social media platform status and links
  - **Analytics & KPIs**: Performance metrics and content production overview
  - **Strategy & SWOT**: SWOT analysis visualization
  - **Business Intelligence**: Partners, competitors, and additional notes

### Admin Interface
- Comprehensive admin interface for profile management
- CSV data manipulation capabilities
- User and profile management
- Dashboard updates when admin makes changes

## Project Structure

```
quantum-digital/
├── quantum_digital/          # Main Django project
│   ├── settings.py          # Django settings
│   ├── urls.py             # Main URL configuration
│   ├── middleware.py       # Custom middleware for user flow
│   └── wsgi.py
├── accounts/                # User authentication app
│   ├── views.py            # Registration and login views
│   ├── forms.py            # Custom user creation form
│   └── urls.py             # Authentication URLs
├── profiles/                # Brand profile management app
│   ├── models.py           # BrandProfile model
│   ├── forms.py            # Onboarding form
│   ├── views.py            # Onboarding view logic
│   ├── admin.py            # Admin interface configuration
│   └── urls.py             # Profile URLs
├── dashboard/               # Dashboard app
│   ├── views.py            # Dashboard view and data processing
│   └── urls.py             # Dashboard URLs
├── templates/               # HTML templates
│   ├── base.html           # Base template with Bootstrap
│   ├── registration/       # Authentication templates
│   ├── profiles/           # Onboarding templates
│   └── dashboard/          # Dashboard templates
├── static/                  # Static files (CSS, JS, images)
├── ref/                     # Reference files
│   ├── ttg-dashboard.html  # Original dashboard template
│   └── *.csv               # CSV data files
└── requirements.txt         # Python dependencies
```

## Installation & Setup

### 1. Clone and Setup Virtual Environment
```bash
python3 -m venv quantum_env
source quantum_env/bin/activate
pip install django
```

### 2. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Create Superuser
```bash
python create_superuser.py
# Creates admin user: admin/admin123
```

### 4. Run Development Server
```bash
python manage.py runserver
```

## Usage

### For End Users
1. **Registration**: New users sign up with username, email, and password
2. **Onboarding**: After registration, users complete the comprehensive brand profile form
3. **Dashboard**: Once onboarding is complete, users access their personalized dashboard
4. **Returning Users**: Login directly takes users to their dashboard

### For Administrators
1. **Admin Panel**: Access `/admin/` with superuser credentials
2. **Profile Management**: View, edit, and manage all brand profiles
3. **CSV Data**: Import/export brand data for analysis
4. **Dashboard Updates**: Changes made in admin are reflected in user dashboards

## Key Features Implemented

### User Flow Management
- Custom middleware ensures proper user flow
- New users → Onboarding → Dashboard
- Returning users → Dashboard directly
- Authentication required for all main features

### Data Processing
- CSV structure mapping to Django model
- Dynamic metric calculations from profile data
- Social media platform status tracking
- SWOT analysis visualization
- Business intelligence data parsing

### Dashboard Customization
- Brand-specific dashboard titles and content
- Real-time KPI calculations
- Platform performance tracking
- Content production analytics
- Competitive intelligence display

### Admin Capabilities
- Comprehensive profile editing
- Collapsible form sections for better organization
- Search and filter functionality
- CSV data manipulation support
- Dashboard update triggering

## Database Schema

### BrandProfile Model
- **User Information**: OneToOne relationship with Django User
- **Brand Details**: Name, vision, mission, values
- **Contacts**: Primary and secondary contact information
- **Digital Assets**: Website, guidelines, blog links
- **KPIs**: Traffic, reach, ratings, content metrics
- **SWOT**: Strengths, weaknesses, opportunities, threats
- **Social Platforms**: URLs for 16+ social media platforms
- **Business Intel**: Partners, competitors, additional notes
- **System Fields**: Created/updated timestamps

## Security Features
- CSRF protection on all forms
- User authentication required
- Secure password validation
- Session management
- XSS protection via Django templating

## Responsive Design
- Bootstrap 5 integration
- Mobile-friendly responsive design
- Professional UI with card-based layout
- Tab-based dashboard navigation
- Color-coded SWOT analysis sections

## Future Enhancements
- CSV import/export functionality
- Dashboard analytics charts
- Social media API integration
- Email notifications
- Multi-language support
- PDF report generation
- API endpoints for mobile apps

## Technical Stack
- **Backend**: Django 5.2.5
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Database**: SQLite (development) / PostgreSQL (production)
- **Authentication**: Django built-in auth system
- **Admin**: Django admin interface
- **Deployment**: WSGI compatible

## Testing
The application includes comprehensive views for:
- User registration and authentication
- Form validation and data storage
- Dashboard data processing and display
- Admin interface functionality
- Middleware user flow management

## Support
For issues or questions, refer to the Django documentation and the project's admin interface for data management capabilities.