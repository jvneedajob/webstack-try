from flask import app
from flask_login import LoginManager

login_manager = LoginManager()

login_manager = LoginManager(app)