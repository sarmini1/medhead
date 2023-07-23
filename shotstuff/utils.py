from datetime import datetime
import calendar
from dateutil.relativedelta import relativedelta

def calculate_date(start_date=datetime.utcnow(), months_in_future=0):
    """
    Given a start date and an optional amount of time in the future
    """

    full_time = start_date + relativedelta(months=months_in_future)
    future_date = full_time.strftime("%Y-%m-%d")
    return future_date


def generate_friendly_date_time(date):
        """ Returns dictionary with year, month, day, time, date and time formatted
            in a friendly way.
        """

        year = date.strftime("%Y")
        month = date.strftime("%m")
        day = date.strftime("%d")
        time = date.strftime("%H:%M:%S")
        formatted_date = date.strftime("%m/%d/%Y")
        full_date_time = date.strftime("%m/%d/%Y, %H:%M:%S")

        # Note: this version of this method now has date in the return, whereas
        # others don't-- seriously need to break this out next time I work on this
        return {
            "year": year,
            "month": month,
            "day": day,
            "time": time,
            "date": formatted_date,
            "weekday": calendar.day_name[date.weekday()],
            "full_date_time": full_date_time
        }