from flask import render_template, request, jsonify, current_app
from app.auth.utils import login_required, current_user
from app.main import bp
from app.models import User, Video, Summary, Paper
from app import db
import os

@bp.route('/')
def index():
    """Landing page with 3D hero animation"""
    return render_template('index.html')

@bp.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard with AI module cards"""
    user_videos = Video.query.filter_by(user_id=current_user.id).count()
    user_summaries = Summary.query.filter_by(user_id=current_user.id).count()
    user_papers = Paper.query.filter_by(user_id=current_user.id).count()
    
    return render_template('dashboard.html',
                         user_videos=user_videos,
                         user_summaries=user_summaries,
                         user_papers=user_papers)

@bp.route('/profile')
@login_required
def profile():
    """User profile page"""
    return render_template('profile.html', user=current_user)

@bp.route('/reports')
@login_required
def reports():
    """Analytics and reports page"""
    return render_template('reports.html')

@bp.route('/projects')
@login_required
def projects():
    """Projects management page"""
    return render_template('projects.html')

@bp.route('/documentation')
def documentation():
    """Documentation page"""
    return render_template('documentation.html')

@bp.route('/api-reference')
def api_reference():
    """API Reference page"""
    return render_template('api_reference.html')

@bp.route('/contact')
def contact():
    """Contact page"""
    return render_template('contact.html')

@bp.route('/contact/submit', methods=['POST'])
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
        
        # Validate subject is from allowed options
        valid_subjects = ['general', 'support', 'feature', 'bug', 'billing', 'partnership', 'other']
        if subject not in valid_subjects:
            return jsonify({'error': 'Invalid subject selection'}), 400
        
        # In a real application, you would:
        # 1. Save to database
        # 2. Send email notification
        # 3. Integrate with support system
        # For now, we'll just return success
        
        print(f"Contact form submitted:")
        print(f"From: {first_name} {last_name} ({email})")
        print(f"Subject: {subject}")
        print(f"Message: {message[:100]}...")
        
        return jsonify({
            'message': 'Your message has been sent successfully! We will get back to you within 24 hours.',
            'ticket_id': f'TICKET-{hash(email + str(int(__import__('time').time()))) % 10000:04d}'
        }), 200
        
    except Exception as e:
        print(f"Contact form error: {str(e)}")
        return jsonify({'error': 'Failed to process contact form. Please try again later.'}), 500

@bp.route('/privacy')
def privacy():
    """Privacy Policy page"""
    return render_template('privacy.html')

@bp.route('/faq')
def faq():
    """FAQ page"""
    return render_template('faq.html')

@bp.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@bp.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500