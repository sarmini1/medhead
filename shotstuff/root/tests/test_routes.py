import unittest
import datetime
from sqlalchemy.exc import IntegrityError

from shotstuff import app
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

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL_TEST
app.config["TESTING"] = True
app.config["SQLALCHEMY_ECHO"] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.drop_all()
db.create_all()


class AuthRoutesTestCase(unittest.TestCase):
    """Tests homepage, login, and signup routes."""

    # def setUp(self):
    #     """Create test data. """

    #     Lab.query.delete()
    #     Injection.query.delete()
    #     Treatment.query.delete()
    #     MedicationRegimen.query.delete()
    #     Injection.query.delete()
    #     User.query.delete()

    #     # InjectionFactory makes a TreatmentFactory instance, which makes
    #     # User and MedicationRegimen factory instances under the hood
    #     self.i1 = InjectionFactory()
    #     self.t1 = self.i1.treatment
    #     self.u1 = self.i1.treatment.user

    #     # Same note as above for LabFactory
    #     self.l1 = LabFactory()

    def tearDown(self):
        # Rollback the session to clean up any fouled transactions
        db.session.rollback()

    def test_homepage(self):
        """"""