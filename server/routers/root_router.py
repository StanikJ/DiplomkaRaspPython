from flask import Blueprint, render_template


blueprint = Blueprint('root', __name__)

@blueprint.route("/")
def home():
    return render_template("indexN.html")