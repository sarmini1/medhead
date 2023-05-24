import factory
import datetime

from shotstuff import app
from shotstuff.database import db
from shotstuff.injections.models import Injection
from shotstuff.treatments.factories import TreatmentFactory
from shotstuff.body_regions.factories import BodyRegionFactory
from shotstuff.positions.factories import PositionFactory
# from shotstuff.utils import calculate_date


class InjectionFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Factory to create a Injection instance for testing."""

    class Meta:
        model = Injection
        sqlalchemy_session = db.session
        sqlalchemy_get_or_create = (
            'id',
        )

    id = 1
    treatment_id = 1
    method = "subcutaneous"
    body_region_id = 1
    body_region = factory.SubFactory(BodyRegionFactory)
    position_id = 1
    position = factory.SubFactory(PositionFactory)
    occurred_at = datetime.datetime.utcnow()
    notes = "pretty smooth"