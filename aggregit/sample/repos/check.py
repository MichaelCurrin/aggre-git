"""
Sample check repos module.
"""
from github import UnknownObjectException

from etc import config
from lib.connection import CONN


def repos_exist(repo_names):
    for repo_name in repo_names:
        print(repo_name, end=" ")
        try:
            CONN.get_repo(repo_name, lazy=False)
            print("OK")
        except UnknownObjectException as e:
            print("ERROR")


def main():
    repos_exist(config.REPOS)


if __name__ == '__main__':
    main()
