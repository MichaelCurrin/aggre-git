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
    As of 2018-05-17, Github imposes a 10s limit for completion of API requests.
    Thus, the timeout should be slightly > 10s to account for network/front-end
    latency.
"""
from github import Github

from etc import config


# TODO: Consider configuring the per_page argument from the default and see how
# it affects paging and rate limits.
CONN = Github(config.ACCESS_TOKEN)
