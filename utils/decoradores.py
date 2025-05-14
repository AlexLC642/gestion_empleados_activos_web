from functools import wraps
from flask import session, redirect, url_for, flash

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario' not in session:
            flash("Debes iniciar sesión para acceder.", "error")
            return redirect(url_for('inicio'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if session.get('rol') != 'admin':
            flash("Acceso restringido a administradores.", "error")
            return redirect(url_for('inicio'))
        return f(*args, **kwargs)
    return wrapper
