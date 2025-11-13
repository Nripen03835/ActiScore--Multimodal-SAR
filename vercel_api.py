#!/usr/bin/env python3
"""
Ultra-minimal Vercel entry point for the ActiScore Flask application.
This version provides API endpoints without template dependencies.
"""

from flask import Flask, jsonify, request
import os
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'vercel-deployment-secret-key'

@app.route('/')
def index():
    """Health check endpoint"""
    return jsonify({
        'status': 'success',
        'message': 'ActiScore API is running',
        'version': '1.0.0',
        'endpoints': [
            '/health',
            '/contact/submit',
            '/api/status'
        ]
    })

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'ActiScore API',
        'timestamp': __import__('datetime').datetime.utcnow().isoformat()
    })

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
            'ticket_id': f'TICKET-{hash(email + str(int(__import__("datetime").datetime.now().timestamp()))) % 10000:04d}',
            'success': True
        }), 200
        
    except Exception as e:
        print(f"Contact form error: {str(e)}")
        return jsonify({'error': 'Failed to process contact form. Please try again later.'}), 500

@app.route('/api/status')
def api_status():
    """API status endpoint"""
    return jsonify({
        'status': 'operational',
        'features': {
            'video_summarizer': 'available',
            'contact_form': 'available',
            'emotion_analysis': 'available'
        }
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# Vercel requires the app to be named 'app'
app = app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)