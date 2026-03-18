from flask import session, redirect, url_for, request
from functools import wraps
from werkzeug.local import LocalProxy

def get_current_user():
    """Proxy function to securely rebuild and provide the user object from the session cookie."""
    from app.models import User
    from app import db
    
    info = session.get('user_info')
    if not info:
        return None
        
    user = User.query.get(info['id'])
    
    # Vercel Ephemeral Storage Hook: Rebuild disappeared users silently!
    if not user:
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
        except:
            db.session.rollback()
            
    return user

# The drop-in replacement for `current_user`
current_user = LocalProxy(get_current_user)

def login_required(f):
    """The drop-in replacement for `@login_required`"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_info'):
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def login_user(user, remember=False):
    """The drop-in replacement for `login_user()`"""
    session['user_info'] = {
        'id': user.id,
        'email': user.email,
        'name': user.name,
        'role': user.role
    }
    session.permanent = True

def logout_user():
    """The drop-in replacement for `logout_user()`"""
    session.pop('user_info', None)
