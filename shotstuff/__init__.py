import os
from flask import Flask, session, g
from flask_login import LoginManager

from shotstuff.config import DATABASE_URL
from shotstuff.database import connect_db
from shotstuff.root.routes import root
from shotstuff.users.routes import users
from shotstuff.users.models import User
from shotstuff.treatments.models import Treatment
from shotstuff.injection_regimens.models import InjectionRegimen
from shotstuff.injections.models import Injection
from shotstuff.labs.models import Lab
from shotstuff.body_regions.models import BodyRegion
from shotstuff.positions.models import Position
from shotstuff.medications.models import Medication
from shotstuff.generic_forms import CSRFProtection

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# @app.before_request
# def add_csrf_only_form():
#     """Add a CSRF-only form so that every route can use it"""

#     g.csrf_form = CSRFProtection()

app.register_blueprint(root)
app.register_blueprint(users, url_prefix='/users')

connect_db(app)