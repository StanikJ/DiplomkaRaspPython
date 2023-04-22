from flask import Blueprint, session, redirect, render_template, url_for, request, flash
from models.drawers_model import DrawersModel
from decorators import auth_decorator
from helpers.database import db

blueprint = Blueprint('drawers', __name__)

@blueprint.route('/drawers')
@auth_decorator.is_authentificate
def drawers():
        # mac = DrawersModel("Cav Johnny", 0, 1)
        # db.session.add(mac)
        # db.session.commit()
        #drawers = DrawersModel.function_to_check_if_clients_work()
        drawers = DrawersModel.query.all()
        return render_template('drawers.html', drawers=drawers)