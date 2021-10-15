"""
Search issues module.

Handle a search for Issues and Pull Requests.
"""
import collections
import pprint

from lib.connection import CONN

# Merged Pull Requests created by MichaelCurrin in public repos of other users.
username = "MichaelCurrin"
SEARCH_QUERY = (
    f"is:pr is:merged author:{username} -user:{username} -user:2uinc sort:created-desc"
)


def extract(issue):
    """
    Process a fetched issue and return as a dict of useful fields.
    """
    details = {
        "title": issue.title,
        "url": issue.html_url,
        "repo": issue.repository.name,
        "state": issue.state,
        "created_at": issue.created_at,
    }

    if issue.state == "closed":
        details["closed_at"] = issue.closed_at

    return details


def group_by_month(issues):
    """
    They won't all be merged always so safer to group by created at date.
    """
    counter = collections.Counter()

    for issue in issues:
        date = issue["created_at"]
        key = (date.year, date.month)
        counter.update([key])

    return counter


def display(issues_resp):
    """
    Print report of issues data.
    """
    total = issues_resp.totalCount

    print("Total")
    print(total)

    issues = [extract(issue) for issue in issues_resp]

    max_groups = 7

    print(f"By month - {max_groups} months")
    groups = group_by_month(issues)

    print("Month   | PRs")
    print("---     | ---")
    for i, (k, count) in enumerate(groups.items()):
        y, m = k
        print(f"{y}-{m:02d} | {count:3d}")
        if i + 1 == max_groups:
            break

    limit = 3
    print(f"Detailed - {limit} items")
    for issue in issues[:limit]:
        pprint.pprint(issue)


def main():
    """
    Main command-line entry-point.

    If this is too long or slow, use `issues_resp[:5]` for example.
    """
    print(f"Search query:")
    print(f"    {SEARCH_QUERY}")

    issues_resp = CONN.search_issues(SEARCH_QUERY)
    display(issues_resp)


if __name__ == "__main__":
    main()
