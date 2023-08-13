import factory

from shotstuff import app
from shotstuff.database import db
from shotstuff.medications.models import Medication


class MedicationFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Factory to create a Medication instance for testing."""

    class Meta:
        model = Medication
        sqlalchemy_session = db.session
        sqlalchemy_get_or_create = (
            'id',
        )

    id = 1
    name = 'testosterone cypionate'
