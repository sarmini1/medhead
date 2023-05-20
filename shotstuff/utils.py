from datetime import datetime
from dateutil.relativedelta import relativedelta

def calculate_date(start_date=datetime.utcnow(), months_in_future=0):
    """
    Given a start date and an optional amount of time in the future
    """

    full_time = start_date + relativedelta(months=months_in_future)
    future_date = full_time.strftime("%Y-%m-%d")
    return future_date