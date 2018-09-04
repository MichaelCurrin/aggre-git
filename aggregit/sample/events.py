"""
Sample events module.
"""
from etc import config
from lib.connection import CONN


def print_details(event):
    details = {
        'repo': event.repo.name,
        'org': event.org.login if event.org else None,
        'type': event.type,
        'data_keys': list(event.payload.keys())
    }

    for k, v in details.items():
        print("{}: {}".format(k, v))


def main():
    login = config.MY_HANDLE
    user = CONN.get_user(login)
    for event in user.get_events()[:10]:
        print_details(event)
        print()


if __name__ == '__main__':
    main()
