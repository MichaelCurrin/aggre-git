"""
Validate objects library module.

Usage:
    $ python -m lib.validate_objects

    OR
    >>> from lib.validate_objects import validate_config
    >>> validate_config()

Validate some values in the config details by request the objects from
the API. This is useful to do upfront to fail early when getting details
for several objects as part of a report.

Note that there are CONN.get_repos() and CONN.get_users() methods but they
only take a `since` parameter and appear to return *all* objects on Github
without filtering.
"""
from github import UnknownObjectException

from etc import config
from lib.connection import CONN


def check_repo(repo_path):
    """
    Request a Gitub repo by path and raise an error if it cannot be retrieved.

    The lazy parameter must be used when retrieving repos in order
    to fail immediately. This parameter does not exist for `.get_users()`.

    @param repo_path: str in the format "some_user/some_repo_name".

    @return: None
    @raises: ValueError
    """
    print(repo_path, end=" ")
    try:
        CONN.get_repo(repo_path, lazy=False)
        print("OK")
    except UnknownObjectException as e:
        print()
        raise ValueError("Could not find repo: {}".format(repo_path))


def check_user(username):
    """
    Request a username on Github raise an error if it cannot be retrieved.

    @param username: str

    @return: None
    @raises: ValueError
    """
    print(username, end=" ")
    try:
        CONN.get_user(username)
        print("OK")
    except UnknownObjectException as e:
        print()
        raise ValueError("Could not find username: {}".format(username))


def validate_config():
    """
    Request configured repos and users and raise errors if they do not exist.

    @return: None
    @raises: ValueError, AssertionError
    """
    print("REPOS")
    if config.BY_OWNER:
        assert config.REPO_OWNER, "REPO_OWNER value must be set in config."
        check_user(config.REPO_OWNER)
    else:
        assert config.REPO_PATHS, "REPO_PATHS value must be set in config."
        for repo_path in config.REPO_PATHS:
            check_repo(repo_path)

    print("\nUSERS")
    assert config.USERNAMES, "USERNAMES value must be set in config."
    for username in config.USERNAMES:
        check_user(username)


if __name__ == '__main__':
    validate_config()
