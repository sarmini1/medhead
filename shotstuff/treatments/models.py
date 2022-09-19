from datetime import datetime, timedelta, date
import calendar

from shotstuff.database import db
# from shotstuff.injection_regimens.models import InjectionRegimen


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
    # is_for_injectable = db.Column(
    #     db.Boolean,
    #     nullable=False,
    #     default=True
    # )
    # injection_regimen_id = db.Column(
    #     db.Integer,
    #     db.ForeignKey("injection_regimens.id"),
    #     nullable=True
    # )
    medication_regimen_id = db.Column(
        db.Integer,
        db.ForeignKey("medication_regimens.id"),
        nullable=True
    )
    # currently_active = db.Column(
    #     db.Boolean,
    #     nullable=False,
    #     default=True
    # )
    start_date = db.Column(
        db.Date,
        nullable=True,
        # default=date.today()
    )
    frequency_in_seconds = db.Column(
        db.Integer,
        db.CheckConstraint("frequency_in_seconds > 0"),
        nullable=False
    )
    # injection_regimen = db.relationship('InjectionRegimen')
    medication_regimen = db.relationship('MedicationRegimen')

    injections = db.relationship('Injection',
                                  backref="treatment")
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
        # for a non-injectable treatment. Same for other injection method below.

        num_injections_occurred = len(self.injections)
        if num_injections_occurred == 0:
            return None
        last_injection = self.injections[num_injections_occurred - 1]

        # breakpoint()
        return {
            "injection": last_injection,
            "occurred_at": self.generate_friendly_date_time(
                last_injection.occurred_at
                )
        }

    @property
    def next_injection_time(self):
        """
        Based on the date of their most recent injection and the injection
        frequency of their treatment, return the date when their next injection
        is due.
        """

        num_injections_occurred = len(self.injections)

        # TODO: need to handle case when no injections have occurred yet,
        # this is just an ungraceful placeholder
        if num_injections_occurred == 0:
            return "No injections added yet!"

        last_injection = self.injections[num_injections_occurred - 1]
        frequency = self.frequency_in_seconds

        next_inj_date = last_injection.occurred_at + timedelta(seconds=frequency)

        return self.generate_friendly_date_time(next_inj_date)

    def to_dict(self):
        """Serialize to a dict of regimen info."""

        return {
            "id": self.id,
            "user_id": self.user_id,
            "medication_regimen_id": self.medication_regimen_id,
        }

    def generate_friendly_date_time(self, date):
        """ Returns dictionary with year, month, day, time, date and time formatted
            in a friendly way.
        """

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