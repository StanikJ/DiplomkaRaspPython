from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

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


@app.route('/drawers')
def drawers():
    drawers = Data.query.all()
    return render_template('drawers.html', drawers=drawers)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)