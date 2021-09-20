"""
Connection library module.

Usage:
    >>> from lib.connection import CONN
    >>> CONN.get_repo('PyGithub/PyGithub')

Note that this script does not actually validate credentials or connect to
Github. If you do a request using bad credentials, you will get
a `github.BadCredentialsException` error.

According to the PyGithub script where the Github class is defined, the
global timeout is set at 15 seconds. That is already long so don't bother
extending. Also, the there is a note in the script.

Note on paging and timeout.
    The default is 30 items per page (see `DEFAULT_PER_PAGE` in the library).
    The max is 100 allowed by GitHub.

    But the max might not always be good to use. Each query will be slower, even if it takes fewer queries.

    GitHub has a 10s limit imposed on
    queries, so a few but larger queries are more likely to timeout than more
    but smaller queries.
"""
from etc import config
from github import Github

RETRY_COUNT = 3
PER_PAGE = 30

# TODO: Consider configuring the per_page argument from the default and see how
# it affects paging and rate limits.

CONN = Github(config.ACCESS_TOKEN, per_page=PER_PAGE, retry=RETRY_COUNT)
