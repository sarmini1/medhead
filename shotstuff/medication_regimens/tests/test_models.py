import unittest

from shotstuff import app
from shotstuff.database import db
from shotstuff.config import DATABASE_URL_TEST
from shotstuff.medication_regimens.factories import MedicationRegimenFactory
from shotstuff.medication_regimens.models import MedicationRegimen

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL_TEST
app.config["TESTING"] = True
app.config["SQLALCHEMY_ECHO"] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.drop_all()
db.create_all()


class MedicationRegimenModelTestCase(unittest.TestCase):

    def setUp(self):
        # Prepare a new, clean session
        # self.session = test_session.Session()
        self.mr1 = MedicationRegimenFactory()

    def tearDown(self):
        # Rollback the session => no changes to the database
        db.session.rollback()
        # Remove it, so that the next test gets a new Session()
        # test_session.Session.remove()

    def test_creating_med_regimens(self):
        """TODO: Not sure if keeping this"""
        mr2 = MedicationRegimenFactory(id=2, title='med title')
        self.assertEqual(
            [self.mr1, mr2],
            db.session.query(MedicationRegimen).all()
        )
