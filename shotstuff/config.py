import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ['DATABASE_URL']
DATABASE_URL_TEST = os.environ['DATABASE_URL_TEST']
