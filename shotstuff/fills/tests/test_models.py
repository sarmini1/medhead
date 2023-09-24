from freezegun import freeze_time
import unittest
import datetime

from shotstuff import app
from shotstuff.database import db
from shotstuff.config import DATABASE_URL_TEST

from shotstuff.fills.factories import FillFactory

from shotstuff.users.models import User
from shotstuff.treatments.models import Treatment
from shotstuff.medication_regimens.models import MedicationRegimen
from shotstuff.injections.models import Injection
from shotstuff.fills.models import Fill

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL_TEST
app.config["TESTING"] = True
app.config["SQLALCHEMY_ECHO"] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.drop_all()
db.create_all()


class FillModelTestCase(unittest.TestCase):
    """Tests Fill model."""

    def setUp(self):
        """Create test data. """

        Fill.query.delete()
        Treatment.query.delete()
        MedicationRegimen.query.delete()
        User.query.delete()

        self.f1 = FillFactory()

    def tearDown(self):
        # Rollback the session to clean up any fouled transactions
        db.session.rollback()

    @freeze_time("2023-05-26 10:30:01")
    def test_friendly_occurred_at(self):
        """Test that the friendly_occurred_at property works with a valid date/time."""

        f1 = FillFactory(
            id=1002,
            occurred_at=datetime.datetime.utcnow()
        )

        friendly_occurred_at = f1.friendly_occurred_at
        expectation = {
            "year": "2023",
            "month": "05",
            "day": "26",
            "time": "03:30:01",
            "date": "05/26/2023",
            "weekday": "Friday",
            "full_date_time": "05/26/2023, 03:30:01"
        }
        self.assertEqual(
            friendly_occurred_at,
            expectation
        )
