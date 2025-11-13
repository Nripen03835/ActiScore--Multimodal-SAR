#!/usr/bin/env python3
"""
Lightweight Vercel entry point for the ActiScore Flask application.
This version is optimized for serverless deployment without large model files.
"""

import os
import sys
from app import create_app, db
from app.models import User
from config_vercel import config

# Get configuration for Vercel deployment
config_name = 'vercel'
app = create_app(config[config_name])

# Mock the ML models for lightweight deployment
import app.intellilearn.routes as intellilearn_routes
import app.actiscore.routes as actiscore_routes

# Override model loading with mock functions
def mock_load_models():
    """Mock model loading for deployment without large files"""
    return {
        'fer_model': {'loaded': False, 'type': None, 'accuracy': 0, 'emotions': []},
        'ser_model': {'loaded': True, 'type': 'ser_svm', 'accuracy': 0.68, 'emotions': ['neutral', 'calm', 'happy', 'sad', 'angry', 'fearful', 'disgust', 'surprised']},
        'fusion_model': {'loaded': True, 'type': 'fusion_ensemble', 'accuracy': 0.82, 'emotions': ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']}
    }

# Apply mock models
intellilearn_routes.models = mock_load_models()
actiscore_routes.models = mock_load_models()

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