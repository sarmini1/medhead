import factory

from shotstuff import app
from shotstuff.database import db
from shotstuff.treatments.models import Treatment
from shotstuff.medication_regimens.factories import MedicationRegimenFactory
from shotstuff.users.factories import UserFactory
from shotstuff.utils import calculate_date


class TreatmentFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Factory to create a Treatment instance for testing."""

    class Meta:
        model = Treatment
        sqlalchemy_session = db.session
        sqlalchemy_get_or_create = (
            'id',
        )

    id = 101
    user_id = 101
    medication_regimen_id = 1
    currently_active = True
    start_date = calculate_date()
    end_date = calculate_date(months_in_future=12)
    frequency_in_seconds = 604800 # 1 week
    requires_labs = True
    lab_frequency_in_months = 3
    lab_point_in_cycle = 'peak'
    # next_lab_due_date
    # clinic_supervising
    medication_regimen = factory.SubFactory(MedicationRegimenFactory)
    user = factory.SubFactory(UserFactory)
