#!/usr/bin/env python3
"""
Run script for the ActiScore Flask application.
"""

import os
import sys
from app import create_app, db
from app.models import User
from config import config

def main():
    """Main function to run the Flask application"""
    # Get configuration from environment variable or use development config
    config_name = os.environ.get('FLASK_CONFIG') or 'development'
    app = create_app(config[config_name])
    
    # Create admin user if it doesn't exist
    with app.app_context():
        # Create database tables first
        db.create_all()
        print("Database tables created successfully!")
        
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
    
    # Run the application
    if config_name == 'development':
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()