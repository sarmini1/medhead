# import unittest
# import datetime
# from sqlalchemy.exc import IntegrityError
# from flask_login import FlaskLoginClient

# from shotstuff import app, login_manager
# from shotstuff.database import db
# from shotstuff.config import DATABASE_URL_TEST

# from shotstuff.users.factories import UserFactory
# from shotstuff.treatments.factories import TreatmentFactory
# from shotstuff.injections.factories import InjectionFactory
# from shotstuff.labs.factories import LabFactory

# from shotstuff.users.models import User
# from shotstuff.treatments.models import Treatment
# from shotstuff.medication_regimens.models import MedicationRegimen
# from shotstuff.injections.models import Injection
# from shotstuff.labs.models import Lab

# app.test_client_class = FlaskLoginClient
# app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL_TEST
# app.config["TESTING"] = True
# app.config["SQLALCHEMY_ECHO"] = False
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['WTF_CSRF_ENABLED'] = False

# login_manager.session_protection = None

# db.drop_all()
# db.create_all()


# class UserRoutesTestCase(unittest.TestCase):
#     """Tests User routes."""

#     def setUp(self):
#         """Create test data. """

#         Lab.query.delete()
#         Injection.query.delete()
#         Treatment.query.delete()
#         MedicationRegimen.query.delete()
#         Injection.query.delete()
#         User.query.delete()

#         # InjectionFactory makes a TreatmentFactory instance, which makes
#         # User and MedicationRegimen factory instances under the hood
#         self.i1 = InjectionFactory()
#         self.t1 = self.i1.treatment
#         self.u1 = self.i1.treatment.user

#         # Same note as above for LabFactory
#         self.l1 = LabFactory()
#         self.client = app.test_client()

#     def tearDown(self):
#         # Rollback the session to clean up any fouled transactions
#         db.session.rollback()

#     def test_request_with_logged_in_user(self):
#         user = User.query.get(101)
#         with app.test_client(user=user) as client:
#             breakpoint()
#             # This request has user 1 already logged in!
#             client.get("/")

#     # def test_dashboard_with_logged_in_user(self):
#     #     with self.client as client:
#     #         with client.session_transaction() as sess:
#     #             sess["_user_id"] = self.u1.id
#     #         breakpoint()
#     #         resp = client.get("/users/dashboard")
#     #         html = resp.get_data(as_text=True)

#     #         self.assertEqual(resp.status_code, 200)
#     #         self.assertIn("test_firstname's Dashboard", html)
#     #         self.assertIn("Testosterone for HRT", html)
