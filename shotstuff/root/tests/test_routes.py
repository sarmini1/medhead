import unittest
from flask_login import FlaskLoginClient, login_user, LoginManager

from shotstuff import app, login_manager
from shotstuff.database import db
from shotstuff.config import DATABASE_URL_TEST

from shotstuff.users.factories import UserFactory
from shotstuff.treatments.factories import TreatmentFactory
from shotstuff.injections.factories import InjectionFactory
from shotstuff.labs.factories import LabFactory

from shotstuff.users.models import User
from shotstuff.treatments.models import Treatment
from shotstuff.medication_regimens.models import MedicationRegimen
from shotstuff.injections.models import Injection
from shotstuff.labs.models import Lab

app.test_client_class = FlaskLoginClient
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL_TEST
app.config["TESTING"] = True
app.config["SQLALCHEMY_ECHO"] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['WTF_CSRF_ENABLED'] = False

# login_manager = LoginManager()
# login_manager.init_app(app)

# @login_manager.user_loader
# def load_user(user_id):
#     breakpoint()
#     return User.query.get(user_id)

db.drop_all()
db.create_all()


class AnonRoutesTestCase(unittest.TestCase):
    """Tests homepage, login, and signup routes."""

    def setUp(self):
        """Create test data. """

        self.u1 = UserFactory()

    def tearDown(self):
        # Rollback the session to clean up any fouled transactions
        db.session.rollback()

    def test_homepage(self):
        """Tests rendering homepage when not logged in. """

        with app.test_client() as client:

            resp = client.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Login", html)
            self.assertIn("Signup", html)

    def test_login(self):
        """Tests that rendering the login page works."""

        with app.test_client() as client:

            resp = client.get("/login")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Login", html)
            # Add another assertion here that really proves it's the login form

# FIXME: figure out why i can't have two test functions in the same class that
# make unauthenticated requests

    # def test_signup(self):
    #     """Tests that rendering the signup page works."""

    #     with app.test_client() as client:

    #         resp = client.get("/signup")
    #         html = resp.get_data(as_text=True)

    #         self.assertEqual(resp.status_code, 200)
    #         self.assertIn("Signup", html)
            # Add another assertion here that really proves it's the login form

    # TODO put the rest of the non-authenticated routes in this class


    # def test_homepage_as_auth_user(self):
    #     """Tests that an authenticated user gets redirected to dashboard. """
    #     # with app.test_request_context():

    #     user = User.query.get(self.u1.id)
    #     self.client = app.test_client(user=user)
    #     # user.is_authenticated = True
    #     with self.client as client:
    #         # login_user(user)
    #         breakpoint()
    #         # resp = client.get("/", follow_redirects=True)
    #         resp = client.get("/users/dashboard", follow_redirects=True)
    #         html = resp.get_data(as_text=True)
    #         breakpoint()

    #         self.assertEqual(resp.status_code, 200)
    #         self.assertIn("Dashboard", html)
    #         # self.assertIn("Signup", html)
