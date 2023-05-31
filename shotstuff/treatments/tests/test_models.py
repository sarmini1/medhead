from freezegun import freeze_time
import unittest
import datetime

from shotstuff import app
from shotstuff.database import db
from shotstuff.config import DATABASE_URL_TEST
from shotstuff.treatments.factories import TreatmentFactory
from shotstuff.medication_regimens.factories import MedicationRegimenFactory
from shotstuff.injections.factories import InjectionFactory

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
        # self.i1 = InjectionFactory()

    def tearDown(self):
        # Rollback the session => no changes to the database
        db.session.rollback()

    def test_creating_treatments(self):
        """Test creating a new instance is successful."""
        t2 = TreatmentFactory(
            id=2,
            medication_regimen=MedicationRegimenFactory(id=2)
        )
        self.assertEqual(
            [self.t1, t2],
            db.session.query(Treatment).all()
        )

    @freeze_time("2023-05-26 10:30:01")
    def test_generate_friendly_date_time(self):
        """Test that a treatment instance can give back helpful time data."""

        t2 = TreatmentFactory()
        generated = t2.generate_friendly_date_time(datetime.datetime.now())

        self.assertEqual(
            generated,
            {
                'year': '2023',
                'month': '05',
                'day': '26',
                'time': '10:30:01',
                'weekday': 'Friday',
                'full_date_time': '05/26/2023, 10:30:01'
            }
        )

    def test_find_next_inj_position(self):
        """
        For an active treatment with past injections, test that we can find the
        next correct injection position.
        """

        # Making a new injection will make a new Treatment instance for us
        i2 = InjectionFactory()
        next_inj_position = i2.treatment._find_next_injection_position()
        self.assertEqual(
            next_inj_position,
            ("left", "lower")
        )

    @freeze_time("2023-05-26 10:30:01")
    def test_update_next_lab_due_date(self):
        """Test method for updating next lab due date. """

        t2 = TreatmentFactory(
            next_lab_due_date=datetime.datetime.now()
        )
        t2.update_next_lab_due_date()
        self.assertEqual(
            t2.next_lab_due_date,
            "2023-09-30"
        )

    @freeze_time("2023-05-26 10:30:01")
    def test_next_injection_detail_with_past_injections(self):
        """
        Test method for calculating next injection detail when past injections
        have occurred.
        """

        # Making a new injection will make a new Treatment instance for us
        i2 = InjectionFactory(
            occurred_at=datetime.datetime.now()
        )
        # Injection factory makes a Treatment instance with inj frequency
        # every 7 days, so next injection time is predictable
        next_injection_detail = {
            "time_due": {
                "year": "2023",
                "month": "06",
                "day": "02",
                "time": "10:30:01",
                "weekday": "Friday",
                "full_date_time": "06/02/2023, 10:30:01"
            },
            "position": ("left", "lower")
        }
        self.assertEqual(
            next_injection_detail,
            i2.treatment.calculate_next_injection_detail()
        )

    def test_next_injection_detail_no_injections(self):
        """Test that an error is thrown when trying to access this property
        on a treatment without any injections."""

        with self.assertRaises(ValueError):
            self.t1.calculate_next_injection_detail()

    @freeze_time("2023-05-26 10:30:01")
    def test_last_injection_detail_with_past_injections(self):
        """
        Test accessing the last injection details for a treatment with past
        injections.
        """
        i2 = InjectionFactory(
            occurred_at=datetime.datetime.now()
        )
        last_injection_details = {
            "injection": i2,
            "occurred_at": {
                "year": "2023",
                "month": "05",
                "day": "26",
                "time": "10:30:01",
                "weekday": "Friday",
                "full_date_time": "05/26/2023, 10:30:01"
            }
        }
        self.assertEqual(
            i2.treatment.last_injection_details,
            last_injection_details
        )

    def test_last_injection_detail_no_past_injections(self):
        """Test getting last injection details when no injections have occurred."""

        # Our treatment from the setup doesn't have any injections yet
        self.assertEqual(
            None,
            self.t1.last_injection_details
        )