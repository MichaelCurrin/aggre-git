"""
Pull Request report script.

Get all Pull Requests and print out summary data.

Requires either a configured repo owner (as user or organization) to retrieve
repos for, otherwise the paths for required repos.
Also requires configured usernames, such that only PRs created by these users
are included.

A commit doesn't have to have an author - if blank assume it was by the PR
author as it probably was.
"""
from etc import config
from lib.connection import CONN


if config.BY_OWNER:
    user = CONN.get_user(config.REPO_OWNER)
    repos = user.get_repos()
else:
    # TODO: Consider whether lazy=False affects memory and total time,
    # since it is useful for checking paths are valid up front. Unless
    # this can be checked another way which requires requests but then ignores
    # the objects.
    repos = [CONN.get_repo(repo_path) for repo_path in config.REPO_PATHS]

for repo in repos:
    print(repo.name)
    for pr in repo.get_pulls(state=config.PR_STATE):
        author = pr.user
        print(author.login)
        for commit in pr.get_commits():
            print(commit)
