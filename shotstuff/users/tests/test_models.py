from shotstuff import app
from shotstuff.database import db
from shotstuff.config import DATABASE_URL_TEST
from shotstuff.testing_seed import BaseModelTestCase
from shotstuff.users.models import User
from shotstuff.treatments.models import Treatment

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

        self.assertEqual(
            self.u1.active_treatments,
            Treatment.query.filter_by(
                user_id=self.u1.id,
                currently_active=True
            ).all()
        )
        self.assertNotIn(self.t2, self.u1.active_treatments)