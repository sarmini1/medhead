import unittest

from shotstuff import app
from shotstuff.database import db
from shotstuff.config import DATABASE_URL_TEST
from shotstuff.body_regions.factories import BodyRegionFactory
from shotstuff.body_regions.models import BodyRegion

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL_TEST
app.config["TESTING"] = True
app.config["SQLALCHEMY_ECHO"] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.drop_all()
db.create_all()

class BodyRegionModelTestCase(unittest.TestCase):

    def setUp(self):
        self.b1 = BodyRegionFactory()

    def tearDown(self):
        # Rollback the session => no changes to the database
        db.session.rollback()

    def test_creating_treatments(self):
        """Simple test to create a new BodyRegion instance."""

        b2 = BodyRegionFactory()

        self.assertEqual(
            [self.b1, b2],
            db.session.query(BodyRegion).all()
        )
