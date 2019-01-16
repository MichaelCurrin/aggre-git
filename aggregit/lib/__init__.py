"""
Initliazation file for library module.
"""
import datetime
from textwrap import shorten
from email.utils import mktime_tz, parsedate_tz

import github


def parse_datetime(standard_datetime):
    """
    Parse a standardised datetime string to a datetime object.

    :param standard_datetime: datetime value as a string .
        e.g. 'Thu, 30 Aug 2018 13:14:09 GMT'

    :return: datetime object in UTC time. Printing this out will reflect
        in the system's timezone. e.g. entering time 12:00 for +0000 timezone
        shows as 14:00 if printing in a system set to +0200 timezone,
        whether doing str(obj) or str(obj.hour).
    """
    time_tuple = parsedate_tz(standard_datetime)
    timestamp = mktime_tz(time_tuple)

    return datetime.datetime.fromtimestamp(timestamp)


def display(user: github.NamedUser.NamedUser):
    """
    Return an easy to read reference for a Github user account.

    :return: Return user's name if set, otherwise user's login
        including an '@' prefix to show that it is a username.
    """
    if user.name:
        return user.name
    else:
        return f"@{user.login}"


def truncate(text, limit):
    """
    Format text for easy reading on a single line.

    Newline characters are replaced  and if the text has to be shortened
    then an ellipsis will be added at the end.

    :param text: Text to format.
    :param limit: Number of characters to limit to.

    :return: Formatted message.
    """
    return shorten(text.replace("\n", "  "), limit)
