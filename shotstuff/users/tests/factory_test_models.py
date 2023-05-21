import unittest

from shotstuff import app
from shotstuff.database import db
from shotstuff.users.factories import UserFactory
from shotstuff.users.models import User
# from shotstuff import test_session

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
