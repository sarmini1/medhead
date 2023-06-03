import factory
import datetime

from shotstuff import app
from shotstuff.database import db
from shotstuff.injections.models import Injection
from shotstuff.treatments.factories import TreatmentFactory
from shotstuff.body_regions.factories import BodyRegionFactory
from shotstuff.positions.factories import PositionFactory


class InjectionFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Factory to create a Injection instance for testing."""

    class Meta:
        model = Injection
        sqlalchemy_session = db.session
        sqlalchemy_get_or_create = (
            'id',
        )

    id = factory.Sequence(lambda n: n) #TODO: decide when this is appropriate in other factories, too
    treatment_id = 101
    treatment = factory.SubFactory(TreatmentFactory)
    method = "subcutaneous"
    body_region_id = 1
    body_region = factory.SubFactory(BodyRegionFactory)
    position_id = 1
    position = factory.SubFactory(PositionFactory)
    occurred_at = factory.LazyFunction(datetime.datetime.now)
    notes = "pretty smooth"