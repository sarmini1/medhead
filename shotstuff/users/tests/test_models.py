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
from shotstuff.utils import generate_friendly_date_time

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

        # InjectionFactory makes a TreatmentFactory instance, which makes
        # User and MedicationRegimen factory instances under the hood
        self.i1 = InjectionFactory()
        self.t1 = self.i1.treatment
        self.u1 = self.i1.treatment.user

        # Same note as above for LabFactory
        self.l1 = LabFactory()

    def tearDown(self):
        # Rollback the session to clean up any fouled transactions
        db.session.rollback()

    def test_creating_users(self):
        """Simple test that we can create a new user. """
        u2 = UserFactory(id=2)
        self.assertEqual([self.u1, u2], db.session.query(User).all())

    def test_signup_valid_data(self):
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

    def test_signup_invalid_data(self):
        """Test User.signup method fails with bad data. """

        with self.assertRaises(IntegrityError):
            # Create a user with no username
            User.signup(
                first_name="baduser_firstname",
                username=None,
                password="some_password"
            )
            db.session.commit()

        db.session.rollback()
        self.assertEqual(
            0,
            User.query.filter_by(first_name="baduser_firstname").count()
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
        inactive_treatment = TreatmentFactory(
            id=102,
            currently_active=False
        )

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
        self.assertNotIn(inactive_treatment, self.u1.active_treatments)

    def test_upcoming_injection_times_all_within_2_weeks(self):
        """Test upcoming injection times method works in positive case"""

        u1_upcoming_injections = self.u1.upcoming_injection_times
        inj_days = self.t1.frequency_in_seconds/86400
        inj_date = self.i1.occurred_at + datetime.timedelta(days=inj_days)

        # TODO: decide if having generate_friendly_date_time called here is the
        # right move
        self.assertEqual(
            u1_upcoming_injections,
            [
                {
                    "full_date_time": generate_friendly_date_time(inj_date),
                    "formatted_date": inj_date.strftime('%m/%d/%Y'),
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
            id=102,
            frequency_in_seconds = 1728000,
            currently_active = True
        )

        i2 = InjectionFactory(
            treatment_id = t2.id
        )

        u1_upcoming_injections = self.u1.upcoming_injection_times
        inj_days = self.t1.frequency_in_seconds/86400
        inj_date = i2.occurred_at + datetime.timedelta(days=inj_days)

        self.assertEqual(
            u1_upcoming_injections,
            [
                {
                    "full_date_time": generate_friendly_date_time(inj_date),
                    "formatted_date": inj_date.strftime('%m/%d/%Y'),
                    "treatment": self.t1
                }
            ]
        )

    def test_on_time_lab_percentage_when_labs_present(self):
        """
        Test that this property returns the correct percentage when the user has
        past labs done.
        """

        LabFactory(
            id=2,
            completed_on_time=False
        )

        percentage = self.u1.on_time_lab_percentage
        self.assertEqual(
            percentage,
            "50.0%"
        )

    def test_on_time_lab_percentage_when_no_labs_present(self):
        """
        Test that this property returns the correct percentage when the user does
        not have any past labs.
        """
        u2 = UserFactory(
            id=102
        )

        percentage = u2.on_time_lab_percentage
        self.assertEqual(
            percentage,
            None
        )
