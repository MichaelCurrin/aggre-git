"""
Sample organization module.

Get stats for an organization on GitHub.

For a list of open source repos by organizations on GitHub, see:
    https://github.com/collections/open-source-organizations
"""
from etc import config
from github import GithubException, UnknownObjectException
from lib.connection import CONN


def extract(org):
    events = len(list(org.get_events()))
    members = len(list(org.get_members()))
    repos = len(list(org.get_repos()))

    try:
        issues = len(list(org.get_issues()))
    except UnknownObjectException as e:
        # This occurred on the 'twitter' org and may occur on others.
        issues = f"UnknownObjectException: {str(e)}"

    try:
        teams = len(list(org.get_teams()))
    except GithubException as e:
        # May get an access error.
        teams = f"GithubException: {str(e)}"

    details = dict(
        name=org.name,
        login=org.login,
        events=events,
        members=members,
        repos=repos,
        private_repos=org.total_private_repos,
        issues=issues,
        teams=teams,
    )

    return details


def main():
    org = CONN.get_organization(config.REPO_OWNER)
    details = extract(org)
    print(details)


if __name__ == "__main__":
    main()
