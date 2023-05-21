import unittest

from shotstuff import app
from shotstuff.database import db
from shotstuff.config import DATABASE_URL_TEST
from shotstuff.treatments.factories import TreatmentFactory
from shotstuff.medication_regimens.factories import MedicationRegimenFactory
from shotstuff.treatments.models import Treatment

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL_TEST
app.config["TESTING"] = True
app.config["SQLALCHEMY_ECHO"] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.drop_all()
db.create_all()

class TreatmentModelTestCase(unittest.TestCase):

    def setUp(self):
        self.t1 = TreatmentFactory()

    def tearDown(self):
        # Rollback the session => no changes to the database
        db.session.rollback()

    def test_creating_treatments(self):
        """TODO: Not sure if keeping this"""
        t2 = TreatmentFactory(
            id=2,
            medication_regimen=MedicationRegimenFactory(id=2)
        )
        self.assertEqual(
            [self.t1, t2],
            db.session.query(Treatment).all()
        )
