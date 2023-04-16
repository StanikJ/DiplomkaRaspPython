from flask import Blueprint, session, redirect, render_template, url_for, request, flash
from helpers.convert_to_number_helper import convert_to_number
from models import drawers_model
from helpers.database import db
from decorators import auth_decorator
import time

blueprint = Blueprint('details', __name__,
                        template_folder='../views/details')

@blueprint.route('/details/<int:id>', methods=['GET'])
@auth_decorator.is_authentificate
def get_details(id):
    drawer = drawers_model.query.get(id)
    return render_template('details.html', drawer=drawer)

@blueprint.route('/details/<int:id>', methods=['POST'])
@auth_decorator.is_authentificate
def post_details(id):
        drawer = drawers_model.query.get(id)
        new_drawer1 = convert_to_number(request.form.get('drawer1'))
        new_drawer2 = convert_to_number(request.form.get('drawer2'))
        if drawer.drawer1 == new_drawer1 and drawer.drawer2 == new_drawer2:
            drawerMac = drawers_model.query.filter_by(id=id).first().MACaddr
            flash(f"Na zasuvke s MAC adresou: |{drawerMac}|, nebolo nic updatnute!", category='popup')
            return redirect(url_for('drawers'))
        else:
            drawer.drawer1 = convert_to_number(request.form.get('drawer1'))
            drawer.drawer2 = convert_to_number(request.form.get('drawer2'))
            db.session.commit()
            drawerMac = drawers_model.query.filter_by(id=id).first().MACaddr
            id_dictionary[drawerMac] = True # dynamicka premenna a ked ju odosleme na klienta tak sa nadstavi na False
            flash(f"Zasuvka s MAC adresou: |{drawerMac}|, bola uspesne updatnuta!", category='popup')
            time.sleep(3) # pauza pre poslanie dat, prijatie od klienta a nacitanie db z drawers asi musi byt v klientovi pri prijati aj poslanie aby toto fungovalo
            return redirect(url_for('drawers'))

@blueprint.route('/details/<int:id>', methods=['PUT'])
@auth_decorator.is_authentificate
def put_details(id):
    drawer = drawers_model.query.get(id)
    drawer.drawer1 = 0
    drawer.drawer2 = 0
    db.session.commit()
    drawerMac = drawers_model.query.filter_by(id=id).first().MACaddr
    id_dictionary[drawerMac] = True
    flash(f"Zasuvka s MAC adresou: |{drawerMac}|, bola uplne vypnuta!", category='popup')
    time.sleep(3)  # Pause for 5 seconds
    return redirect(url_for('drawers'))