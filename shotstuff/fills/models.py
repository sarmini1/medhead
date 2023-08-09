from datetime import datetime

from shotstuff.database import db
from shotstuff.utils import generate_friendly_date_time, convert_date_to_pst


class Fill(db.Model):
    """Fill."""

    # A fill should be tied to a treatment-- depending on the date the fill occurred,
    # the days supply of the fill and the frequency of the dose, figure out a nice
    # way to proactively remind a user that they'll need to start planning for
    # their refill soon.

    # If this fill leaves only 1 more remaining, include in the reminder that
    # they may need to reach out to their doctor if their pharmacy doesn't
    # do that for them.

    __tablename__ = "fills"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Treatment model has a 'fills' relationship with a 'treatment' backref

    treatment_id = db.Column(
        db.Integer,
        db.ForeignKey("treatments.id", ondelete="cascade"),
        nullable=False
    )
    filled_by = db.Column(
        db.Text,
        nullable=False
    )
    days_supply = db.Column(
        db.Integer,
        nullable=False
    )
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

    @property
    def friendly_occurred_at(self):
        """
        Returns complete dictionary of time data for a fill's occurred_at time,
        converted to PST.
        """
        occurred_at_pst = convert_date_to_pst(self.occurred_at)
        return generate_friendly_date_time(occurred_at_pst)