import factory

from shotstuff import app
from shotstuff.database import db
from shotstuff.positions.models import Position

class PositionFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Factory to create a User instance for testing."""

    class Meta:
        model = Position
        sqlalchemy_session = db.session
        sqlalchemy_get_or_create = (
            'id',
            'horizontal',
            'vertical'
        )

    id = 1
    horizontal = 'right'
    vertical = 'lower'
