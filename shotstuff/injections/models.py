from datetime import datetime

from shotstuff.database import db

class Injection(db.Model):
    """Injection."""

    __tablename__ = "injections"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    treatment_id = db.Column(
        db.Integer,
        db.ForeignKey("treatments.id", ondelete="cascade"),
        nullable=False
    )
    medication_id = db.Column(
        db.Integer,
        db.ForeignKey("medications.id", ondelete="cascade"),
        nullable=False
    )
    method = db.Column(db.Text, nullable=False)
    body_region_id = db.Column(
        db.Integer,
        db.ForeignKey("body_regions.id", ondelete="cascade"),
        nullable=False
    )
    body_region = db.relationship("BodyRegion")
    position_id = db.Column(
        db.Integer,
        db.ForeignKey("positions.id", ondelete="cascade"),
        nullable=False
    )
    position = db.relationship("Position")
    occurred_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow()
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

    def generate_friendly_date_time(self):
        """
        Returns dictionary with year, month, day, time, date and time formatted
        in a friendly way.
        """

        year = self.occurred_at.strftime("%Y")
        month = self.occurred_at.strftime("%m")
        day = self.occurred_at.strftime("%d")
        time = self.occurred_at.strftime("%H:%M:%S")
        full_date_time = self.occurred_at.strftime("%m/%d/%Y, %H:%M:%S")

        return {
            "year": year,
            "month": month,
            "day": day,
            "time": time,
            "full_date_time": full_date_time
        }
