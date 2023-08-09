"""Models for injection tracker app."""
from datetime import datetime, timedelta
# import calendar
from flask_login import UserMixin
from flask_bcrypt import Bcrypt

from shotstuff.database import db
# from shotstuff.utils import generate_friendly_date_time, convert_date_to_tz
# from shotstuff.treatments.models import Treatment

bcrypt = Bcrypt()


class User(UserMixin, db.Model):
    """User."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.Text, nullable=False)
    first_name = db.Column(db.Text, nullable=False)
    timezone_location = db.Column(
        db.Text,
        nullable=False,
        default='US/Pacific'
    )
    treatments = db.relationship('Treatment', backref='user')
    labs = db.relationship(
        'Lab',
        secondary="treatments",
        backref='user'
    )

    @property
    def num_injections(self):
        """
        Returns the total integer number of injections this user has completed.
        """

        count = 0

        for t in self.treatments:
            count += len(t.injections)

        return count

    @property
    def active_treatments(self):
        """Return list of treatments marked currently active."""

        return [t for t in self.treatments if t.currently_active]

    @property
    def upcoming_labs(self):
        """Return list of labs marked as upcoming."""

        return [l for l in self.labs if not l.occurred_at]

    @property
    def past_labs(self):
        """Return list of labs not marked as upcoming."""

        return [l for l in self.labs if l.occurred_at]

    @property
    def on_time_lab_percentage(self):
        """Return stats on completed labs marked on-time."""

        if self.labs:
            on_time_labs = [l for l in self.labs if l.completed_on_time]
            percentage = (len(on_time_labs)/len(self.labs)) * 100
            return f"{percentage}%"

    @property
    def upcoming_injection_times(self):
        """
        Return list of injections occuring in the next 14 days for all active
        treatments.
        """

        two_weeks_in_seconds = 1209600
        two_weeks_time = datetime.utcnow() + timedelta(seconds=two_weeks_in_seconds)
        upcoming_injection_times = []

        for t in self.active_treatments:
            if len(t.injections) > 0:
                next_inj = t.calculate_next_injection_detail()
                formatted_date = next_inj["time_due"]["full_date_time"].split(",")[0]
                date = datetime.strptime(formatted_date, '%m/%d/%Y')
                if date < two_weeks_time:
                    upcoming_injection_times.append(
                        {
                            "full_date_time": next_inj["time_due"],
                            "formatted_date": formatted_date,
                            "treatment": t
                        }
                    )
        return upcoming_injection_times

    @property
    def treatments_needing_refills(self):
        """
        Return list of all treatments where a refill is needed within the next
        10 days.
        """

        return [t for t in self.treatments if t.is_refill_needed == True]

    @classmethod
    def signup(cls, username, password, first_name):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            password=hashed_pwd,
            first_name=first_name
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False