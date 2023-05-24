import unittest
import datetime

from shotstuff import app
from shotstuff.database import db
from shotstuff.config import DATABASE_URL_TEST
from shotstuff.users.factories import UserFactory
from shotstuff.users.models import User
from shotstuff.treatments.factories import TreatmentFactory
from shotstuff.treatments.models import Treatment
from shotstuff.medication_regimens.models import MedicationRegimen
from shotstuff.injections.factories import InjectionFactory
from shotstuff.injections.models import Injection
from shotstuff.labs.models import Lab
from shotstuff.labs.factories import LabFactory
from shotstuff.body_regions.models import BodyRegion
from shotstuff.body_regions.factories import BodyRegionFactory
from shotstuff.positions.models import Position
from shotstuff.positions.factories import PositionFactory
from shotstuff.utils import calculate_date

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL_TEST
app.config["TESTING"] = True
app.config["SQLALCHEMY_ECHO"] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.drop_all()
db.create_all()

class UserModelTestCase(unittest.TestCase):
    """Tests User model."""

    def setUp(self):
        """Create test data. """

        Lab.query.delete()
        Injection.query.delete()
        Treatment.query.delete()
        MedicationRegimen.query.delete()
        Injection.query.delete()
        User.query.delete()

        u1 = UserFactory()
        t1 = TreatmentFactory()
        br1 = BodyRegionFactory()
        p1 = PositionFactory()
        i1 = InjectionFactory()
        l1 = LabFactory()

        self.u1 = u1
        self.t1 = t1
        self.br1 = br1
        self.p1 = p1
        self.i1 = i1
        self.l1 = l1

    def tearDown(self):
        # Rollback the session to clean up any fouled transactions
        db.session.rollback()

    def test_creating_users(self):
        """TODO: Not sure if keeping this"""
        u2 = UserFactory(id=2)
        self.assertEqual([self.u1, u2], db.session.query(User).all())

    def test_signup(self):
        """Test User.signup method works successfully with good data."""

        User.signup(
            first_name="signup_user_fname",
            username="signup_username",
            password="signup_password"
        )

        db.session.commit()

        self.assertEqual(
            len(User.query.filter_by(username="signup_username").all()),
            1
        )

    def test_authenticate_valid_credentials(self):
        """Test User.authenticate method works successfully with valid data."""

        auth_user = User.authenticate(
            username="test_username",
            password="password"
        )

        self.assertEqual(
            auth_user,
            User.query.filter_by(username="test_username").first()
        )

    def test_authenticate_invalid_credentials(self):
        """Test User.authenticate method works successfully with invalid data."""

        auth_user = User.authenticate(
            username="test_username",
            password="nope"
        )

        self.assertEqual(
            auth_user,
            False
        )

    def test_active_treatments(self):
        """Test active treatments property."""

        # make inactive treatment
        t2 = TreatmentFactory(
            id=2,
            currently_active=False
        )

        db.session.add(t2)
        db.session.commit()

        u1_active_treatments = (
            Treatment
            .query
            .filter_by(
                user_id=self.u1.id,
                currently_active=True
            )
            .all()
        )

        self.assertEqual(
            self.u1.active_treatments,
            u1_active_treatments
        )
        self.assertNotIn(t2, self.u1.active_treatments)

    def test_upcoming_injection_times_all_within_2_weeks(self):
        """Test upcoming injection times method works in positive case"""

        u1_upcoming_injections = self.u1.upcoming_injection_times
        inj_days = self.t1.frequency_in_seconds/86400
        inj_date = self.i1.occurred_at + datetime.timedelta(days=inj_days)

        self.assertEqual(
            u1_upcoming_injections,
            [
                {
                    "full_date": inj_date.strftime('%m/%d/%Y'),
                    "treatment": self.t1
                }
            ]
        )

    def test_upcoming_injection_times_not_all_within_2_weeks(self):
        """
        Test upcoming injection times method only shows injections coming
        up in the next 2 weeks.
        """

        # Create new treatment where injections are every 20 days, too far
        # in advance
        t2 = TreatmentFactory(
            frequency_in_seconds = 1728000,
            start_date = calculate_date(), # will set start date to now by default
            currently_active = True
        )

        i2 = InjectionFactory(
            treatment_id = t2.id,
        )

        u1_upcoming_injections = self.u1.upcoming_injection_times
        inj_days = self.t1.frequency_in_seconds/86400
        inj_date = i2.occurred_at + datetime.timedelta(days=inj_days)

        self.assertEqual(
            u1_upcoming_injections,
            [
                {
                    "full_date": inj_date.strftime('%m/%d/%Y'),
                    "treatment": self.t1
                }
            ]
        )

    def test_on_time_labs(self):
        """Test that this property returns the correct percentage. """

        # TODO shouldn't have to set the id here?????
        LabFactory(
            id=2,
            completed_on_time=False
        )

        percentage = self.u1.on_time_lab_percentage
        self.assertEqual(
            percentage,
            "50.0%"
        )
