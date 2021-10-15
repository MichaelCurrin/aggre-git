"""
Sample teams module.
"""
from etc import config
from github import UnknownObjectException
from lib.connection import CONN
from sample import user


def main():
    try:
        o = CONN.get_organization(config.REPO_OWNER)
    except UnknownObjectException:
        msg = (
            f"Could not find organization: {config.REPO_OWNER}."
            f" Did you provide a user by accident?"
        )
        raise ValueError(msg)

    teams = list(o.get_teams())

    print(f"Teams: {len(teams)}\n")

    for t in teams:
        print(f"Team: {t.name}")
        print("---")

        for m in t.get_members():
            user.print_details(m)
            print()
        print()


if __name__ == "__main__":
    main()
