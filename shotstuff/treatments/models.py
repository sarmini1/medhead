from datetime import datetime, timedelta

from shotstuff.database import db
from shotstuff.labs.models import Lab
from shotstuff.injections.models import Injection
from shotstuff.utils import calculate_date, generate_friendly_date_time


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

    fills = db.relationship(
        'Fill',
        backref="treatment"
    )

    @property
    def friendly_start_date(self):
        """
        Looks on the instance and generates a dictionary of time data about the
        current instance's start date.
        """
        # TODO: since start date can be null/unknown, assess path forward if
        # someone tries to access this property on such an instance
        try:
            return generate_friendly_date_time(self.start_date)
        except AttributeError:
            return None

    @property
    def friendly_next_lab_due_date(self):
        """
        Looks on the instance and generates a dictionary of time data about the
        current instance's next lab due date.
        """

        try:
            return generate_friendly_date_time(self.next_lab_due_date)
        except AttributeError:
            return None

    @property
    def friendly_last_fill_date(self):
        """
        Looks on the instance and generates a dictionary of time data about the
        current instance's next lab due date.
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
        """
        # TODO: consider adding error handling if we try to call this method
        # for a non-injectable treatment to match other method below.

        num_injections_occurred = len(self.injections)

        if num_injections_occurred == 0:
            return None
        last_injection = self.injections[num_injections_occurred - 1]
        friendly_occurred_at = generate_friendly_date_time(
                last_injection.occurred_at
        )

        return {
            "injection": last_injection,
            "occurred_at": friendly_occurred_at
        }

    @property
    def is_refill_needed(self):
        """
        Returns boolean depending on if we're 10 days or fewer out from the date
        when their most-recent fill should run out, based on their last dose and
        that fill's days supply.
        """

        # figure out when that fill may run out
        # if we are within 10 days of that date, return True
        # else, return False
        if not self.last_fill:
            return False

        run_out_date_minus_10_days = self.calculate_run_out_date_last_fill() - timedelta(days=10)

        return datetime.utcnow() >= run_out_date_minus_10_days

    @property
    def friendly_run_out_date_info(self):
        """
        Returns dictionary with friendly run out date and boolean telling us
        if that date is past the current date.
        """
        run_out_date = self.calculate_run_out_date_last_fill()
        friendly_date = generate_friendly_date_time(run_out_date)

        return {
            "friendly_date": friendly_date,
            "is_overdue": run_out_date < datetime.utcnow()
        }

    def calculate_run_out_date_last_fill(self):
        """
        Returns the date by which the most recent fill, with its days supply
        will run out.
        """

        # find the most recent dose/injection from their last fill
            # query injections/doses for this treatment where occurred at is
            # after fill date, order by asc and select the first record

        # add the days supply from the fill to that most recent dose date

        most_recent_dose = Injection.query.filter(
            Injection.occurred_at < datetime.utcnow()
        ).order_by(
            Injection.occurred_at.asc()
        ).first()

        run_out_date = most_recent_dose.occurred_at + timedelta(days=self.last_fill.days_supply)
        return run_out_date
        # return (run_out_date, run_out_date > datetime.utcnow())

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
            raise AttributeError("No injections yet!")

        last_injection = self.injections[num_injections_occurred - 1]
        frequency = self.frequency_in_seconds

        next_inj_date = last_injection.occurred_at + timedelta(seconds=frequency)
        next_inj_position = self._find_next_injection_position()

        return {
            "time_due": generate_friendly_date_time(next_inj_date),
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

        # converted_datetime = datetime.strptime(
        #     self.next_lab_due_date,
        #     '%Y-%m-%d'
        # )
        # TODO: decide if we need this string-to-Date obj conversion above
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

    def to_dict(self):
        """Serialize to a dict of regimen info."""

        return {
            "id": self.id,
            "user_id": self.user_id,
            "medication_regimen_id": self.medication_regimen_id,
        }
