"""
Sample teams module.
"""
from . import user
from etc import config


def main():
    from lib.connection import CONN
    o = CONN.get_organization(config.REPO_OWNER)
    teams = o.get_teams()

    for t in teams:
        print(f"Team: {t.name}")
        print("---")
        for m in t.get_members():
            user.print_details(m)
            print()
        print()


if __name__ == '__main__':
    main()
