import datetime

from shotstuff import app
from shotstuff.database import db
from shotstuff.config import DATABASE_URL_TEST
from shotstuff.testing_seed import BaseModelTestCase
from shotstuff.users.models import User
from shotstuff.treatments.models import Treatment
from shotstuff.injections.models import Injection
from shotstuff.utils import calculate_date

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL_TEST
app.config["TESTING"] = True
app.config["SQLALCHEMY_ECHO"] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.drop_all()
db.create_all()

class UserModelTestCase(BaseModelTestCase):

    def test_setup(self):
        """Test to make sure tests are set up correctly"""
        test_setup_correct = True
        self.assertEqual(test_setup_correct, True)

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
            username="test_user1",
            password="password"
        )

        self.assertEqual(
            auth_user,
            User.query.filter_by(username="test_user1").first()
        )

    def test_authenticate_invalid_credentials(self):
        """Test User.authenticate method works successfully with invalid data."""

        auth_user = User.authenticate(
            username="test_user1",
            password="nope"
        )

        self.assertEqual(
            auth_user,
            False
        )

    def test_active_treatments(self):
        """Test active treatments property."""

        # make inactive treatment
        self.t2 = Treatment(
            user_id = self.u1.id,
            medication_regimen_id = self.mr2.id,
            frequency_in_seconds = 864000,
            requires_labs = True,
            lab_frequency_in_months = 3,
            lab_point_in_cycle = "peak",
            next_lab_due_date = "2022-06-16",
            clinic_supervising = "UCSF",
            start_date = "2022-02-16",
            currently_active = False
        )

        db.session.add(self.t2)
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
        self.assertNotIn(self.t2, self.u1.active_treatments)

    def test_upcoming_injection_times_all_soon(self):
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

    def test_upcoming_injection_times_not_all_soon(self):
        """
        Test upcoming injection times method only shows injections coming
        up in the next 2 weeks.
        """

        # Create new treatment where injections are every 20 days, too far
        # in advance
        self.t2 = Treatment(
            user_id = self.u1.id,
            medication_regimen_id = self.mr2.id,
            frequency_in_seconds = 1728000,
            requires_labs = True,
            lab_frequency_in_months = 6,
            lab_point_in_cycle = "peak",
            next_lab_due_date = calculate_date(months_in_future=6),
            clinic_supervising = "UCSF",
            start_date = calculate_date(),
            currently_active = False
        )

        db.session.add(self.t2)
        db.session.commit()

        self.i2 = Injection(
            treatment_id = self.t2.id,
            method = "subcutaneous",
            body_region_id = self.br1.id,
            position_id = self.p1.id
        )

        db.session.add(self.i2)
        db.session.commit()

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