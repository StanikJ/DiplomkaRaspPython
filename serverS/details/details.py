from flask import Blueprint, render_template, session, redirect, url_for, flash, request

from helpers.convert_to_number import convert_to_number

details = Blueprint('details', __name__, static_folder='ststic', template_folder='templates')

@details.route('/details/<int:id>', methods=['GET'])
def get_details(id):
    if session.get('logged_in'):
        drawer = Data.query.get(id)
        return render_template('details.html', drawer=drawer)
    else: 
        flash("Boli ste odhlaseny. Musite sa znova prihlasit.", category='popup')
        return redirect(url_for('get_login'))

@details.route('/details/<int:id>', methods=['POST'])
def post_details(id):
    if session.get('logged_in'):
        action = request.form.get('action')
        if action == 'Update':
            drawer = Data.query.get(id)
            drawer.drawer1 = convert_to_number(request.form.get('drawer1'))
            drawer.drawer2 = convert_to_number(request.form.get('drawer2'))
            db.session.commit()
            drawerMac = Data.query.filter_by(id=id).first().MACaddr
            flash(f"Zasuvka s MAC adresou: |{drawerMac}|, bola uspesne updatnuta!", category='popup')
            return redirect(url_for('drawers'))
        elif action == 'Vypnut celu zasuvku':
            drawer = Data.query.get(id)
            drawer.drawer1 = 0
            drawer.drawer2 = 0
            db.session.commit()
            drawerMac = Data.query.filter_by(id=id).first().MACaddr
            flash(f"Zasuvka s MAC adresou: |{drawerMac}|, bola uplne vypnuta!", category='popup')
            return redirect(url_for('drawers'))
    else: 
        flash("Boli ste odhlaseny. Musite sa znova prihlasit.", category='popup')
        return redirect(url_for('get_login'))