from freezegun import freeze_time
import unittest
import datetime

from shotstuff import app
from shotstuff.database import db
from shotstuff.config import DATABASE_URL_TEST

from shotstuff.injections.factories import InjectionFactory

from shotstuff.users.models import User
from shotstuff.treatments.models import Treatment
from shotstuff.medication_regimens.models import MedicationRegimen
from shotstuff.injections.models import Injection

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL_TEST
app.config["TESTING"] = True
app.config["SQLALCHEMY_ECHO"] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.drop_all()
db.create_all()


class InjectionModelTestCase(unittest.TestCase):
    """Tests Injection model."""

    def setUp(self):
        """Create test data. """

        Injection.query.delete()
        Treatment.query.delete()
        MedicationRegimen.query.delete()
        Injection.query.delete()
        User.query.delete()

        self.i1 = InjectionFactory()

    def tearDown(self):
        # Rollback the session to clean up any fouled transactions
        db.session.rollback()

    def test_create(self):
        """Simple test checking that we can create a new Injection instance."""

        i2 = InjectionFactory()
        self.assertEqual(
            [self.i1, i2],
            Injection.query.all()
        )

    @freeze_time("2023-05-26 10:30:01")
    def test_friendly_injection_time(self):
        """Test that an injection instance can hand back nice time data."""

        i2 = InjectionFactory(occurred_at = datetime.datetime.now())
        generated = i2.friendly_injection_time

        self.assertEqual(
            generated,
            {
                'year': '2023',
                'month': '05',
                'day': '26',
                'time': '10:30:01',
                "date": '05/26/2023',
                "weekday": 'Friday',
                'full_date_time': '05/26/2023, 10:30:01'
            }
        )