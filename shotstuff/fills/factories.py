import factory

from shotstuff import app
from shotstuff.database import db
from shotstuff.fills.models import Fill
# from shotstuff.medication_regimens.factories import MedicationRegimenFactory
# from shotstuff.users.factories import UserFactory
from shotstuff.utils import calculate_date


class FillFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Factory to create a Fill instance for testing."""

    class Meta:
        model = Fill
        sqlalchemy_session = db.session
        sqlalchemy_get_or_create = (
            'id',
        )

    id = 101
    treatment_id = 101
    filled_by = 'Alto'
    days_supply = 32
    # occurred_at has default of now currently
    notes = "Fill factory notes section"