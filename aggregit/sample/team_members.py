"""
Sample team members module.
"""
from github import GithubException

from etc import config
from lib.connection import CONN


def print_details(team):
    details = {
        'id': team.id,
        'name': team.name,
        'slug': team.slug,
        'description': team.description if team.description else "N/A",
        'repos_count': team.repos_count,
        'members_count': team.members_count
    }

    if team.repos_count:
        # .get_repos() is a generator so slice outside the list comprehension.
        details['5_repos'] = [repo.name for repo in team.get_repos()][:5]

    for k, v in details.items():
        print(f"{k:20}: {v}")
    print()


def main():
    o = CONN.get_organization(config.REPO_OWNER)
    try:
        for t in o.get_teams():
            print_details(t)
        print()
    except GithubException:
        print(f"Unable to access teams for org: {config.REPO_OWNER}")


if __name__ == '__main__':
    main()
