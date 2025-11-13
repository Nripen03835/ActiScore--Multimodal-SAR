#!/usr/bin/env python3
"""
Vercel entry point for the ActiScore Flask application.
"""

import os
import sys
from app import create_app, db
from app.models import User
from config_vercel import config

# Get configuration for Vercel deployment
config_name = 'vercel'
app = create_app(config[config_name])

# Ensure database is created and admin user exists
def initialize_app():
    with app.app_context():
        try:
            # Create database tables
            db.create_all()
            print("Database tables created successfully!")
            
            # Create admin user if it doesn't exist
            admin = User.query.filter_by(email=app.config['ADMIN_EMAIL']).first()
            if not admin:
                from werkzeug.security import generate_password_hash
                from datetime import datetime
                
                admin = User(
                    name='Admin',
                    email=app.config['ADMIN_EMAIL'],
                    password_hash=generate_password_hash(app.config['ADMIN_PASSWORD']),
                    role='admin',
                    created_at=datetime.utcnow()
                )
                db.session.add(admin)
                db.session.commit()
                print(f"Created admin user: {app.config['ADMIN_EMAIL']}")
        except Exception as e:
            print(f"Initialization error: {e}")

# Initialize the application
initialize_app()

# Vercel requires the app to be named 'app'
app = app

# For local testing
if __name__ == '__main__':
    initialize_app()
    app.run(host='0.0.0.0', port=5000)