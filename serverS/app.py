from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

from homepage.homepage import homepage
from login.login import login
from drawers.drawers import drawers
from details.details import details

app = Flask(__name__)
db = SQLAlchemy(app)


app.register_blueprint(homepage)
app.register_blueprint(login)
app.register_blueprint(drawers)
app.register_blueprint(details)

if __name__ == "__main__":
    app.run(debug=True)