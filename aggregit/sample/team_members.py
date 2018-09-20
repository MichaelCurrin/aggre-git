"""
Sample team members module.
"""
from etc import config


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
        print("{:20}: {}".format(k, v))
    print()


def main():
    from lib.connection import CONN
    o = CONN.get_organization(config.REPO_OWNER)
    teams = o.get_teams()

    for t in teams:
        print_details(t)
    print()


if __name__ == '__main__':
    main()
