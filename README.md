
A server-side app for tracking details and timing for injections, labs, and
medication refills for HRT and general medications.

Development Environment Setup
=============================

Add a `.env` file in the top level directory and include the following:
```
  DATABASE_URL=postgresql:///medhead
  DATABASE_URL_TEST=postgresql:///medhead_test
  FLASK_APP=shotstuff
  SECRET_KEY=whatever-you-want
```

You'll need Python3 and PostgreSQL installed globally. Then, create a virtual environment,
activate it, and install the dependencies:

 - `python3 -m venv venv`
 - `source venv/bin/activate`
 - `pip3 install -r requirements.txt`

 - `createdb medhead`
 - `createdb medhead_test`

Install shotstuff as a Python package in the top level directory:

 - `pip install -e .`

After installing shotstuff, delete the shotstuff.egg-info/ directory:

 - `rm -rf shotstuff.egg-info/`

When you need to add dependencies to requirements.txt, don't include the
shotstuff package as a dependency. To ensure it's not added, update
requirements.txt like this:

 - `pip freeze | grep -v github.com > requirements.txt`

Seeding the Database
====================

From the top-level directory, enter ipython and run the dev_seed.py file with:

- `%run shotstuff/dev_seed.py`

Starting the App
================

If you want to run on port 5000, from the top-level directory, run:

 - `flask run`

If port 5000 is already taken by another process, run on the port of your choosing with:

 - `flask run -p [port number here]`

From here, visit `localhost:[port-number-here]/` and you can either sign up as a new user, or, if you
want to login to an account with substantial dummy date already generated, use the following credentials:

```
username: spencer
password: password
```

Running Tests
=============

Run all tests:
- `python3 -m unittest discover -v` (from highest level)

Run a specific set of tests:
- `python3 -m unittest -v` (from within a /tests directory)

Run all tests and generate a coverage report:
- `python -m coverage run -m unittest` (from highest level)
- `python -m coverage report`