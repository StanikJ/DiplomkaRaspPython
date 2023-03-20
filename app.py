from flask import Flask, redirect, url_for, render_template, request, session, escape, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

# dynamicky html table s jinja 2: https://stackoverflow.com/questions/52019676/dynamic-table-with-python
# quering the database: https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/queries/

app = Flask(__name__)

app.secret_key = "thisismysecretkey"
app.permanent_session_lifetime = timedelta(seconds=30)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class users(db.Model):      #doplnit heslo
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email

class raspberry_data(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    raspberry_mac_address = db.Column(db.String(100))
    drawer1 = db.Column(db.String(100))
    drawer2 = db.Column(db.String(100))
    drawer3 = db.Column(db.String(100))
    drawer4 = db.Column(db.String(100))
    drawer5 = db.Column(db.String(100))
    drawer6 = db.Column(db.String(100))

    def __init__(self, raspberry_mac_address, drawer1, drawer2, drawer3, drawer4, drawer5, drawer6):
        self.raspberry_mac_address = raspberry_mac_address
        self.drawer1 = drawer1
        self.drawer2 = drawer2
        self.drawer3 = drawer3
        self.drawer4 = drawer4
        self.drawer5 = drawer5
        self.drawer6 = drawer6

@app.route("/")
def home():
    return render_template("indexN.html")

@app.route("/log")
def log():
    return render_template("loginN.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        session["user"] = user

        found_user = users.query.filter_by(name=user).first()
        #vymazanie a aj update co bude treba na diplomku po kazdom musi byt db.session.commit()
        # -found_user = users.query.filter_by(name=user).delete()
        # -for user in found_user:
        # user.delete()
        # admin = User.query.filter_by(username='admin').first()
        # admin.email = 'my_new_email@example.com'
        # db.session.commit()


        if found_user:
            session["email"] = found_user.email
        else:
            usr = users(user, "")
            db.session.add(usr)
            db.session.commit()


        flash("Prihlasenie bolo uspesne!")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("Uz si prihlaseny.")
            return redirect(url_for("user"))

        return render_template("login.html")

@app.route("/view")
def view():
    #update_user = users.query.filter_by(email="fezoj@gmail.com").first()
    #update_user.email = "fezojovnovy@gmail.com"
    #db.session.commit()
    return render_template("view.html", values=users.query.all())

@app.route("/user", methods=["POST", "GET"])
def user():
    email = None
    if "user" in session:
        user = session["user"]

        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            found_user = users.query.filter_by(name=user).first()
            found_user.email = email
            db.session.commit()
            flash("Email bol ulozeny.")
        else:
            if "email" in session:
                email = session["email"]
        return render_template("user.html", email=email)
    else:
        flash("Nie si prihlaseny!")
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    flash("Bol si odhlaseny!", "info")
    session.pop("user,", None)
    session.pop("email", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)