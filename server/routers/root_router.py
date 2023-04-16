from flask import Blueprint, render_template


blueprint = Blueprint('root', __name__,
                        template_folder='views/root')

@blueprint.route("/")
def home():
    return render_template("indexN.html")