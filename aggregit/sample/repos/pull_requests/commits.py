"""
Sample pull request commits module.

Get all commits for configured repos.
"""
import pprint

from etc import config
import lib
from lib.connection import CONN


def extract(commit):
    date = lib.parse_datetime(commit.stats.last_modified).date()

    return dict(
        author=commit.author.login if commit.author else "N/A",
        SHA=commit.sha,
        last_modified=str(date),
        additions=commit.stats.additions,
        deletions=commit.stats.deletions,
        total=commit.stats.total
    )


def main():
    repos = [CONN.get_repo(repo_name) for repo_name in config.REPO_PATHS]

    for repo in repos:
        print(repo.name)
        for commit in repo.get_commits():
            data = extract(commit)
            pprint.pprint(data)
            print()
        print()


if __name__ == '__main__':
    main()
