from shotstuff.database import db


class Lab(db.Model):
    """Lab."""

    __tablename__ = "labs"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    treatment_id = db.Column(
        db.Integer,
        db.ForeignKey("treatments.id", ondelete="cascade"),
        nullable=False
    )
    is_routine_lab = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )
    # Some labs can be requested if something unexpected comes back from routine labs
    is_supplemental_lab = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )
    # is_upcoming = db.Column(
    #     db.Boolean,
    #     nullable=False,
    #     default=True
    # )
    requires_fasting = db.Column(
        db.Boolean,
        nullable=False
    )
    occurred_at = db.Column(
        db.DateTime,
        nullable=True,
        # default=datetime.utcnow()
    )
    point_in_cycle_occurred = db.Column(
        db.Text,
        nullable=True
    )
    # below to be updated only upon updating an upcoming lab
    completed_on_time = db.Column(
        db.Boolean,
        nullable=True,
        default=None
    )

    treatment = db.relationship('Treatment')
