import os
from flask import Flask, g, session
from flask_login import LoginManager

from shotstuff.config import DATABASE_URL
from shotstuff.database import connect_db

from shotstuff.root.routes import root
from shotstuff.users.routes import users
from shotstuff.treatments.routes import treatments
from shotstuff.labs.routes import labs

from shotstuff.users.models import User
from shotstuff.body_regions.models import BodyRegion
from shotstuff.positions.models import Position
from shotstuff.medications.models import Medication

from shotstuff.generic_forms import CSRFProtection

# NOTE: should investigate why we get an error when removing seemingly unused
# classes from imports

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user_from_session(user_id):
    return User.query.get(user_id)

@login_manager.request_loader
def load_user_from_request(request):
    print("REQUEST LOADER RAN")
    breakpoint()
    user_id = session.get("_user_id")
    if user_id:
        return User.query.get(user_id)

@app.before_request
def add_csrf_only_form():
    """Add a CSRF-only form so that every route can use it"""

    g.csrf_form = CSRFProtection()

app.register_blueprint(root)
app.register_blueprint(users, url_prefix='/users')
app.register_blueprint(treatments, url_prefix='/treatments')
app.register_blueprint(labs, url_prefix='/labs')


connect_db(app)