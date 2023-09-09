Development Environment Setup
=============================

Add a `.env` file in the top level directory and include the following:
```
  DATABASE_URL=postgresql:///medhead
  DATABASE_URL_TEST=postgresql:///medhead_test
  FLASK_APP=shotstuff
  SECRET_KEY=whatever-you-want
```

You'll need Python3 and PostgreSQL:

  `python3 -m venv venv`
  `source venv/bin/activate`
  `pip3 install -r requirements.txt`

  `createdb medhead`
  `createdb medhead_test`

Install shotstuff as a python package in the top level directory:

  `pip install -e .`

After installing shotstuff, delete the shotstuff.egg-info/ directory:

  `rm -rf shotstuff.egg-info/`

When you need to add dependencies to requirements.txt, don't include the
shotstuff package as a dependency. To ensure it's not added, update
requirements.txt like this:

  `pip freeze | grep -v github.com > requirements.txt`

Running Tests
=============

Run all tests:
- python3 -m unittest discover -v (from highest level)

Run a specific set of tests:
- python3 -m unittest -v (from within a /tests directory)

Run all tests and generate a coverage report:
- python -m coverage run -m unittest (from highest level)
- python -m coverage report