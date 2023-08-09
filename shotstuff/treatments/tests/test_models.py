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

    def test_find_next_inj_position(self):
        """
        For an active treatment with past injections, test that we can find the
        next correct injection position.
        """

        # Making a new injection will make a new Treatment instance for us or
        # be associated with the default TreatmentFactory instance, if it already
        # exists
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
            id=102,
            next_lab_due_date=datetime.datetime.now()
        )

        t2.update_next_lab_due_date()
        self.assertEqual(
            t2.next_lab_due_date,
            "2023-09-26"
        )

    @freeze_time("2023-05-26 10:30:01")
    def test_next_injection_detail_with_past_injections(self):
        """
        Test method for calculating next injection detail when past injections
        have occurred.
        """

        i2 = InjectionFactory(
            occurred_at=datetime.datetime.now()
        )
        # Injection factory makes a Treatment instance with inj frequency
        # every 7 days, so next injection time is predictable

        # TODO: decide if manually converting this to PST to account for time
        # zone stuff is the right call
        next_injection_detail = {
            "time_due": {
                "year": "2023",
                "month": "06",
                "day": "02",
                "time": "03:30:01",
                "date": "06/02/2023",
                "weekday": "Friday",
                "full_date_time": "06/02/2023, 03:30:01"
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

        with self.assertRaises(AttributeError):
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
                "date": "05/26/2023",
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

    @freeze_time("2023-05-26 10:30:01")
    def test_friendly_start_date_when_start_date_present(self):
        """Test that the friendly_start_date property works with a valid date."""

        t2 = TreatmentFactory(
            id=102,
            start_date=datetime.datetime.now()
        )

        friendly_start_date = t2.friendly_start_date
        expectation = {
                "year": "2023",
                "month": "05",
                "day": "26",
                "time": "10:30:01",
                "date": "05/26/2023",
                "weekday": "Friday",
                "full_date_time": "05/26/2023, 10:30:01"
            }
        self.assertEqual(
            friendly_start_date,
            expectation
        )

    def test_friendly_start_date_when_start_date_null(self):
        """
        Test that the friendly_start_date property returns None when
        accessed for an instance with an unknown start date. """

        t2 = TreatmentFactory(
            id=102,
            start_date=None
        )

        friendly_start_date = t2.friendly_start_date
        self.assertEqual(
            friendly_start_date,
            None
        )

    @freeze_time("2023-05-26 10:30:01")
    def test_friendly_next_lab_date_when_next_lab_date_present(self):
        """Test that the friendly_next_lab_date property works with a valid date."""

        t2 = TreatmentFactory(
            id=102,
            next_lab_due_date=datetime.datetime.now()
        )

        friendly_start_date = t2.friendly_next_lab_due_date
        expectation = {
                "year": "2023",
                "month": "05",
                "day": "26",
                "time": "10:30:01",
                "date": "05/26/2023",
                "weekday": "Friday",
                "full_date_time": "05/26/2023, 10:30:01"
            }
        self.assertEqual(
            friendly_start_date,
            expectation
        )

    def test_friendly_next_lab_date_when_next_lab_date_null(self):
        """
        Test that the friendly_next_lab_due_date property returns None when
        accessed for an instance with an unknown next lab date. """

        t2 = TreatmentFactory(
            id=102,
        )

        friendly_start_date = t2.friendly_next_lab_due_date
        self.assertEqual(
            friendly_start_date,
            None
        )

    def test_num_injections_property_when_past_injections_present(self):
        """Tests num_injections property for a user when they have past injections."""

        InjectionFactory()
        self.assertEqual(
            self.t1.user.num_injections,
            1
        )

    def test_num_injections_property_when_past_injections_not_present(self):
        """Tests num_injections property for a user when they do not have past injections."""

        self.assertEqual(
            self.t1.user.num_injections,
            0
        )