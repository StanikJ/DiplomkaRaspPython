from flask import Blueprint, render_template, redirect, request, flash, session, url_for
import os

login = Blueprint("login", __name__, static_folder="ststic", template_folder="templates")

@login.route('/login', methods=['GET'])
def get_login():
    return render_template('login.html')

@login.route('/login', methods=['POST'])
def post_login():
    username = request.form['username']
    password = request.form['password']
    env_username = os.getenv('GLOBAL_USER_NAME')
    env_password = os.getenv('GLOBAL_USER_PASSWORD')
    if username == env_username and password == env_password:
        flash("Boli ste uspesne prihlaseny.", category='popup')
        session['logged_in'] = True
        return redirect(url_for('drawers'))
    else:
        flash("Nespravne prihlasovacie udaje.", category='popup')
        return render_template('login.html')