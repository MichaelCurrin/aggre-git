"""
Sample user module.

Gets stats for a username of a user or organization.
"""
from etc import config
from lib.connection import CONN


def print_details(user):
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

    # Orgs seems to be created, not belong to.
    counts = {
        "Repos": list(user.get_repos()),
        "Orgs": list(user.get_orgs()),
        "Events": list(user.get_events()),
        "Watched": list(user.get_watched()),
        "Starred": list(user.get_starred()),
    }
    for k, v in counts.items():
        print(f"{k:7}: {len(v):,d}")


def main():
    login = config.REPO_OWNER
    user = CONN.get_user(login)
    print_details(user)


if __name__ == "__main__":
    main()
