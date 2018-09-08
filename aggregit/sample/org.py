"""
Sample organization module.
"""
from etc import config


def extract(org):
    details = dict(
        name=org.name,
        login=org.login,
        events=len(list(org.get_events())),
        members=len(list(org.get_members())),
        issues=len(list(org.get_issues())),
        repos=len(list(org.get_repos())),
        teams=len(list(org.get_teams()))
    )

    return details


def main():
    from lib.connection import CONN
    org = CONN.get_organization(config.ORGANIZATION)
    details = extract(org)
    print(details)


if __name__ == '__main__':
    main()
