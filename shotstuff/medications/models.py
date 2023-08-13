from shotstuff.database import db


class Medication(db.Model):
    """Medication."""

    __tablename__ = "medications"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)