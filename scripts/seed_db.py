#!/usr/bin/env python3
"""
Database initialization script for ActiScore application.
Creates all tables and seeds initial data.
"""

import os
import sys
from datetime import datetime
from werkzeug.security import generate_password_hash

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User, Video, FERResult, SERResult, FusionResult, Summary, Paper, Startup, ChatHistory, Attendance
from config import Config

def create_admin_user():
    """Create admin user if it doesn't exist"""
    admin_email = Config.ADMIN_EMAIL
    admin_password = Config.ADMIN_PASSWORD
    
    admin = User.query.filter_by(email=admin_email).first()
    if not admin:
        admin = User(
            name='Admin',
            email=admin_email,
            password_hash=generate_password_hash(admin_password),
            role='admin',
            created_at=datetime.utcnow()
        )
        db.session.add(admin)
        print(f"Created admin user: {admin_email}")
    else:
        print(f"Admin user already exists: {admin_email}")

def create_sample_users():
    """Create sample users for testing"""
    sample_users = [
        {
            'name': 'John Doe',
            'email': 'john@example.com',
            'password': 'password123',
            'role': 'user'
        },
        {
            'name': 'Jane Smith',
            'email': 'jane@example.com',
            'password': 'password123',
            'role': 'user'
        }
    ]
    
    for user_data in sample_users:
        existing_user = User.query.filter_by(email=user_data['email']).first()
        if not existing_user:
            user = User(
                name=user_data['name'],
                email=user_data['email'],
                password_hash=generate_password_hash(user_data['password']),
                role=user_data['role'],
                created_at=datetime.utcnow()
            )
            db.session.add(user)
            print(f"Created sample user: {user_data['email']}")
        else:
            print(f"Sample user already exists: {user_data['email']}")

def create_sample_data():
    """Create sample data for demonstration"""
    # This will be implemented later when we have actual models
    pass

def main():
    """Main function to initialize the database"""
    app = create_app()
    
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("Database tables created successfully!")
        
        print("Creating admin user...")
        create_admin_user()
        
        print("Creating sample users...")
        create_sample_users()
        
        print("Creating sample data...")
        create_sample_data()
        
        try:
            db.session.commit()
            print("Database initialization completed successfully!")
            print("\nDefault credentials:")
            print(f"Admin: {Config.ADMIN_EMAIL} / {Config.ADMIN_PASSWORD}")
            print("Sample users: john@example.com / password123")
            print("              jane@example.com / password123")
        except Exception as e:
            db.session.rollback()
            print(f"Error during database initialization: {e}")
            sys.exit(1)

if __name__ == '__main__':
    main()