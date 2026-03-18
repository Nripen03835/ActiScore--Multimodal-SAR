from datetime import datetime
from flask_login import UserMixin
from app import db, login_manager
from flask import session

# PostgreSQL-specific imports (will be conditionally imported)
try:
    from sqlalchemy.dialects.postgresql import ARRAY
except ImportError:
    # Fallback for SQLite
    ARRAY = None

@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    
    # Vercel Ephemeral Storage Fix: Recreate user if DB was wiped but session is valid
    if not user and 'user_info' in session:
        info = session['user_info']
        if int(user_id) == info.get('id'):
            user = User(
                id=info['id'],
                name=info['name'],
                email=info['email'],
                role=info['role'],
                password_hash='restored_from_session_cookie'
            )
            try:
                db.session.add(user)
                db.session.commit()
            except Exception:
                db.session.rollback()
                
    return user

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user', nullable=False)  # user, admin
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    videos = db.relationship('Video', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    fer_results = db.relationship('FERResult', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    ser_results = db.relationship('SERResult', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    fusion_results = db.relationship('FusionResult', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    summaries = db.relationship('Summary', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    papers = db.relationship('Paper', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    startups = db.relationship('Startup', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    chat_history = db.relationship('ChatHistory', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    attendance_records = db.relationship('Attendance', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.email}>'
    
    def is_admin(self):
        return self.role == 'admin'

class Video(db.Model):
    __tablename__ = 'videos'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    duration = db.Column(db.Float)  # in seconds
    file_size = db.Column(db.Integer)  # in bytes
    transcript = db.Column(db.Text)
    summary_id = db.Column(db.Integer, db.ForeignKey('summaries.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    processed = db.Column(db.Boolean, default=False)
    processing_status = db.Column(db.String(50), default='pending')  # pending, processing, completed, failed
    
    # Relationships
    fer_results = db.relationship('FERResult', backref='video', lazy='dynamic', cascade='all, delete-orphan')
    ser_results = db.relationship('SERResult', backref='video', lazy='dynamic', cascade='all, delete-orphan')
    fusion_results = db.relationship('FusionResult', backref='video', lazy='dynamic', cascade='all, delete-orphan')
    summary = db.relationship('Summary', backref='videos')

class FERResult(db.Model):
    __tablename__ = 'fer_results'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    video_id = db.Column(db.Integer, db.ForeignKey('videos.id'), nullable=False)
    frame_ts = db.Column(db.Float, nullable=False)  # timestamp in seconds
    face_bbox = db.Column(db.JSON)  # bounding box coordinates
    emotion = db.Column(db.String(50), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class SERResult(db.Model):
    __tablename__ = 'ser_results'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    audio_id = db.Column(db.Integer, db.ForeignKey('videos.id'), nullable=False)
    ts = db.Column(db.Float, nullable=False)  # timestamp in seconds
    emotion = db.Column(db.String(50), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class FusionResult(db.Model):
    __tablename__ = 'fusion_results'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    video_id = db.Column(db.Integer, db.ForeignKey('videos.id'), nullable=False)
    timestamp = db.Column(db.Float, nullable=False)
    fer_emotion = db.Column(db.String(50), nullable=False)
    ser_emotion = db.Column(db.String(50), nullable=False)
    fused_label = db.Column(db.String(50), nullable=False)
    score = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Summary(db.Model):
    __tablename__ = 'summaries'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # video, document, paper, etc.
    original_text_or_file = db.Column(db.Text)
    summary_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # For document summaries
    original_filename = db.Column(db.String(255))
    file_path = db.Column(db.String(500))

class Paper(db.Model):
    __tablename__ = 'papers'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(500), nullable=False)
    keywords = db.Column(db.Text)
    abstract = db.Column(db.Text)
    summary = db.Column(db.Text)
    embedding = db.Column(db.Text)  # Store as JSON text for now
    file_path = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Startup(db.Model):
    __tablename__ = 'startups'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    features_json = db.Column(db.JSON, nullable=False)  # Features for prediction
    success_probability = db.Column(db.Float)
    risk_level = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ChatHistory(db.Model):
    __tablename__ = 'chat_history'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    query = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=False)
    vector_ref = db.Column(db.String(255))  # Reference to vector database
    module_context = db.Column(db.String(50))  # Which module the chat is related to
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Attendance(db.Model):
    __tablename__ = 'attendance'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    datetime = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    location = db.Column(db.String(255))
    face_id = db.Column(db.String(255))
    emotion = db.Column(db.String(50))
    status = db.Column(db.String(20), default='present')  # present, absent, late
    confidence = db.Column(db.Float)
    image_path = db.Column(db.String(500))