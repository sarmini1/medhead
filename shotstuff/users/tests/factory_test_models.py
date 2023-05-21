import unittest

from shotstuff import app
from shotstuff.database import db
from shotstuff.config import DATABASE_URL_TEST
from shotstuff.users.factories import UserFactory
from shotstuff.users.models import User

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL_TEST
app.config["TESTING"] = True
app.config["SQLALCHEMY_ECHO"] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.drop_all()
db.create_all()

class UserModelTestCase(unittest.TestCase):
    """Tests User model."""

    @classmethod
    def setUp(cls):
        User.query.delete()
        u1 = UserFactory()
        cls.u1 = u1

    def tearDown(self):
        # Rollback the session => no changes to the database
        db.session.rollback()
        # Remove it, so that the next test gets a new Session()

    def test_creating_users(self):
        """TODO: Not sure if keeping this"""
        u2 = UserFactory(id=2)
        self.assertEqual([self.u1, u2], db.session.query(User).all())

    def test_signup(self):
        """Test User.signup method works successfully with good data."""

        User.signup(
            first_name="signup_user_fname",
            username="signup_username",
            password="signup_password"
        )

        db.session.commit()

        self.assertEqual(
            len(User.query.filter_by(username="signup_username").all()),
            1
        )

    def test_authenticate_valid_credentials(self):
        """Test User.authenticate method works successfully with valid data."""

        auth_user = User.authenticate(
            username="test_username",
            password="password"
        )

        self.assertEqual(
            auth_user,
            User.query.filter_by(username="test_user1").first()
        )