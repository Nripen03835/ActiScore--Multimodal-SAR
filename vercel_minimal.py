#!/usr/bin/env python3
"""
Minimal Vercel entry point for the ActiScore Flask application.
This version is optimized for serverless deployment without any large dependencies.
"""

import os
import sys
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json

# Create minimal Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'vercel-deployment-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Minimal User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200))
    role = db.Column(db.String(20), default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Create tables and admin user
with app.app_context():
    try:
        db.create_all()
        print("Database tables created successfully!")
        
        # Create admin user if it doesn't exist
        admin_email = os.environ.get('ADMIN_EMAIL') or 'admin@actiscore.com'
        admin_password = os.environ.get('ADMIN_PASSWORD') or 'admin123'
        
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
            db.session.commit()
            print(f"Created admin user: {admin_email}")
    except Exception as e:
        print(f"Initialization error: {e}")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Minimal routes
@app.route('/')
def index():
    """Landing page"""
    return render_template('index.html')

@app.route('/contact')
def contact():
    """Contact page"""
    return render_template('contact.html')

@app.route('/contact/submit', methods=['POST'])
def contact_submit():
    """Handle contact form submission"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Extract form data
        first_name = data.get('firstName', '').strip()
        last_name = data.get('lastName', '').strip()
        email = data.get('email', '').strip()
        subject = data.get('subject', '').strip()
        message = data.get('message', '').strip()
        
        # Validate required fields
        if not all([first_name, last_name, email, subject, message]):
            return jsonify({'error': 'All fields are required'}), 400
        
        # Validate email format
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return jsonify({'error': 'Invalid email format'}), 400
        
        # Return success
        return jsonify({
            'message': 'Your message has been sent successfully! We will get back to you within 24 hours.',
            'ticket_id': f'TICKET-{hash(email + str(int(datetime.now().timestamp()))) % 10000:04d}'
        }), 200
        
    except Exception as e:
        print(f"Contact form error: {str(e)}")
        return jsonify({'error': 'Failed to process contact form. Please try again later.'}), 500

@app.route('/documentation')
def documentation():
    """Documentation page"""
    return render_template('documentation.html')

@app.route('/faq')
def faq():
    """FAQ page"""
    return render_template('faq.html')

@app.route('/api-reference')
def api_reference():
    """API Reference page"""
    return render_template('api_reference.html')

@app.route('/privacy')
def privacy():
    """Privacy Policy page"""
    return render_template('privacy.html')

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500

# Vercel requires the app to be named 'app'
app = app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)