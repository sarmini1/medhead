import factory

from shotstuff import app
from shotstuff.database import db
from shotstuff.body_regions.models import BodyRegion

class BodyRegionFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Factory to create a BodyRegion instance for testing."""

    class Meta:
        model = BodyRegion
        sqlalchemy_session = db.session
        sqlalchemy_get_or_create = ('id',)

    id = factory.Sequence(lambda n: n)
    name = 'abdomen'
