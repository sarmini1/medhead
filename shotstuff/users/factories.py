import factory

from shotstuff import app
from shotstuff.database import db
from shotstuff.users.models import User

class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Factory to create a User instance for testing."""

    class Meta:
        model = User
        sqlalchemy_session = db.session
        sqlalchemy_get_or_create = ('id',)

    id = 1
    username = "test_username"
    first_name = 'test_firstname'
    password = 'password'
