"""
Sample user module.
"""
from etc import config
from lib.connection import CONN


def print_details(user):
    details = {
        'Username': "@{}".format(user.login),
        'Email': user.email if user.email else "N/A",
        'Name': user.name if user.name else "N/A",
        'Location': user.location if user.location else "N/A",
        'Company': user.company if user.company else "N/A",
        'Created At': str(user.created_at.date()),
    }
    for k, v in details.items():
        print("{:20}: {}".format(k, v))

    # Orgs seems to be created, not belong to.
    counts = {
        'Repos': list(user.get_repos()),
        'Orgs': list(user.get_orgs()),
        'Events': list(user.get_events()),
        'Watched': list(user.get_watched()),
        'Starred': list(user.get_starred()),
    }
    for k, v in counts.items():
        print("{:7}: {:,d}".format(k, len(v)))


def main():
    login = config.REPO_OWNER
    user = CONN.get_user(login)
    print_details(user)


if __name__ == '__main__':
    main()
