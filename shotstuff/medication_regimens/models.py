from shotstuff.database import db


class MedicationRegimen(db.Model):
    """Medication Regimen."""

    __tablename__ = "medication_regimens"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    is_for_injectable = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )
    route = db.Column(db.Text, nullable=False)
    medication_id = db.Column(
        db.Integer,
        db.ForeignKey("medications.id", ondelete="cascade"),
        nullable=False
    )
    medication = db.relationship('Medication', backref="used_in_regimens")
