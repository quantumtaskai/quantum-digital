# Social Authentication Setup Guide

This guide walks you through setting up OAuth credentials for various social login providers.

## 1. Google OAuth2 Setup

### Step 1: Go to Google Cloud Console
1. Visit [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the "Google+ API" and "Google OAuth2 API"

### Step 2: Create OAuth2 Credentials
1. Go to "Credentials" in the left sidebar
2. Click "Create Credentials" → "OAuth client ID"
3. Choose "Web application"
4. Add authorized redirect URIs:
   - `http://127.0.0.1:8001/accounts/google/login/callback/` (development)
   - `https://your-domain.com/accounts/google/login/callback/` (production)

### Step 3: Update Environment Variables
```bash
GOOGLE_OAUTH2_CLIENT_ID=your-actual-google-client-id
GOOGLE_OAUTH2_CLIENT_SECRET=your-actual-google-client-secret
```

## 2. Facebook OAuth2 Setup

### Step 1: Create Facebook App
1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Create a new app
3. Add "Facebook Login" product

### Step 2: Configure OAuth Settings
1. In Facebook Login settings, add Valid OAuth Redirect URIs:
   - `http://127.0.0.1:8001/accounts/facebook/login/callback/` (development)
   - `https://your-domain.com/accounts/facebook/login/callback/` (production)

### Step 3: Update Environment Variables
```bash
FACEBOOK_APP_ID=your-facebook-app-id
FACEBOOK_APP_SECRET=your-facebook-app-secret
```

## 3. GitHub OAuth2 Setup

### Step 1: Create GitHub OAuth App
1. Go to GitHub Settings → Developer settings → OAuth Apps
2. Click "New OAuth App"
3. Set Authorization callback URL:
   - `http://127.0.0.1:8001/accounts/github/login/callback/` (development)
   - `https://your-domain.com/accounts/github/login/callback/` (production)

### Step 2: Update Environment Variables
```bash
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret
```

## 4. LinkedIn OAuth2 Setup

### Step 1: Create LinkedIn App
1. Go to [LinkedIn Developers](https://www.linkedin.com/developers/apps)
2. Create a new app
3. Add "Sign In with LinkedIn" product

### Step 2: Configure OAuth Settings
1. Add authorized redirect URLs:
   - `http://127.0.0.1:8001/accounts/linkedin_oauth2/login/callback/` (development)
   - `https://your-domain.com/accounts/linkedin_oauth2/login/callback/` (production)

### Step 3: Update Environment Variables
```bash
LINKEDIN_OAUTH2_CLIENT_ID=your-linkedin-client-id
LINKEDIN_OAUTH2_CLIENT_SECRET=your-linkedin-client-secret
```

## 5. Django Admin Configuration

After setting up the OAuth credentials, you need to configure them in Django admin:

1. Start your Django server: `python manage.py runserver`
2. Go to `http://127.0.0.1:8001/admin/`
3. Navigate to "Sites" → "Sites" and ensure you have a site with domain `127.0.0.1:8001` for development
4. Go to "Social Accounts" → "Social applications"
5. For each provider, create a new Social application:
   - **Provider**: Choose the provider (Google, Facebook, etc.)
   - **Name**: Give it a name (e.g., "Google OAuth")
   - **Client id**: Your OAuth client ID
   - **Secret key**: Your OAuth client secret
   - **Sites**: Select your site(s)

## Testing Social Login

Once configured, you can test social login by:
1. Going to the login page: `http://127.0.0.1:8001/accounts/login/`
2. You should see social login buttons
3. Click on a provider button to test the OAuth flow

## Important Security Notes

- Keep your OAuth secrets secure and never commit them to version control
- Use environment variables for all sensitive credentials
- Set up proper redirect URIs for production
- Regularly rotate your OAuth secrets
- Test the complete OAuth flow in both development and production environments
