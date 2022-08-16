from flask import Flask

from shotstuff.config import DATABASE_URL
from shotstuff.database import connect_db
from shotstuff.root.routes import root

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.register_blueprint(root)

connect_db(app)