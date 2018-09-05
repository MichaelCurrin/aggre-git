"""
Sample events module.
"""
from etc import config


def print_details(event):
    details = {
        'repo_full_name': event.repo.full_name,
        'repo_name': event.repo.name,
        'org': event.org.login if event.org else "N/A",
        'type': event.type,
        'data_keys': " ".join(list(event.payload.keys()))
    }

    for k, v in details.items():
        print("{:20}: {}".format(k, v))
    print()


def main():
    from lib.connection import CONN

    login = config.MY_HANDLE
    user = CONN.get_user(login)
    # Due to apparent bug, the repo will be name shown for a single event
    # but within a for loop the full_name is used instead.
    for event in user.get_events():
        print_details(event)


if __name__ == '__main__':
    main()
