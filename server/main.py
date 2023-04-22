from flask import Flask
from dotenv import load_dotenv
import os
from flask_swagger_ui import get_swaggerui_blueprint
from helpers.database import db
from services.bluetooth_server_service.Config import Config
from helpers.bluetooth_helper import start_bluetooth_service

from routers.entrance_router import blueprint as entrance_router
from routers.root_router import blueprint as root_router
from routers.drawer_detail_router import blueprint as drawer_detail_router
from routers.drawer_router import blueprint as drawer_router

load_dotenv()
config = Config

app = Flask(__name__, static_url_path='/public', static_folder='public', template_folder='views')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///exampleForD.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'secret_key'
db.init_app(app)

app.secret_key = os.getenv('SECRET_KEY')
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_COOKIE_NAME'] = 'your_session_cookie_name'
app.config['PERMANENT_SESSION_LIFETIME'] = 1800 #1800 je 30 minutes in seconds

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

app.register_blueprint(entrance_router)
app.register_blueprint(root_router)
app.register_blueprint(drawer_detail_router)
app.register_blueprint(drawer_router)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    start_bluetooth_service(config)

#https://github.com/deveshkharve/flask-middleware