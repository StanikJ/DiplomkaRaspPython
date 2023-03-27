from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///exampleForD.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'secret_key'
db = SQLAlchemy(app)

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    MACaddr = db.Column(db.String(80), unique=True, nullable=False)
    drawer1 = db.Column(db.Integer, nullable=False)
    drawer2 = db.Column(db.Integer, nullable=False)

    def __init__(self, MACaddr, drawer1, drawer2):
        self.MACaddr = MACaddr
        self.drawer1 = drawer1
        self.drawer2 = drawer2

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
    env_username = os.getenv('global_user_name')
    env_password = os.getenv('global_user_password')
    if username == env_username and password == env_password:
        flash("Boli ste uspesne prihlaseny.", category='popup')
        return redirect(url_for('drawers'))
    else:
        flash("Nespravne prihlasovacie udaje.", category='popup')
        return render_template('loginN.html')

@app.route('/drawers')
def drawers():
    drawers = Data.query.all()
    return render_template('drawers.html', drawers=drawers)

@app.route('/details/<int:id>', methods=['GET'])
def get_details(id):
    drawer = Data.query.get(id)
    return render_template('details.html', drawer=drawer)

@app.route('/details/<int:id>', methods=['POST'])
def post_details(id):
    drawer = Data.query.get(id)
    drawer.drawer1 = convert_to_number(request.form.get('drawer1'))
    drawer.drawer2 = convert_to_number(request.form.get('drawer2'))
    db.session.commit()
    drawerMac = Data.query.filter_by(id=id).first().MACaddr
    flash(f"Zasuvka s MAC adresou: |{drawerMac}|, bola uspesne updatnuta!", category='popup')
    return redirect(url_for('drawers'))

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