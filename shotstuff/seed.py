from shotstuff import app
from shotstuff.database import db
from shotstuff.users.models import User
from shotstuff.treatments.models import Treatment
from shotstuff.injections.models import Injection
from shotstuff.labs.models import Lab
from shotstuff.medications.models import Medication
from shotstuff.medication_regimens.models import MedicationRegimen
from shotstuff.positions.models import Position
from shotstuff.body_regions.models import BodyRegion


db.drop_all(app=app)
db.create_all(app=app)

u1 = User.signup(
    first_name="test first1",
    username="test_user1",
    password="password"
)

u2 = User.signup(
    first_name="test first2",
    username="test_user2",
    password="password"
)

m1 = Medication(
    name = "test med1"
)

m2 = Medication(
    name = "test med2"
)

br1 = BodyRegion(
    name = "abdomen"
)

br2 = BodyRegion(
    name = "thigh"
)

p1 = Position(
    horizontal_position = "left",
    vertical_position = "upper"
)

p2 = Position(
    horizontal_position = "right",
    vertical_position = "lower"
)

db.session.add_all([u1, u2, m1, m2, br1, br2, p1, p2])
db.session.commit()

first_user = User.query.first()
med = Medication.query.first()
body_region = BodyRegion.query.first()
position = Position.query.first()

# mr1 = InjectionRegimen(
#     title = "first injection regimen title",
#     medication_id = med.id
# )

# mr2 = InjectionRegimen(
#     title = "second injection regimen title",
#     medication_id = med.id
# )

mr1 = MedicationRegimen(
    title = "first medication regimen title",
    is_for_injectable=True,
    medication_id = med.id
)

mr2 = MedicationRegimen(
    title = "second medication regimen title",
    is_for_injectable=False,
    medication_id = med.id
)

db.session.add_all([mr1, mr2])
db.session.commit()

first_regimen = MedicationRegimen.query.first()

t1 = Treatment(
    user_id = u1.id,
    medication_regimen_id = mr1.id,
    frequency_in_seconds = 864000,
    requires_labs = True,
    lab_frequency_in_months = 3,
    lab_point_in_cycle = "peak",
    next_lab_due_date = "2022-06-16",
    clinic_supervising = "UCSF"
)

t2 = Treatment(
    user_id = u1.id,
    medication_regimen_id = mr2.id,
    frequency_in_seconds = 86400,
    requires_labs = True,
    lab_frequency_in_months = 3,
    lab_point_in_cycle = "trough",
    next_lab_due_date = "2022-06-16",
    clinic_supervising = "One Medical"
)

t3 = Treatment(
    user_id = u2.id,
    medication_regimen_id = mr2.id,
    frequency_in_seconds= 777600,
    requires_labs = False,
    clinic_supervising = "Foresight"
)

mt4 = Treatment(
    user_id = u1.id,
    medication_regimen_id = mr1.id,
    frequency_in_seconds= 777600,
    requires_labs = False,
    clinic_supervising = "Foresight"
)

mt5 = Treatment(
    user_id = u1.id,
    medication_regimen_id = mr2.id,
    frequency_in_seconds= 777600,
    requires_labs = True,
    clinic_supervising = "Foresight"
)

db.session.add_all([t1, t2, t3, mt4, mt5])
db.session.commit()

# lab that has already occurred that was done correctly
correct_past_lab = Lab(
    treatment_id = t1.id,
    # user_id = u1.id,
    occurred_at = None,
    point_in_cycle_occurred = "peak",
    # is_upcoming = False,
    requires_fasting = True
)

upcoming_lab = Lab(
    treatment_id = t1.id,
    # occurred_at = None,
    # point_in_cycle_occurred = "peak",
    # is_upcoming = True,
    requires_fasting = True
)

incorrect_past_lab = Lab(
    treatment_id = t1.id,
    occurred_at = None,
    point_in_cycle_occurred = "trough",
    # is_upcoming = False,
    requires_fasting = False
)

db.session.add_all([correct_past_lab, upcoming_lab, incorrect_past_lab])
db.session.commit()

i1 = Injection(
    treatment_id = t1.id,
    # medication_id = mr1.medication_id,
    method = "subcutaneous",
    body_region_id = br1.id,
    position_id = p1.id
)

i2 = Injection(
    treatment_id = t1.id,
    # medication_id = mr1.medication_id,
    method = "subcutaenous",
    body_region_id = br1.id,
    position_id = p2.id,
    notes = "Used second to last injection needle"
)

i3 = Injection(
    treatment_id = t2.id,
    # medication_id = mr2.medication_id,
    method = "intramuscular",
    body_region_id = br2.id,
    position_id = p2.id
)

db.session.add_all([i1, i2, i3])
db.session.commit()