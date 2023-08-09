import calendar
from pytz import timezone
from datetime import datetime
from dateutil.relativedelta import relativedelta


def convert_date_to_pst(date):
    """
    Converts datetime object to pacific datetime object.
    """
    aware = timezone('UTC').localize(date)
    pacific_tz = timezone("US/Pacific")
    pacific_date = aware.astimezone(pacific_tz)

    return pacific_date

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

# NOTE: leftover test from treatment models tests:

#     @freeze_time("2023-05-26 10:30:01")
    # def test_generate_friendly_date_time(self):
    #     """Test that a treatment instance can give back helpful time data."""

    #     t2 = TreatmentFactory()
    #     generated = t2.generate_friendly_date_time(datetime.datetime.now())

    #     self.assertEqual(
    #         generated,
    #         {
    #             'year': '2023',
    #             'month': '05',
    #             'day': '26',
    #             'time': '10:30:01',
    #             "date": "05/26/2023",
    #             'weekday': 'Friday',
    #             'full_date_time': '05/26/2023, 10:30:01'
    #         }
    #     )