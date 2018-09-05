"""
Sample teams module.
"""
import user
from etc import config


def print_details(team):
    print(team.id)
    print(team.name)
    details = {
        'name': team.name,
        'slug': team.slug,
        'description': team.description if team.description else "N/A",
        'repos_count': team.repos_count,
        'members_count': team.members_count
    }

    if team.repos_count:
        # .get_repos() is a generator so slice outside the list comprehension.
        details['5_repos'] = " ".join([repo.name for repo
                                       in team.get_repos()][:5]),

    for k, v in details.items():
        print("{:20}: {}".format(k, v))
    print()


def main():
    from lib.connection import CONN
    o = CONN.get_organization(config.ORGANIZATION)
    teams = o.get_teams()

    print("Summary of all teams")
    print("===")
    for t in teams:
        print_details(t)
    print()

    print("Members for configured teams")
    print("===")
    for t in teams:
        if t.name in config.TEAMS:
            print(t.name)
            print("---")
            for m in t.get_members():
                print(user.print_details(m))


if __name__ == '__main__':
    main()
