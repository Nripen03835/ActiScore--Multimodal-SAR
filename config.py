import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # File upload configuration
    UPLOAD_FOLDER = os.path.join(basedir, 'uploads')
    MODEL_FOLDER = os.path.join(basedir, 'models')
    MAX_CONTENT_LENGTH = 2000 * 1024 * 1024  # 2000MB max file size
    
    # Additional upload settings for large files
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None  # No time limit for large uploads
    
    # Request timeout settings (in seconds)
    REQUEST_TIMEOUT = 300  # 5 minutes for large file uploads
    
    # Memory settings for file handling
    SEND_FILE_MAX_AGE_DEFAULT = 0  # Disable caching for uploaded files
    
    # Flask-WTF settings for large files
    MAX_FORM_MEMORY_SIZE = 2000 * 1024 * 1024  # 2000MB for form data
    MAX_FORM_PARTS = 1000  # Allow many form parts for large uploads
    
    # Allowed file extensions
    ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'webm'}
    ALLOWED_AUDIO_EXTENSIONS = {'wav', 'mp3', 'flac', 'aac', 'm4a'}
    ALLOWED_DOCUMENT_EXTENSIONS = {'pdf', 'txt', 'doc', 'docx'}
    
    # Model configuration
    MODEL_DIR = os.path.join(basedir, 'models')
    FER_MODEL_PATH = os.path.join(MODEL_DIR, 'fer_model.h5')
    SER_MODEL_PATH = os.path.join(MODEL_DIR, 'ser_model.pkl')
    FUSION_MODEL_PATH = os.path.join(MODEL_DIR, 'fusion_model.pkl')
    FEATURE_SCALER_PATH = os.path.join(MODEL_DIR, 'feature_scaler_efficient.pkl')
    
    # FAISS configuration
    FAISS_INDEX_PATH = os.path.join(MODEL_DIR, 'faiss_index.bin')
    
    # Cache configuration
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 300
    
    # Redis configuration (for Celery)
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379/0'
    
    # Email configuration (optional)
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    # Admin configuration
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL') or 'admin@example.com'
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD') or 'admin123'

class DevelopmentConfig(Config):
    DEBUG = True
    
class ProductionConfig(Config):
    DEBUG = False
    
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}