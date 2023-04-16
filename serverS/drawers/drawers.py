from flask import Blueprint, render_template, session, redirect, url_for, flash

drawers = Blueprint('drawers', __name__, static_folder='ststic', template_folder='templates')


@drawers.route('/drawers')
def drawers():
    if session.get('logged_in'):
        drawers = Data.query.all()
        return render_template('drawers.html', drawers=drawers)
    else:
        flash("Boli ste odhlaseny. Musite sa znova prihlasit.", category='popup')
        return redirect(url_for('get_login'))