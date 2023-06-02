## Running tests

Run all tests:
- python3 -m unittest discover -v (from highest level)

Run a specific set of tests:
- python3 -m unittest -v (from within a /tests directory)

Run all tests and generate a coverage report:
- python -m coverage run -m unittest (from highest level)
- python -m coverage report