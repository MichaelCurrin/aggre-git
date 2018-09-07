"""
Sample teams module.
"""
import user
from etc import config


def main():
    from lib.connection import CONN
    o = CONN.get_organization(config.ORGANIZATION)
    teams = o.get_teams()

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
