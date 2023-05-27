import factory
import datetime

from shotstuff import app
from shotstuff.database import db
from shotstuff.labs.models import Lab
from shotstuff.treatments.factories import TreatmentFactory


class LabFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Factory to create a Lab instance for testing."""

    class Meta:
        model = Lab
        sqlalchemy_session = db.session
        sqlalchemy_get_or_create = (
            'id',
        )

    id = 101
    treatment_id = 101
    treatment = factory.SubFactory(TreatmentFactory)
    is_routine_lab = True
    is_supplemental_lab = False
    requires_fasting = False
    occurred_at = datetime.datetime.utcnow()
    point_in_cycle_occurred = "peak"
    completed_on_time = True