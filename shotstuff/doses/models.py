from datetime import datetime

from shotstuff.database import db
from shotstuff.utils import generate_friendly_date_time


class Dose(db.Model):
    """Dose."""

    __tablename__ = "doses"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    treatment_id = db.Column(
        db.Integer,
        db.ForeignKey("treatments.id", ondelete="cascade"),
        nullable=False
    )

    was_injected = db.Column(
        db.Boolean,
        nullabe=False,
        default=False
    )

    method = db.Column(db.Text, nullable=False)

    body_region_id = db.Column(
        db.Integer,
        db.ForeignKey("body_regions.id", ondelete="cascade"),
        nullable=True
    )

    # body_region = db.relationship("BodyRegion")

    position_id = db.Column(
        db.Integer,
        db.ForeignKey("positions.id", ondelete="cascade"),
        nullable=True
    )

    # position = db.relationship("Position")

    occurred_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow()
        #TODO: remove this defaulting to now
    )

    notes = db.Column(
        db.Text,
        nullable=True
    )

    def to_dict(self):
        """Serialize injection to a dict of info."""

        return {
            "id": self.id,
            "treatment_id": self.treatment_id,
            "medication_id": self.medication_id,
            "method": self.method,
            "body_region_id": self.body_region_id,
            "position_id": self.position_id,
            "occurred_at": self.occurred_at
        }

    @property
    def friendly_dose_time(self):
        """
        Returns dictionary with year, month, day, time, date and time formatted
        in a friendly way.
        """

        return generate_friendly_date_time(self.occurred_at)
