from shotstuff.database import db

class Position(db.Model):
    """Site."""

    __tablename__ = "positions"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    horizontal = db.Column(
        db.Text,
        # db.CheckConstraint(
        #     "horizontal_position in ['left', 'right']"
        # ),
        nullable=False,
    )
    vertical = db.Column(
        db.Text,
        # db.CheckConstraint(
        #     "vertical_position in ['upper', 'lower']"
        # ),
        nullable=False
    )
