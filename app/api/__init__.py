from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
import uuid
from datetime import datetime

bp = Blueprint('api', __name__)

def allowed_file(filename, allowed_extensions):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def generate_unique_filename(original_filename):
    """Generate a unique filename while preserving extension"""
    ext = os.path.splitext(original_filename)[1]
    unique_name = f"{uuid.uuid4().hex}{ext}"
    return unique_name

@bp.route('/upload/video', methods=['POST'])
@login_required
def upload_video():
    """Upload video file for processing"""
    if 'video' not in request.files:
        return jsonify({'error': 'No video file provided'}), 400
    
    file = request.files['video']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename, current_app.config['ALLOWED_VIDEO_EXTENSIONS']):
        try:
            # Generate unique filename
            filename = generate_unique_filename(file.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            
            # Save file
            file.save(filepath)
            
            # Get file info
            file_size = os.path.getsize(filepath)
            
            return jsonify({
                'message': 'Video uploaded successfully',
                'filename': filename,
                'original_filename': file.filename,
                'file_size': file_size,
                'upload_path': filepath
            }), 200
            
        except Exception as e:
            return jsonify({'error': f'Upload failed: {str(e)}'}), 500
    
    return jsonify({'error': 'Invalid file type'}), 400

@bp.route('/upload/document', methods=['POST'])
@login_required
def upload_document():
    """Upload document file for processing"""
    if 'document' not in request.files:
        return jsonify({'error': 'No document file provided'}), 400
    
    file = request.files['document']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename, current_app.config['ALLOWED_DOCUMENT_EXTENSIONS']):
        try:
            # Generate unique filename
            filename = generate_unique_filename(file.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            
            # Save file
            file.save(filepath)
            
            # Get file info
            file_size = os.path.getsize(filepath)
            
            return jsonify({
                'message': 'Document uploaded successfully',
                'filename': filename,
                'original_filename': file.filename,
                'file_size': file_size,
                'upload_path': filepath
            }), 200
            
        except Exception as e:
            return jsonify({'error': f'Upload failed: {str(e)}'}), 500
    
    return jsonify({'error': 'Invalid file type'}), 400

@bp.route('/processing/status/<task_id>')
@login_required
def get_processing_status(task_id):
    """Get processing status for a task"""
    # This would typically check a task queue or database
    # For now, return a mock response
    return jsonify({
        'task_id': task_id,
        'status': 'processing',
        'progress': 75,
        'message': 'Processing video...',
        'estimated_time_remaining': '2 minutes'
    }), 200

@bp.route('/user/stats')
@login_required
def get_user_stats():
    """Get user statistics"""
    from app.models import Video, Summary, Paper
    
    stats = {
        'total_videos': Video.query.filter_by(user_id=current_user.id).count(),
        'total_summaries': Summary.query.filter_by(user_id=current_user.id).count(),
        'total_papers': Paper.query.filter_by(user_id=current_user.id).count(),
        'account_created': current_user.created_at.isoformat(),
        'last_login': current_user.last_login.isoformat() if current_user.last_login else None
    }
    
    return jsonify(stats), 200

@bp.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    }), 200