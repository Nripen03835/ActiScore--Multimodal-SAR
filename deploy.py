#!/usr/bin/env python3
"""
Simple deployment script for ActiScore API
"""

import subprocess
import os
import sys

def deploy_to_vercel():
    """Deploy the application to Vercel"""
    print("🚀 Starting ActiScore deployment to Vercel...")
    
    # Change to deployment directory
    os.chdir('deployment')
    
    # Create vercel.json with proper configuration
    vercel_config = {
        "version": 2,
        "builds": [
            {
                "src": "app.py",
                "use": "@vercel/python",
                "config": {
                    "maxLambdaSize": "15mb"
                }
            }
        ],
        "routes": [
            {
                "src": "/(.*)",
                "dest": "app.py"
            }
        ],
        "env": {
            "SECRET_KEY": "your-secret-key-here",
            "ADMIN_EMAIL": "admin@actiscore.com",
            "ADMIN_PASSWORD": "admin123"
        }
    }
    
    with open('vercel.json', 'w') as f:
        import json
        json.dump(vercel_config, f, indent=2)
    
    print("✅ Vercel configuration created")
    print("✅ Deployment files prepared")
    print("\n📋 Deployment Summary:")
    print("- Application: ActiScore API")
    print("- Endpoints: /, /health, /contact/submit, /api/status")
    print("- Features: Contact form, API status, Health check")
    print("\n📝 Next steps:")
    print("1. Install Vercel CLI: npm install -g vercel")
    print("2. Run: vercel deploy")
    print("3. Set environment variables in Vercel dashboard")
    print("\n✨ Deployment ready!")

if __name__ == '__main__':
    deploy_to_vercel()