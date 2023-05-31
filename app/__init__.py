from flask import Flask
from config import Config
from flask_login import LoginManager
from .models import db, User
from flask_migrate import Migrate
from .auth.auth_routes import auth


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
login_manager.login_view = 'auth.login_page'

app.register_blueprint(auth)

from . import routes
from . import models

