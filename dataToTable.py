from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from flask_swagger_ui import get_swaggerui_blueprint
import time
from datetime import datetime, timedelta

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///exampleForD.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'secret_key'
db = SQLAlchemy(app)

app.secret_key = os.getenv('SECRET_KEY')
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_COOKIE_NAME'] = 'your_session_cookie_name'
app.config['PERMANENT_SESSION_LIFETIME'] = 1800 #1800 je 30 minutes in seconds

id_dictionary = {}

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGER_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name' : "Smart drawers"
    }
)
app.register_blueprint(SWAGGER_BLUEPRINT, url_prefix = SWAGGER_URL)

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    MACaddr = db.Column(db.String(80), unique=True, nullable=False)
    drawer1 = db.Column(db.Integer, nullable=False)
    drawer2 = db.Column(db.Integer, nullable=False)
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, MACaddr, drawer1, drawer2):
        self.MACaddr = MACaddr
        self.drawer1 = drawer1
        self.drawer2 = drawer2

    def update_timestamp(self):
        self.updatedAt = datetime.utcnow()

@app.route("/")
def home():
    return render_template("indexN.html")

@app.route('/login', methods=['GET'])
def get_login():
    return render_template('loginN.html')

@app.route('/login', methods=['POST'])
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
        return render_template('loginN.html')

@app.route('/drawers')
def drawers():
    if session.get('logged_in'):
        drawers = Data.query.all()
        return render_template('drawers.html', drawers=drawers)
    else:
        flash("Boli ste odhlaseny. Musite sa znova prihlasit.", category='popup')
        return redirect(url_for('get_login'))

@app.route('/details/<int:id>', methods=['GET'])
def get_details(id):
    if session.get('logged_in'):
        drawer = Data.query.get(id)
        return render_template('details.html', drawer=drawer)
    else: 
        flash("Boli ste odhlaseny. Musite sa znova prihlasit.", category='popup')
        return redirect(url_for('get_login'))

@app.route('/details/<int:id>', methods=['POST'])
def post_details(id):
    if session.get('logged_in'):
        action = request.form.get('action')
        if action == 'Update':
            drawer = Data.query.get(id)
            new_drawer1 = convert_to_number(request.form.get('drawer1'))
            new_drawer2 = convert_to_number(request.form.get('drawer2'))
            if drawer.drawer1 == new_drawer1 and drawer.drawer2 == new_drawer2:
                drawerMac = Data.query.filter_by(id=id).first().MACaddr
                flash(f"Na zasuvke s MAC adresou: |{drawerMac}|, nebolo nic updatnute!", category='popup')
                return redirect(url_for('drawers'))
            else:
                drawer.drawer1 = convert_to_number(request.form.get('drawer1'))
                drawer.drawer2 = convert_to_number(request.form.get('drawer2'))
                db.session.commit()
                drawerMac = Data.query.filter_by(id=id).first().MACaddr
                id_dictionary[drawerMac] = True # dynamicka premenna a ked ju odosleme na klienta tak sa nadstavi na False
                flash(f"Zasuvka s MAC adresou: |{drawerMac}|, bola uspesne updatnuta!", category='popup')
                time.sleep(3) # pauza pre poslanie dat, prijatie od klienta a nacitanie db z drawers asi musi byt v klientovi pri prijati aj poslanie aby toto fungovalo
                return redirect(url_for('drawers'))
        elif action == 'Vypnut celu zasuvku':
            drawer = Data.query.get(id)
            drawer.drawer1 = 0
            drawer.drawer2 = 0
            db.session.commit()
            drawerMac = Data.query.filter_by(id=id).first().MACaddr
            id_dictionary[drawerMac] = True
            flash(f"Zasuvka s MAC adresou: |{drawerMac}|, bola uplne vypnuta!", category='popup')
            time.sleep(3)  # Pause for 5 seconds
            return redirect(url_for('drawers'))
    else: 
        flash("Boli ste odhlaseny. Musite sa znova prihlasit.", category='popup')
        return redirect(url_for('get_login'))

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash("Boli ste uspesne odhlaseny.", category='popup')
    return redirect(url_for('get_login'))

def convert_to_number(word):
    if word == 'Zapnut':
        return 1
    elif word == 'Vypnut':
        return 0
    else:
        return int(word)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)


#class Contact(db.Model):       toto je class model pre DB vo flask
#    _tablename_ = 'contacts'
#    id = db.Column(db.Integer, primary_key=True)
#    first_name = db.Column(db.String(100))
#    last_name = db.Column(db.String(100))
#    phone_number = db.Column(db.String(32))

#    def __repr__(self):
#        return '<Contact {0} {1}: {2}>'.format(self.first_name,
#                                               self.last_name,
#                                               self.phone_number)