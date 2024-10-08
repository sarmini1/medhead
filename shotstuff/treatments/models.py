from datetime import datetime, timedelta

from shotstuff.database import db
from shotstuff.labs.models import Lab
from shotstuff.injections.models import Injection
from shotstuff.utils import (
    calculate_date,
    generate_friendly_date_time,
    convert_date_to_tz
)


class Treatment(db.Model):
    """Treatment."""

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
    # Storing currently_active status so that we can store deprecated
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
    # Below column could be a foreign key to a clinics table, but that would
    # require me to create a clinics table, which maybe implies a doctors table,
    # and there isn't really a reason for that info yet. Users probably just
    # need to be reminded of which clinic to go to or call about a treatment/lab
    clinic_supervising = db.Column(
        db.Text,
        nullable=True
    )
    medication_regimen = db.relationship(
        'MedicationRegimen',
        backref="treatments"
    )

    injections = db.relationship(
        'Injection',
        backref="treatment"
    )

    fills = db.relationship(
        'Fill',
        backref="treatment"
    )

    @property
    def friendly_start_date(self):
        """
        Looks on the instance and generates a dictionary of time data about the
        current instance's start date.

        Returns None if an AttributeError occurs.
        """

        try:
            return generate_friendly_date_time(self.start_date)
        except AttributeError:
            return None

    @property
    def friendly_next_lab_due_date(self):
        """
        Looks on the instance and generates a dictionary of time data about the
        current instance's next lab due date.

        Returns None if an AttributeError occurs.
        """

        try:
            return generate_friendly_date_time(self.next_lab_due_date)
        except AttributeError:
            return None

    @property
    def friendly_last_fill_date(self):
        """
        Looks on the instance and generates a dictionary of time data about the
        current instance's last fill date.

        Returns None if an AttributeError occurs.
        """

        try:
            return generate_friendly_date_time(self.last_fill.occurred_at)
        except AttributeError:
            return None

    @property
    def last_injection_details(self):
        """Determines the last injection that occurred for a treatment.

        Returns dictionary:
         {
            last_injection: Injection,
            occurred_at: {year, month, day, time, full_date_time }
         }

         If called on a treatment instance for a non-injectable, raises
         AttributeError.
        """

        if not self.medication_regimen.is_for_injectable:
            raise AttributeError("This treatment is not for an injectable medication.")

        num_injections_occurred = len(self.injections)

        if num_injections_occurred == 0:
            return None
        last_injection = self.injections[num_injections_occurred - 1]

        occurred_at_with_tz = convert_date_to_tz(
            last_injection.occurred_at,
            self.user.timezone_location
        )
        friendly_occurred_at_with_tz = generate_friendly_date_time(
                occurred_at_with_tz
        )

        return {
            "injection": last_injection,
            "occurred_at": friendly_occurred_at_with_tz
        }

    @property
    def is_refill_needed(self):
        """
        Returns boolean:

        True if we're 10 days or fewer out from the date
        when their most-recent fill should run out, based on their last dose and
        that fill's days supply.

        False if they've never had a fill or haven't started the treatment.
        """

        # Figure out when that fill may run out
        # If we are within 10 days of that date, return True
        # Else, return False
        if not self.last_fill or not self.start_date:
            return False

        run_out_date_minus_10_days = self.calculate_run_out_date_last_fill() - timedelta(days=10)

        return datetime.utcnow() >= run_out_date_minus_10_days

    @property
    def friendly_run_out_date_info(self):
        """
        Returns dictionary with friendly run out date and boolean telling us
        if that date is past the current date.
        """
        run_out_date_utc = self.calculate_run_out_date_last_fill()
        run_out_date_with_tz = convert_date_to_tz(
            run_out_date_utc,
            self.user.timezone_location
        )
        friendly_date = generate_friendly_date_time(run_out_date_with_tz)

        return {
            "friendly_date": friendly_date,
            "is_overdue": run_out_date_utc < datetime.utcnow()
        }

    def calculate_run_out_date_last_fill(self):
        """
        Returns the datetime object, in UTC, by which the most recent fill,
        with its days supply will run out.
        """

        if self.medication_regimen.is_for_injectable:
            most_recent_dose = Injection.query.filter(
                Injection.occurred_at < datetime.utcnow()
            ).order_by(
                Injection.occurred_at.asc()
            ).first()

            run_out_date = most_recent_dose.occurred_at + timedelta(days=self.last_fill.days_supply)
        else:
            run_out_date = self.last_fill.occurred_at + timedelta(days=self.last_fill.days_supply)

        return run_out_date

    @property
    def last_fill(self):
        """Determines when the most recent fill occurred for a treatment and
        returns that Fill instance or None if none have occurred.
        """

        num_fills_occurred = len(self.fills)

        if num_fills_occurred == 0:
            return None
        last_fill = self.fills[num_fills_occurred - 1]

        return last_fill

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

        next_inj_date_utc = last_injection.occurred_at + timedelta(seconds=frequency)
        next_inj_date_tz = convert_date_to_tz(
            next_inj_date_utc,
            self.user.timezone_location
        )
        next_inj_position = self._find_next_injection_position()

        return {
            "time_due": generate_friendly_date_time(next_inj_date_tz),
            "position": next_inj_position
        }

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

    def update_next_lab_due_date(self):
        """
        Looks on current instance's next_lab_due_date time and updates
        according to routine lab frequency. Generates new upcoming lab instance
        for current instance. Returns None.
        """

        self.next_lab_due_date = calculate_date(
            self.next_lab_due_date,
            self.lab_frequency_in_months
        )

        upcoming_lab = Lab(
            treatment_id = self.id,
            requires_fasting = False,
            occurred_at = None,
            point_in_cycle_occurred = None
        )
        db.session.add(upcoming_lab)
