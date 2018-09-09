"""
Library connection module.

Usage:
    >>> from lib.connection import CONN
    >>> CONN.get_repo('PyGithub/PyGithub')

Note that this script does not actually validate credentials or connect to
Github. If you do a request using bad credentials, you will get
a `github.BadCredentialsException` error.
"""
from github import Github

from etc import config


CONN = Github(config.ACCESS_TOKEN)
