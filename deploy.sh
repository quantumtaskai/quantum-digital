#!/bin/bash

# Deployment script for Quantum Digital to Dockploy

echo "🚀 Preparing deployment to digital.quantumtaskai.com"

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "❌ Git not initialized. Run: git init"
    exit 1
fi

# Add all files
echo "📁 Adding files to git..."
git add .

# Commit changes
echo "💾 Committing changes..."
git commit -m "Deploy to production: $(date)"

# Push to repository
echo "📤 Pushing to repository..."
git push origin main

echo "✅ Code pushed to repository!"
echo ""
echo "🔧 Next steps in Dockploy:"
echo "1. Go to your Dockploy dashboard"
echo "2. Create new application: quantum-digital"
echo "3. Set repository URL and branch: main"
echo "4. Add environment variables from .env.production"
echo "5. Set domain: digital.quantumtaskai.com"
echo "6. Enable SSL/TLS"
echo "7. Deploy!"
echo ""
echo "📖 Full guide: DOCKPLOY_DEPLOYMENT.md"
