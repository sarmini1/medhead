from shotstuff.database import db


class Position(db.Model):
    """Position."""

    __tablename__ = "positions"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    horizontal = db.Column(
        db.Text,
        nullable=False,
    )
    vertical = db.Column(
        db.Text,
        nullable=False
    )
