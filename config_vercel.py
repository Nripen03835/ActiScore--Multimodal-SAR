import os
from datetime import timedelta

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Admin credentials
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL') or 'admin@example.com'
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD') or 'admin123'
    
    # File upload settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = 'uploads'
    
    # Model settings
    MODEL_DIR = 'models'
    
    # Session settings
    SESSION_TYPE = 'filesystem'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    
    # Security settings for production
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Use environment variables for sensitive data
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY environment variable must be set in production")

class VercelConfig(Config):
    """Vercel deployment configuration"""
    DEBUG = False
    # Use SQLite for Vercel deployment (file-based database)
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/app.db'
    
    # Simplified configuration for serverless deployment
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'vercel-deployment-secret-key'
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL') or 'admin@actiscore.com'
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD') or 'admin123'
    
    # Required folders for Vercel
    UPLOAD_FOLDER = '/tmp/uploads'
    MODEL_FOLDER = '/tmp/models'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'vercel': VercelConfig,
    'default': DevelopmentConfig
}