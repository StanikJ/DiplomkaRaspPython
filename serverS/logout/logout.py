from flask import Blueprint, session, redirect, url_for, flash

logout = Blueprint('logout', __name__, static_folder='ststic', template_folder='templates')

@logout.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash("Boli ste uspesne odhlaseny.", category='popup')
    return redirect(url_for('get_login'))