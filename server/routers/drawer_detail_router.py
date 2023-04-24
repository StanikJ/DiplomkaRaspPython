from flask import Blueprint, session, redirect, render_template, url_for, request, flash
from helpers.convert_to_number_helper import convert_to_number
from helpers.checkbox_helper import checkbox_to_db_value
from models.drawers_model import DrawersModel
from helpers.database import db
from decorators import auth_decorator
#from helpers.bluetooth_helper import bluetooth_service_helper
import time

blueprint = Blueprint('details', __name__)

@blueprint.route('/details/<int:id>', methods=['GET'])
@auth_decorator.is_authentificate
def get_details(id):
    drawer = DrawersModel.query.get(id)
    return render_template('details.html', drawer=drawer)

@blueprint.route('/details/<int:id>', methods=['POST'])
@auth_decorator.is_authentificate
def post_details(id):
        drawer = DrawersModel.query.get(id)
        new_drawer1 = checkbox_to_db_value(request.form.get('drawer1'))
        new_drawer2 = checkbox_to_db_value(request.form.get('drawer2'))
        if drawer.drawer1 == new_drawer1 and drawer.drawer2 == new_drawer2:
            flash(f"Na zasuvke s MAC adresou: |{drawer.MACaddr}|, nebolo nic updatnute!", category='popup')
            return redirect(url_for('drawers.drawers'))
        else:
            drawer.drawer1 = checkbox_to_db_value(request.form.get('drawer1'))
            drawer.drawer2 = checkbox_to_db_value(request.form.get('drawer2'))
            #bluetooth_service_helper.send_data_to_client([drawer.drawer1, drawer.drawer2], drawer.Macaddr)
            db.session.commit()
            flash(f"Zasuvka s MAC adresou: |{drawer.MACaddr}|, bola uspesne updatnuta!", category='popup')
            return redirect(url_for('drawers.drawers'))

@blueprint.route('/details/<int:id>/all', methods=['POST'])
@auth_decorator.is_authentificate
def put_details(id):
    drawer = DrawersModel.query.get(id)
    drawer.drawer1 = 0
    drawer.drawer2 = 0
    db.session.commit()
    #bluetooth_service_helper.send_data_to_client([drawer.drawer1, drawer.drawer2], drawer.Macaddr)
    flash(f"Zasuvka s MAC adresou: |{drawer.MACaddr}|, bola uplne vypnuta!", category='popup')
    return redirect(url_for('drawers.drawers'))