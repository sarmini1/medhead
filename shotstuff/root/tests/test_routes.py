import unittest
from flask_login import FlaskLoginClient

from shotstuff import app
from shotstuff.database import db
from shotstuff.config import DATABASE_URL_TEST

from shotstuff.users.factories import UserFactory

app.test_client_class = FlaskLoginClient
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL_TEST
app.config["TESTING"] = True
app.config["SQLALCHEMY_ECHO"] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['WTF_CSRF_ENABLED'] = False


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
