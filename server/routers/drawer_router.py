from flask import Blueprint, session, redirect, render_template, url_for, request, flash
from models import drawers_model
from decorators import auth_decorator

blueprint = Blueprint('drawers', __name__,
                        template_folder='../views/drawers')

@blueprint.route('/drawers')
@auth_decorator.is_authentificate
def drawers():
        drawers = drawers_model.query.all()
        return render_template('drawers.html', drawers=drawers)