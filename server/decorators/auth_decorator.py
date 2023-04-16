from flask import session, flash, redirect, url_for
from functools import wraps

def is_authentificate(f):
    @wraps(f)
    def decorator(self, *args, **kwargs):
        if not session.get('logged_in'):
            flash("Boli ste odhlaseny. Musite sa znova prihlasit.", category='popup')
            return redirect(url_for('entrance.get_login'))
        return f(self, *args, **kwargs)
    return decorator