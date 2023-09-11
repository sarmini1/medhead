import sys
sys.path.append('../../../')

# from freezegun import freeze_time
import unittest
# import datetime
from flask_login import FlaskLoginClient
from flask import session

from shotstuff import app, login_manager
from shotstuff.database import db, connect_db
from shotstuff.config import DATABASE_URL_TEST
from shotstuff.treatments.factories import TreatmentFactory
from shotstuff.medication_regimens.factories import MedicationRegimenFactory
from shotstuff.injections.factories import InjectionFactory
from shotstuff.fills.factories import FillFactory

from shotstuff.treatments.models import Treatment
from shotstuff.users.models import User

app.test_client_class = FlaskLoginClient
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL_TEST
app.config["TESTING"] = True
app.config["SQLALCHEMY_ECHO"] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['WTF_CSRF_ENABLED'] = False
# login_manager.session_protection = None

# connect_db(app)

db.drop_all()
db.create_all()


class TreatmentRouteTestCase(unittest.TestCase):

    def setUp(self):
        # app.test_client_class = FlaskLoginClient
        self.t1 = TreatmentFactory()
        self.f1 = FillFactory()
        # self.u1 = self.t1.user
        # self.client = app.test_client(user=self.u1)

    def tearDown(self):
        db.session.rollback()

    def test_treatment_listing_page(self):
        """Tests that active treatments are listed appropriately."""

        user = User.query.first()

        # app.test_client_class = FlaskLoginClient
        with app.test_client(user=user, fresh_login=True) as client:

            response = client.get(f'/treatments/users/{user.id}')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
