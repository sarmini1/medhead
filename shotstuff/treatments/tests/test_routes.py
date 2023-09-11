import sys
sys.path.append('../../../')

# from freezegun import freeze_time
import unittest
# import datetime
from flask_login import FlaskLoginClient

from shotstuff import app
from shotstuff.database import db
from shotstuff.config import DATABASE_URL_TEST
from shotstuff.treatments.factories import TreatmentFactory
from shotstuff.fills.factories import FillFactory

app.test_client_class = FlaskLoginClient
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL_TEST
app.config["TESTING"] = True
app.config["SQLALCHEMY_ECHO"] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['WTF_CSRF_ENABLED'] = False

db.drop_all()
db.create_all()


class TreatmentRouteTestCase(unittest.TestCase):

    def setUp(self):

        self.t1 = TreatmentFactory()
        self.f1 = FillFactory()

    def tearDown(self):
        db.session.rollback()
