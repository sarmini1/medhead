from shotstuff.database import db

class BodyRegion(db.Model):
    """Region of body."""

    __tablename__ = "body_regions"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)