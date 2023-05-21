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

    def setUp(self):
        # Prepare a new, clean session
        # self.session = test_session.Session()
        self.u1 = UserFactory()

    def tearDown(self):
        # Rollback the session => no changes to the database
        db.session.rollback()
        # Remove it, so that the next test gets a new Session()
        # test_session.Session.remove()

    def test_creating_users(self):
        """TODO: Not sure if keeping this"""
        u2 = UserFactory(id=2)
        self.assertEqual([self.u1, u2], db.session.query(User).all())
