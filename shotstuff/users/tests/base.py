# from unittest import TestCase
# from shotstuff import app
# from shotstuff.database import db
# from shotstuff.config import DATABASE_URL_TEST
# from shotstuff.users.models import User
# from shotstuff.medications.models import Medication
# from shotstuff.medication_regimens.models import MedicationRegimen
# from shotstuff.treatments.models import Treatment
# from shotstuff.labs.models import Lab
# from shotstuff.injections.models import Injection
# from shotstuff.body_regions.models import BodyRegion
# from shotstuff.positions.models import Position

# app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL_TEST
# app.config["TESTING"] = True
# app.config["SQLALCHEMY_ECHO"] = False
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db.drop_all()
# db.create_all()

# class UserModelBaseTestCase(TestCase):
#     def setUp(self):
#         """Set up test data here"""

#         Injection.query.delete()
#         Lab.query.delete()
#         Treatment.query.delete()
#         MedicationRegimen.query.delete()
#         Medication.query.delete()
#         User.query.delete()
#         BodyRegion.query.delete()
#         Position.query.delete()

#         self.u1 = User.signup(
#             first_name="test first1",
#             username="test_user1",
#             password="password",
#         )

#         self.med1 = Medication(
#             name = "testosterone cypionate"
#         )

#         self.br1 = BodyRegion(
#             name = "abdomen"
#         )

#         self.br2 = BodyRegion(
#             name = "thigh"
#         )

#         self.p1 = Position(
#             horizontal = "left",
#             vertical = "lower"
#         )

#         self.p2 = Position(
#             horizontal = "right",
#             vertical = "lower"
#         )

#         self.p3 = Position(
#             horizontal = "right",
#             vertical = "upper"
#         )

#         self.p4 = Position(
#             horizontal = "left",
#             vertical = "upper"
#         )

#         db.session.add_all([
#             self.med1,
#             self.br1,
#             self.br2,
#             self.p1,
#             self.p2,
#             self.p3,
#             self.p4,
#         ])
#         db.session.commit()

#         self.mr1 = MedicationRegimen(
#             title = "testosterone for hrt",
#             is_for_injectable=True,
#             route="subcutaneous",
#             medication_id = self.med1.id
#         )

#         db.session.add(self.mr1)
#         db.session.commit()

#         self.t1 = Treatment(
#             user_id = self.u1.id,
#             medication_regimen_id = self.mr1.id,
#             frequency_in_seconds = 864000,
#             requires_labs = True,
#             lab_frequency_in_months = 3,
#             lab_point_in_cycle = "peak",
#             next_lab_due_date = "2022-06-16",
#             clinic_supervising = "UCSF",
#             start_date = "2022-02-16",
#             currently_active = True
#         )

#         db.session.add(self.t1)
#         db.session.commit()

#         self.lab1 = Lab(
#             treatment_id = self.t1.id,
#             occurred_at = None,
#             point_in_cycle_occurred = "peak",
#             requires_fasting = True
#         )

#         db.session.add(self.lab1)
#         db.session.commit()

#         self.i1 = Injection(
#             treatment_id = self.t1.id,
#             method = "subcutaneous",
#             body_region_id = self.br1.id,
#             position_id = self.p1.id
#         )

#         db.session.add(self.i1)
#         db.session.commit()

#     def tearDown(self):
#         """Clean up any fouled transaction."""
#         db.session.rollback()
