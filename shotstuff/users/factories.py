import factory

from shotstuff import app
from shotstuff.database import db
from shotstuff.users.models import User, bcrypt

def set_password(password='password'):
        """Don't know if this is anything"""

        breakpoint()
        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')
        return hashed_pwd


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Factory to create a User instance for testing."""

    class Meta:
        model = User
        sqlalchemy_session = db.session
        sqlalchemy_get_or_create = ('id',)

    id = 101
    username = "test_username"
    first_name = 'test_firstname'
    # email = factory.LazyAttribute(lambda a: '{}.{}@example.com'.format(a.first_name, a.last_name).lower())
    password = factory.LazyAttribute(set_password)
