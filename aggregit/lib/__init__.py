"""
Initliazation file for library module.
"""
import csv
import datetime
import re
from textwrap import shorten
from email.utils import mktime_tz, parsedate_tz

import github
from github import UnknownObjectException

from .connection import CONN
from etc import config


# Match a ticket number like "ABC-123".
JIRA_TICKET_PATTERN = re.compile(r"[A-Z]+-\d+")
# Match a URL like "https://jira.myorg.com/browse/ABC-123", where domain could
# optionally include organization's name. Extract just the ticket portion.
JIRA_URL_PATTERN = re.compile(r"https:\/\/jira.+/browse/([A-Z]+-\d+)")


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

    :return: User's name if available otherwise handle.
    """
    if user:
        if user.name:
            return user.name
        else:
            return f"@{user.login}"

    return "<NOT USER>"


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


def get_repos():
    """
    Get repos to report on using configured details.

    :return repos: A list of Github Repository objects. If getting all repos
        for a user, this is a paginated list (requests are not made yet),
        otherwise if getting repos by repo paths then each objects contains
        data from a completed request.
    """
    if config.BY_OWNER:
        try:
            user = CONN.get_organization(config.REPO_OWNER)
            print(f"Fetched org: {config.REPO_OWNER}")
        except UnknownObjectException:
            user = CONN.get_user(config.REPO_OWNER)
            print(f"Fetched user: {config.REPO_OWNER}")

        # This is a paginated list, so we do not get all repos upfront.
        repos = user.get_repos()
    else:
        repos = []
        for repo_path in config.REPO_PATHS:
            print(f"Fetching repo: {repo_path}")
            try:
                # Get all repos upfront so bad config will cause early failure.
                repo = CONN.get_repo(repo_path, lazy=False)
            except UnknownObjectException:
                raise ValueError(f"Bad repo path: {repo_path}")
            repos.append(repo)
    print()

    return repos


def write_csv(path, header, data):
    """
    Write rows to a CSV.

    :param str path: Write file to this path, overwriting existing any file.
    :param tuple header: Column names.
    :param data: Rows of data to write, where each row is dict that has
        keys matching the header.

    :return: None
    """
    print(f"Writing to {path}")
    with open(path, 'w') as f_out:
        writer = csv.DictWriter(f_out, fieldnames=header,
                                quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()
        writer.writerows(data)


def extract_jira_ticket(text):
    """
    Extract Jira ticket ID if one can be found.

    :param text: Text to search, such as a PR description. Expect it to contain
        a Jira URL otherwise fallback to checking for a plain ticket number.

    :return: The first Jira ticket ID if found e.g. "ABC-123". Or, None
        if no match.

    >>> extract_jira_ticket("https://jira.com/browse/ABC-123")
    'ABC-123'

    >>> extract_jira_ticket("https://jira.myorg.com/browse/DEF-12")
    'DEF-12'

    >>> extract_jira_ticket("XYZ-4001")
    'XYZ-4001'

    >>> extract_jira_ticket("See ticket XYZ-4001, kind regards.")
    'XYZ-4001'

    >>> extract_jira_ticket("abc")

    >>> extract_jira_ticket("123-ABC")

    >>> extract_jira_ticket("https://jira.com/browse/abc-123")

    """
    match = JIRA_URL_PATTERN.search(text)

    if match:
        return match.group(1)

    match = JIRA_TICKET_PATTERN.search(text)

    if match:
        return match.group()

    return None


if __name__ == '__main__':
    # Test with python -m lib.__init__
    import doctest
    doctest.testmod()
