from flask import Blueprint, session, redirect, render_template, url_for, request, flash
import os

blueprint = Blueprint('entrance', __name__)

@blueprint.route('/login', methods=['GET'])
def get_login():
    return render_template('loginN.html')

@blueprint.route('/login', methods=['POST'])
def post_login():
    username = request.form['username']
    password = request.form['password']
    env_username = os.getenv('GLOBAL_USER_NAME')
    env_password = os.getenv('GLOBAL_USER_PASSWORD')
    if username == env_username and password == env_password:
        flash("Boli ste uspesne prihlaseny.", category='popup')
        session['logged_in'] = True
        return redirect(url_for('drawers.drawers'))
    else:
        flash("Nespravne prihlasovacie udaje.", category='popup')
        return render_template('loginN.html')

@blueprint.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash("Boli ste uspesne odhlaseny.", category='popup')
    return redirect(url_for('entrance.get_login'))