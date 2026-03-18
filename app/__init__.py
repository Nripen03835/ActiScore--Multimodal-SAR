from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_caching import Cache
from config import Config
import os

db = SQLAlchemy()
migrate = Migrate()
cache = Cache()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Configure app for large file uploads
    app.config['MAX_CONTENT_LENGTH'] = 2000 * 1024 * 1024  # 2000MB
    app.config['WTF_CSRF_TIME_LIMIT'] = None  # No time limit for large uploads
    
    # Set request timeout for large uploads
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    
    # Ensure upload directory exists with proper permissions
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['MODEL_FOLDER'], exist_ok=True)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    cache.init_app(app)
    
    # Inject current_user deeply into templates natively bypassing Flask-Login
    from app.auth.utils import current_user
    @app.context_processor
    def inject_user():
        return dict(current_user=current_user)
    
    # Register error handlers
    from app.main import routes as main_routes
    app.register_error_handler(404, main_routes.not_found_error)
    app.register_error_handler(500, main_routes.internal_error)
    
    # Global Authentication Lock (User asked only at starting!)
    @app.before_request
    def global_login_check():
        from flask import request, redirect, url_for, session
        allowed_endpoints = ['auth.login', 'auth.register', 'static', 'main.index']
        # Allow OPTIONS requests to pass through (CORS)
        if request.method == 'OPTIONS':
            return
        if request.endpoint and request.endpoint not in allowed_endpoints:
            if not session.get('user_info'):
                return redirect(url_for('auth.login'))
    
    # Register blueprints
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    from app.actiscore import bp as actiscore_bp
    app.register_blueprint(actiscore_bp, url_prefix='/actiscore')
    
    from app.intellilearn import bp as intellilearn_bp
    app.register_blueprint(intellilearn_bp, url_prefix='/ai')
    
    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    # Create upload directories
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['MODEL_FOLDER'], exist_ok=True)
    
    return app

from app import models