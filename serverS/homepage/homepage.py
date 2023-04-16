from flask import Blueprint, render_template

homepage = Blueprint('homepage', __name__, static_folder='ststic', template_folder='templates')

@homepage.route('/')
def home():
    return render_template('index.html')