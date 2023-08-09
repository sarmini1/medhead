# To run from ipython: %run shotstuff/dev_seed.py

from datetime import datetime, timedelta

from shotstuff import app
from shotstuff.database import db
from shotstuff.users.models import User
from shotstuff.treatments.models import Treatment
from shotstuff.injections.models import Injection
from shotstuff.fills.models import Fill
from shotstuff.labs.models import Lab
from shotstuff.medications.models import Medication
from shotstuff.medication_regimens.models import MedicationRegimen
from shotstuff.positions.models import Position
from shotstuff.body_regions.models import BodyRegion


db.drop_all(app=app)
db.create_all(app=app)

u1 = User.signup(
    first_name="Spencer",
    username="spencer",
    password="password"
)

u2 = User.signup(
    first_name="test first2",
    username="test_user2",
    password="password"
)

med_t = Medication(
    name = "testosterone cypionate"
)

med_prep = Medication(
    name = "truvada"
)

med_finast = Medication(
    name = "finasteride"
)

med_estro = Medication(
    name = "estradiol alsdkfjsld"
)

br1 = BodyRegion(
    name = "abdomen"
)

br2 = BodyRegion(
    name = "thigh"
)

p1 = Position(
    horizontal = "left",
    vertical = "lower"
)

p2 = Position(
    horizontal = "right",
    vertical = "lower"
)

p3 = Position(
    horizontal = "right",
    vertical = "upper"
)

p4 = Position(
    horizontal = "left",
    vertical = "upper"
)

db.session.add_all(
    [u1, u2, med_t, med_prep, med_estro, med_finast, br1, br2, p1, p2, p3, p4]
)
db.session.commit()

first_user = User.query.first()
# med = Medication.query.first()
body_region = BodyRegion.query.first()
position = Position.query.first()

inj_test_mr = MedicationRegimen(
    title = "Testosterone for HRT",
    is_for_injectable=True,
    route="subcutaneous",
    medication_id = med_t.id
)

prep_mr = MedicationRegimen(
    title = "Truvada for PrEP",
    is_for_injectable=False,
    route="oral",
    medication_id = med_prep.id
)

finasteride_mr = MedicationRegimen(
    title = "Finasteride for hair",
    is_for_injectable=False,
    route="oral",
    medication_id = med_finast.id
)
inj_estra_mr = MedicationRegimen(
    title = "Another injectable",
    is_for_injectable=True,
    route="intramuscular",
    medication_id = med_estro.id
)

db.session.add_all(
    [inj_test_mr, prep_mr, finasteride_mr, inj_estra_mr]
)
db.session.commit()

first_regimen = MedicationRegimen.query.first()

# test injectable testosterone treatment
t1_inj = Treatment(
    user_id = u1.id,
    medication_regimen_id = inj_test_mr.id,
    frequency_in_seconds = 691200,
    requires_labs = True,
    lab_frequency_in_months = 3,
    lab_point_in_cycle = "peak",
    next_lab_due_date = "2023-08-30",
    clinic_supervising = "UCSF",
    start_date = "2023-05-27",
    currently_active = True
)

# prep
t2 = Treatment(
    user_id = u1.id,
    medication_regimen_id = prep_mr.id,
    frequency_in_seconds = 86400,
    requires_labs = True,
    lab_frequency_in_months = 3,
    lab_point_in_cycle = "trough",
    next_lab_due_date = "2023-08-16",
    clinic_supervising = "One Medical",
    start_date = "2023-05-27",
    currently_active = True
)

# prep for second user
t3 = Treatment(
    user_id = u2.id,
    medication_regimen_id = prep_mr.id,
    frequency_in_seconds= 777600,
    requires_labs = False,
    clinic_supervising = "Foresight"
)

# finasteride
mt4 = Treatment(
    user_id = u1.id,
    medication_regimen_id = finasteride_mr.id,
    frequency_in_seconds= 86400,
    requires_labs = False,
    clinic_supervising = "Foresight",
    start_date = None,
    currently_active = False
)

#estradiol
t5_inj = Treatment(
    user_id = u1.id,
    medication_regimen_id = inj_estra_mr.id,
    frequency_in_seconds = 864000,
    requires_labs = True,
    lab_frequency_in_months = 3,
    lab_point_in_cycle = "peak",
    next_lab_due_date = "2023-10-16",
    clinic_supervising = "UCSF",
    start_date = "2023-07-16",
    currently_active = True

)

db.session.add_all([t1_inj, t2, t3, mt4, t5_inj])
db.session.commit()

# lab that has already occurred that was done correctly
correct_past_lab_t1_inj = Lab(
    treatment_id = t1_inj.id,
    # user_id = u1.id,
    occurred_at = None,
    point_in_cycle_occurred = "peak",
    # is_upcoming = False,
    requires_fasting = False
)

correct_past_lab_t5_inj = Lab(
    treatment_id = t5_inj.id,
    # user_id = u1.id,
    occurred_at = None,
    point_in_cycle_occurred = "peak",
    # is_upcoming = False,
    requires_fasting = True
)

upcoming_lab = Lab(
    treatment_id = t2.id,
    # occurred_at = None,
    # point_in_cycle_occurred = "peak",
    # is_upcoming = True,
    requires_fasting = True
)

incorrect_past_lab = Lab(
    treatment_id = t1_inj.id,
    occurred_at = None,
    point_in_cycle_occurred = "trough",
    # is_upcoming = False,
    requires_fasting = False
)

db.session.add_all(
    [
        correct_past_lab_t1_inj,
        correct_past_lab_t5_inj,
        upcoming_lab,
        incorrect_past_lab
    ]
)
db.session.commit()

# i1 = Injection(
#     treatment_id = t1_inj.id,
#     method = "subcutaneous",
#     body_region_id = br1.id,
#     position_id = p1.id
# )

i2 = Injection(
    treatment_id = t1_inj.id,
    method = "subcutaenous",
    body_region_id = br1.id,
    position_id = p2.id,
    notes = "Used second to last injection needle",
    occurred_at = datetime.utcnow() - timedelta(days=8),
)

i3 = Injection(
    treatment_id = t5_inj.id,
    method = "intramuscular",
    body_region_id = br2.id,
    position_id = p2.id
)

f1 = Fill(
    treatment_id = t1_inj.id,
    filled_by = "Alto",
    occurred_at = datetime.utcnow() - timedelta(days=30),
    days_supply = 32,
    notes = "Something something",
)

f2 = Fill(
    treatment_id = t2.id,
    filled_by = "CVS",
    occurred_at = datetime.utcnow() - timedelta(days=10),
    days_supply = 30
)

db.session.add_all([i2, i3, f1, f2])
db.session.commit()