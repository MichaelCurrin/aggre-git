"""
Sample user module.
"""
from etc import config
from lib.connection import CONN


def print_details(user):
    details = {
        'Username': user.login,
        'Email': user.email,
        'Name': user.name,
        'Location': user.location,
        'Company': user.company,
        'Created At': str(user.created_at.date()),
    }
    for k, v in details.items():
        print("{}: {}".format(k, v))
        print()


def main():
    login = config.MY_HANDLE
    user = CONN.get_user(login)
    print_details(user)


if __name__ == '__main__':
    main()