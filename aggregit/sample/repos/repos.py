"""
Sample repos module.
"""
from pprint import pprint

from lib.connection import CONN


def display_repo(repo):
    """
    Print data of interest for a given repo.
    """
    data = dict(
        name=repo.name,
        default_branch=repo.default_branch,
        full_name=repo.full_name,
        html_url=repo.html_url,
        created_at=str(repo.created_at),
        last_modified=str(repo.last_modified),
        owner=repo.owner,
        org=repo.organization,
        permissions=repo.permissions,
        private=repo.private,
        language=repo.language,
    )
    pprint(data)
    print()


def main():
    repo = CONN.get_repo('Python/CPython')
    display_repo(repo)

    repo = CONN.get_repo('MichaelCurrin/aggre-git')
    display_repo(repo)


if __name__ == '__main__':
    main()
