"""
Sample events module.
"""
import lib
from etc import config


def print_details(event):
    # Each event will have its own keys in its payload.
    # Created at is datetime but modified is a string.
    modified = lib.parse_datetime(event.last_modified)
    details = {
        'repo_full_name': event.repo.full_name,
        'repo_name': event.repo.name,
        'org': event.org.login if event.org else "N/A",
        'type': event.type,
        'data_keys': list(event.payload.keys()),
        'created_at': str(event.created_at),
        'modified_at': str(modified)
    }

    for k, v in details.items():
        print("{:14}: {}".format(k, v))
    print()


def main():
    from lib.connection import CONN

    login = config.MY_HANDLE
    user = CONN.get_user(login)

    for event in user.get_events():
        print_details(event)


if __name__ == '__main__':
    main()
