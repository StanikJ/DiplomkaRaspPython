from flask import Blueprint, render_template, session, redirect, url_for


blueprint = Blueprint('root', __name__)

@blueprint.route("/")
def home():
    if session['logged_in'] is True:
        return redirect(url_for('drawers.drawers'))
    return render_template("indexN.html")