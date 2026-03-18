from flask import render_template, request, jsonify, redirect, url_for, flash
from app.auth.utils import login_required, current_user
from functools import wraps
from app.admin import bp
from app import db
from app.models import User, Video, Summary, Paper, Startup, ChatHistory
from datetime import datetime, timedelta
import json

def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('Admin access required', 'error')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """Admin dashboard with statistics"""
    # Get statistics
    total_users = User.query.count()
    total_videos = Video.query.count()
    total_summaries = Summary.query.count()
    total_papers = Paper.query.count()
    
    # Get recent users
    recent_users = User.query.order_by(User.created_at.desc()).limit(10).all()
    
    # Get processing status
    processing_stats = {
        'pending': Video.query.filter_by(processing_status='pending').count(),
        'processing': Video.query.filter_by(processing_status='processing').count(),
        'completed': Video.query.filter_by(processing_status='completed').count(),
        'failed': Video.query.filter_by(processing_status='failed').count()
    }
    
    return render_template('admin/dashboard.html',
                         total_users=total_users,
                         total_videos=total_videos,
                         total_summaries=total_summaries,
                         total_papers=total_papers,
                         recent_users=recent_users,
                         processing_stats=processing_stats)

@bp.route('/users')
@login_required
@admin_required
def users():
    """User management page"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    
    query = User.query
    if search:
        query = query.filter(User.name.contains(search) | User.email.contains(search))
    
    users = query.paginate(page=page, per_page=20, error_out=False)
    
    return render_template('admin/users.html', users=users, search=search)

@bp.route('/users/<int:user_id>')
@login_required
@admin_required
def user_detail(user_id):
    """User detail page"""
    user = User.query.get_or_404(user_id)
    
    # Get user's content statistics
    user_stats = {
        'videos': Video.query.filter_by(user_id=user_id).count(),
        'summaries': Summary.query.filter_by(user_id=user_id).count(),
        'papers': Paper.query.filter_by(user_id=user_id).count(),
        'startups': Startup.query.filter_by(user_id=user_id).count(),
        'chats': ChatHistory.query.filter_by(user_id=user_id).count()
    }
    
    # Get recent activity
    recent_videos = Video.query.filter_by(user_id=user_id).order_by(Video.created_at.desc()).limit(5).all()
    recent_summaries = Summary.query.filter_by(user_id=user_id).order_by(Summary.created_at.desc()).limit(5).all()
    
    return render_template('admin/user_detail.html',
                         user=user,
                         user_stats=user_stats,
                         recent_videos=recent_videos,
                         recent_summaries=recent_summaries)

@bp.route('/users/<int:user_id>/toggle-status', methods=['POST'])
@login_required
@admin_required
def toggle_user_status(user_id):
    """Toggle user active status"""
    user = User.query.get_or_404(user_id)
    user.is_active = not user.is_active
    db.session.commit()
    
    status = 'activated' if user.is_active else 'deactivated'
    flash(f'User {user.name} has been {status}', 'success')
    
    return jsonify({'success': True, 'is_active': user.is_active})

@bp.route('/users/<int:user_id>/update-role', methods=['POST'])
@login_required
@admin_required
def update_user_role(user_id):
    """Update user role"""
    user = User.query.get_or_404(user_id)
    new_role = request.json.get('role')
    
    if new_role not in ['user', 'admin']:
        return jsonify({'error': 'Invalid role'}), 400
    
    user.role = new_role
    db.session.commit()
    
    flash(f'User role updated to {new_role}', 'success')
    return jsonify({'success': True, 'role': new_role})

@bp.route('/content')
@login_required
@admin_required
def content():
    """Content management page"""
    page = request.args.get('page', 1, type=int)
    content_type = request.args.get('type', 'videos', type=str)
    
    if content_type == 'videos':
        query = Video.query
    elif content_type == 'summaries':
        query = Summary.query
    elif content_type == 'papers':
        query = Paper.query
    else:
        query = Video.query
    
    content_items = query.order_by(Video.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('admin/content.html',
                         content_items=content_items,
                         content_type=content_type)

@bp.route('/analytics')
@login_required
@admin_required
def analytics():
    """Analytics dashboard"""
    # Get date range
    days = request.args.get('days', 30, type=int)
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Get analytics data
    user_growth = get_user_growth_data(start_date)
    content_growth = get_content_growth_data(start_date)
    processing_stats = get_processing_stats()
    
    return render_template('admin/analytics.html',
                         user_growth=user_growth,
                         content_growth=content_growth,
                         processing_stats=processing_stats,
                         days=days)

def get_user_growth_data(start_date):
    """Get user growth data for analytics"""
    from sqlalchemy import func
    
    user_data = db.session.query(
        func.date(User.created_at).label('date'),
        func.count(User.id).label('count')
    ).filter(User.created_at >= start_date).group_by(
        func.date(User.created_at)
    ).order_by(func.date(User.created_at)).all()
    
    return [{'date': str(item.date), 'count': item.count} for item in user_data]

def get_content_growth_data(start_date):
    """Get content growth data for analytics"""
    from sqlalchemy import func
    
    video_data = db.session.query(
        func.date(Video.created_at).label('date'),
        func.count(Video.id).label('count')
    ).filter(Video.created_at >= start_date).group_by(
        func.date(Video.created_at)
    ).order_by(func.date(Video.created_at)).all()
    
    summary_data = db.session.query(
        func.date(Summary.created_at).label('date'),
        func.count(Summary.id).label('count')
    ).filter(Summary.created_at >= start_date).group_by(
        func.date(Summary.created_at)
    ).order_by(func.date(Summary.created_at)).all()
    
    return {
        'videos': [{'date': str(item.date), 'count': item.count} for item in video_data],
        'summaries': [{'date': str(item.date), 'count': item.count} for item in summary_data]
    }

def get_processing_stats():
    """Get video processing statistics"""
    total = Video.query.count()
    completed = Video.query.filter_by(processing_status='completed').count()
    processing = Video.query.filter_by(processing_status='processing').count()
    failed = Video.query.filter_by(processing_status='failed').count()
    pending = Video.query.filter_by(processing_status='pending').count()
    
    return {
        'total': total,
        'completed': completed,
        'processing': processing,
        'failed': failed,
        'pending': pending,
        'success_rate': (completed / total * 100) if total > 0 else 0
    }

@bp.route('/system-info')
@login_required
@admin_required
def system_info():
    """System information page"""
    import platform
    import psutil
    
    # Get system information
    system_info = {
        'platform': platform.platform(),
        'python_version': platform.python_version(),
        'cpu_count': psutil.cpu_count(),
        'memory_total': psutil.virtual_memory().total,
        'memory_available': psutil.virtual_memory().available,
        'disk_usage': psutil.disk_usage('/')._asdict()
    }
    
    # Get database info
    from sqlalchemy import text
    
    try:
        db_stats = db.session.execute(text("""
            SELECT 
                COUNT(*) as total_tables,
                pg_size_pretty(pg_database_size(current_database())) as db_size
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)).fetchone()
        
        system_info['database'] = {
            'total_tables': db_stats[0] if db_stats else 0,
            'db_size': db_stats[1] if db_stats else 'Unknown'
        }
    except:
        # SQLite fallback
        system_info['database'] = {
            'total_tables': 'Unknown',
            'db_size': 'Unknown'
        }
    
    return render_template('admin/system_info.html', system_info=system_info)

@bp.route('/settings')
@login_required
@admin_required
def settings():
    """Application settings page"""
    from flask import current_app
    
    config_info = {
        'secret_key_set': bool(current_app.config.get('SECRET_KEY')),
        'upload_folder': current_app.config.get('UPLOAD_FOLDER'),
        'max_file_size': current_app.config.get('MAX_CONTENT_LENGTH'),
        'allowed_video_types': list(current_app.config.get('ALLOWED_VIDEO_EXTENSIONS', [])),
        'allowed_audio_types': list(current_app.config.get('ALLOWED_AUDIO_EXTENSIONS', [])),
        'allowed_document_types': list(current_app.config.get('ALLOWED_DOCUMENT_EXTENSIONS', []))
    }
    
    return render_template('admin/settings.html', config_info=config_info)