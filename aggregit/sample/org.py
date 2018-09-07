"""
Sample organization module.
"""
from etc import config


def print_details(org):
    events = list(org.get_events())
    members = list(org.get_members())
    issues = list(org.get_issues())
    repos = list(org.get_repos())

    print("Name: {}".format(org.name))
    print("Events: {}".format(len(events)))
    print("Members: {}".format(len(members)))
    print("Issues: {}".format(len(issues)))
    print("Repos: {}".format(len(repos)))


def main():
    from lib.connection import CONN
    org = CONN.get_organization(config.ORGANIZATION)
    print_details(org)


if __name__ == '__main__':
    main()
