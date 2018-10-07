"""
Connection library module.

Usage:
    >>> from lib.connection import CONN
    >>> CONN.get_repo('PyGithub/PyGithub')

Note that this script does not actually validate credentials or connect to
Github. If you do a request using bad credentials, you will get
a `github.BadCredentialsException` error.
"""
from github import Github

from etc import config

# TODO: Consider configuring the per_page argument from the default and see how
# it affects paging and rate limits.
CONN = Github(config.ACCESS_TOKEN)
