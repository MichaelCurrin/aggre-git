"""
Initliazation for library module.
"""
import datetime
from email.utils import mktime_tz, parsedate_tz


def parse_commit_date(commit_datetime):
    """
    Parse commit time string to a datetime object.

    @param commit_datetime: datetime value as a string .
        e.g. 'Thu, 30 Aug 2018 13:14:09 GMT'

    @return: datetime object in UTC time. Printing this out will reflect
        in the system's timezone.
        e.g. entering time 12:00 for +0000 timezone will show as 14:00 if
        printing in a system set to +0200 timezone, whether doing str(obj) or
        str(obj.hour).
    """
    time_tuple = parsedate_tz(commit_datetime)
    timestamp = mktime_tz(time_tuple)

    return datetime.datetime.fromtimestamp(timestamp)
