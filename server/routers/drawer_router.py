from flask import Blueprint, session, redirect, render_template, url_for, request, flash
from models.drawers_model import DrawersModel
from decorators import auth_decorator

blueprint = Blueprint('drawers', __name__)

@blueprint.route('/drawers')
@auth_decorator.is_authentificate
def drawers():
        drawers = DrawersModel.query.all()
        return render_template('drawers.html', drawers=drawers)