from shotstuff.database import db

#TODO: this was made after the injection regimen model was made-- idea is that
# a user taking a medication shouldn't have to be injectable for it to be
# considered a treatment
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
    medication_id = db.Column(
        db.Integer,
        db.ForeignKey("medications.id", ondelete="cascade"),
        nullable=False
    )

    def to_dict(self):
        """Serialize to a dict of regimen info."""

        return {
            "id": self.id,
            "title": self.title,
            "medication_id": self.medication_id,
        }
