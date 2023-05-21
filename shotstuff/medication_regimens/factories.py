import factory

from shotstuff import app
from shotstuff.database import db
from shotstuff.medication_regimens.models import MedicationRegimen
from shotstuff.medications.factories import MedicationFactory

class MedicationRegimenFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Factory to create a MedicationRegimen instance for testing."""

    class Meta:
        model = MedicationRegimen
        sqlalchemy_session = db.session
        sqlalchemy_get_or_create = (
            'id',
        )

    id = 1
    title = 'Testosterone for HRT'
    is_for_injectable = True
    route = 'subcutaneous'
    medication_id = 1
    medication = factory.SubFactory(MedicationFactory)
