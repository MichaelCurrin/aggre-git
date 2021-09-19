"""
Sample user module.

Get stats for a configured GitHub profile.
"""
from etc import config
from lib.connection import CONN


def print_profile_details(user):
    details = {
        "Username": f"@{user.login}",
        "Email": user.email if user.email else "N/A",
        "Name": user.name if user.name else "N/A",
        "Location": user.location if user.location else "N/A",
        "Company": user.company if user.company else "N/A",
        "Created At": str(user.created_at.date()),
    }

    for k, v in details.items():
        print(f"{k:20}: {v}")


def print_counts(user):
    # Orgs seems to be created, not belong to.
    counts = {
        "Repos": user.get_repos,
        "Orgs": user.get_orgs,
        "Events": user.get_events,
        "Watched": user.get_watched,
        "Starred": user.get_starred,
    }

    for k, v in counts.items():
        result = list(v())
        print(f"{k:7}: {len(result):,d}")
        print("")


def main():
    """
    Main command-line entry-point.
    """
    login = config.REPO_OWNER
    user = CONN.get_user(login)

    print("Profile details")
    print_profile_details(user)

    print("Counts")
    print_counts(user)


if __name__ == "__main__":
    main()
