from datetime import datetime, timedelta
import calendar

from shotstuff.database import db
from shotstuff.labs.models import Lab
from shotstuff.utils import calculate_date


class Treatment(db.Model):
    """Treatment."""

    # This table is meant to connect users and injection regimens

    __tablename__ = "treatments"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="cascade"),
        nullable=False
    )

    # User model has 'treatments' property with 'user' backref

    medication_regimen_id = db.Column(
        db.Integer,
        db.ForeignKey("medication_regimens.id"),
        nullable=True
    )
    # storing currently_active status so that we can store deprecated
    # treatments
    currently_active = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )
    start_date = db.Column(
        db.Date,
        nullable=True,
    )
    end_date = db.Column(
        db.Date,
        nullable=True,
    )
    frequency_in_seconds = db.Column(
        db.Integer,
        db.CheckConstraint("frequency_in_seconds > 0"),
        nullable=False
    )
    requires_labs = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )
    lab_frequency_in_months = db.Column(
        db.Integer,
        db.CheckConstraint("lab_frequency_in_months > 0"),
        nullable=True
    )
    # TODO: change name to routine_lab_point_in_cycle
    lab_point_in_cycle = db.Column(
        db.Text,
        nullable=True
    )
    next_lab_due_date = db.Column(
        db.Date,
        nullable=True
    )
    # below column could be a foreign key to a clinics table, but that would
    # require me to create a clinics table, which maybe implies a doctors table,
    # and there isn't really a reason for that info yet? users probably just
    # need to be reminded of which clinic to go to or call about a treatment/lab
    clinic_supervising = db.Column(
        db.Text,
        nullable=True
    )
    medication_regimen = db.relationship('MedicationRegimen')

    injections = db.relationship(
        'Injection',
        backref="treatment"
    )

    @property
    def friendly_start_date(self):
        """TBD"""
        return self.generate_friendly_date_time(self.start_date)

    @property
    def last_injection_details(self):
        """Determines the last injection that occurred for a treatment.

        Returns dictionary:
         {
            last_injection: Injection,
            occurred_at: {year, month, day, time, full_date_time }
         }
        """
        # TODO: consider adding error handling if we try to call this method
        # for a non-injectable treatment to match other method below.

        num_injections_occurred = len(self.injections)

        if num_injections_occurred == 0:
            return None
        last_injection = self.injections[num_injections_occurred - 1]
        friendly_occurred_at = self.generate_friendly_date_time(
                last_injection.occurred_at
        )

        return {
            "injection": last_injection,
            "occurred_at": friendly_occurred_at
        }

    def calculate_next_injection_detail(self):
        """
        Based on the date and position of their most recent injection and
        the injection frequency of their treatment, return the dict of
        date/time info and position tuple for their next injection.
        Returns dictionary like:

        {
            "time_due": {year, month, day, time, ... },
            "position": ("left", "lower")
        }

        If no injections have occurred for this treatment, raises ValueError.
        """

        num_injections_occurred = len(self.injections)

        if num_injections_occurred == 0:
            raise ValueError("No injections yet!")

        last_injection = self.injections[num_injections_occurred - 1]
        frequency = self.frequency_in_seconds

        next_inj_date = last_injection.occurred_at + timedelta(seconds=frequency)
        next_inj_position = self._find_next_injection_position()

        return {
            "time_due": self.generate_friendly_date_time(next_inj_date),
            "position": next_inj_position
        }

    def update_next_lab_due_date(self):
        """
        Looks on current instance's next_lab_due_date time and updates
        according to routine lab frequency. Generates new upcoming lab instance
        for current instance. Returns None.
        """

        converted_datetime = datetime.strptime(
            self.next_lab_due_date,
            '%Y-%m-%d'
        )
        self.next_lab_due_date = calculate_date(
            converted_datetime,
            self.lab_frequency_in_months
        )

        upcoming_lab = Lab(
            treatment_id = self.id,
            requires_fasting = False,
            occurred_at = None,
            point_in_cycle_occurred = None
        )
        db.session.add(upcoming_lab)

    def _find_next_injection_position(self):
        """
        Looks at the most recent injection and returns the placement, a tuple like
        ("left", "lower"), where the next injection is due.
        """

        ordered_positions = [
            ("left", "lower"),
            ("right", "upper"),
            ("left", "upper"),
            ("right", "lower"),
        ]
        last_inj = self.last_injection_details["injection"]

        last_inj_position = (
            last_inj.position.horizontal,
            last_inj.position.vertical
        )
        next_position_idx = ordered_positions.index(last_inj_position) + 1
        if next_position_idx >= len(ordered_positions):
            next_position_idx = 0

        next_position = ordered_positions[next_position_idx]
        return next_position

    def to_dict(self):
        """Serialize to a dict of regimen info."""

        return {
            "id": self.id,
            "user_id": self.user_id,
            "medication_regimen_id": self.medication_regimen_id,
        }

    # TODO: assess how to break this method out to be more generic
    def generate_friendly_date_time(self, date):
        """ Returns dictionary with year, month, day, time, date and time formatted
            in a friendly way.
        """
        # breakpoint()
        year = date.strftime("%Y")
        month = date.strftime("%m")
        day = date.strftime("%d")
        time = date.strftime("%H:%M:%S")
        full_date_time = date.strftime("%m/%d/%Y, %H:%M:%S")

        return {
            "year": year,
            "month": month,
            "day": day,
            "time": time,
            "weekday": calendar.day_name[date.weekday()],
            "full_date_time": full_date_time
        }