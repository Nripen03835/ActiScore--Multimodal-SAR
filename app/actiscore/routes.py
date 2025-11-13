from flask import render_template, request, jsonify, current_app, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app.actiscore import bp
from app import db
from app.models import Video, FERResult, SERResult, FusionResult
from app.models_ml import process_video_emotions_mock
import os
from datetime import datetime
import json

# Import ML libraries (will be used in actual implementation)
# import tensorflow as tf
# from tensorflow.keras.models import load_model
# import librosa

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_VIDEO_EXTENSIONS']

@bp.route('/multimodal-emotion')
@login_required
def multimodal_emotion():
    """Multimodal emotion analysis page"""
    return render_template('actiscore/multimodal_emotion.html')

@bp.route('/process-video', methods=['POST'])
@login_required
def process_video():
    """Process uploaded video for emotion analysis"""
    if 'video' not in request.files:
        return jsonify({'error': 'No video file provided'}), 400
    
    file = request.files['video']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        try:
            # Check file size before processing
            file.seek(0, os.SEEK_END)  # Go to end of file
            file_size = file.tell()    # Get current position (file size)
            file.seek(0)               # Reset to beginning
            
            max_size = current_app.config.get('MAX_CONTENT_LENGTH', 2000 * 1024 * 1024)
            if file_size > max_size:
                return jsonify({'error': f'File size exceeds {max_size // (1024*1024)}MB limit'}), 400
            
            # Generate unique filename
            filename = secure_filename(file.filename)
            unique_filename = f"{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{filename}"
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
            
            # Save file in chunks for large files
            chunk_size = 8192  # 8KB chunks
            with open(filepath, 'wb') as f:
                while True:
                    chunk = file.read(chunk_size)
                    if not chunk:
                        break
                    f.write(chunk)
            
            # Get video info (placeholder for now)
            # In real implementation, use cv2.VideoCapture
            fps = 30  # Default FPS
            frame_count = 300  # Default frame count
            duration = frame_count / fps if fps > 0 else 0
            
            # Create video record
            video = Video(
                user_id=current_user.id,
                filename=unique_filename,
                original_filename=filename,
                file_path=filepath,
                duration=duration,
                file_size=os.path.getsize(filepath),
                processing_status='processing'
            )
            
            db.session.add(video)
            db.session.commit()
            
            # Process video (placeholder for actual ML processing)
            # In real implementation, this would be handled by Celery worker
            process_video_emotions(video.id)
            
            return jsonify({
                'message': 'Video uploaded and processing started',
                'video_id': video.id,
                'filename': filename,
                'duration': duration,
                'frames': frame_count
            }), 200
            
        except Exception as e:
            return jsonify({'error': f'Processing failed: {str(e)}'}), 500
    
    return jsonify({'error': 'Invalid file type'}), 400

def process_video_emotions(video_id):
    """Process video for emotion analysis using mock models"""
    video = Video.query.get(video_id)
    if not video:
        return
    
    try:
        # Use mock processing for demonstration
        results = process_video_emotions_mock(video.file_path, video.user_id, video_id)
        
        # Update video status
        video.processing_status = 'completed'
        video.processed = True
        
        db.session.commit()
        
    except Exception as e:
        video.processing_status = 'failed'
        db.session.commit()
        current_app.logger.error(f"Video processing failed: {str(e)}")

@bp.route('/results/<int:video_id>')
@login_required
def get_results(video_id):
    """Get emotion analysis results for a video"""
    video = Video.query.filter_by(id=video_id, user_id=current_user.id).first()
    if not video:
        return jsonify({'error': 'Video not found'}), 404
    
    # Get FER results
    fer_results = FERResult.query.filter_by(video_id=video_id).all()
    fer_data = [{
        'timestamp': result.frame_ts,
        'emotion': result.emotion,
        'confidence': result.confidence,
        'face_bbox': json.loads(result.face_bbox) if result.face_bbox else None
    } for result in fer_results]
    
    # Get SER results
    ser_results = SERResult.query.filter_by(audio_id=video_id).all()
    ser_data = [{
        'timestamp': result.ts,
        'emotion': result.emotion,
        'confidence': result.confidence
    } for result in ser_results]
    
    # Get fusion results
    fusion_results = FusionResult.query.filter_by(video_id=video_id).all()
    fusion_data = [{
        'timestamp': result.timestamp,
        'fer_emotion': result.fer_emotion,
        'ser_emotion': result.ser_emotion,
        'fused_label': result.fused_label,
        'score': result.score
    } for result in fusion_results]
    
    return jsonify({
        'video_info': {
            'id': video.id,
            'filename': video.original_filename,
            'duration': video.duration,
            'processing_status': video.processing_status
        },
        'fer_results': fer_data,
        'ser_results': ser_data,
        'fusion_results': fusion_data
    }), 200

@bp.route('/live-webcam')
@login_required
def live_webcam():
    """Live webcam emotion analysis page"""
    return render_template('actiscore/live_webcam.html')

@bp.route('/attendance-monitoring')
@login_required
def attendance_monitoring():
    """AI attendance and emotion monitoring page"""
    return render_template('actiscore/attendance_monitoring.html')