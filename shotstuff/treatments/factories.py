import factory

from shotstuff import app
from shotstuff.database import db
from shotstuff.medication_regimens.factories import MedicationRegimenFactory
from shotstuff.users.factories import UserFactory
from shotstuff.treatments.models import Treatment
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
    medication_regimen_id = 101
    currently_active = True
    start_date = factory.LazyFunction(calculate_date)
    end_date = factory.LazyFunction(lambda: calculate_date(months_in_future=12))
    frequency_in_seconds = 604800 # 1 week
    requires_labs = True
    lab_frequency_in_months = 4
    lab_point_in_cycle = 'peak'
    next_lab_due_date = factory.LazyFunction(calculate_date)
    # clinic_supervising
    medication_regimen = factory.SubFactory(MedicationRegimenFactory)
    user = factory.SubFactory(UserFactory)
    # last_fill = factory.SubFactory(FillFactory)
