"""
Search issues module.

Handle a search for Issues and Pull Requests.
"""
import collections
import pprint

from etc import config
from lib.connection import CONN

# TODO: Replace
q = "is:pr is:closed author:MichaelCurrin archived:false org:MichaelCurrin"


def extract(issue):
    """
    Process the issue.
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


def main():
    """
    Main command-line entry-point.

    If this is too long or slow, use `issues_resp[:5]` for example.
    """
    issues_resp = CONN.search_issues(q)

    total = issues_resp.totalCount

    print("Total")
    print(total)

    issues = [extract(issue) for issue in issues_resp]

    print("By month")
    groups = group_by_month(issues)
    for k, count in groups.items():
        y, m = k
        print(f"{y}-{m}: {count}")

    print("Detailed")
    for issue in issues:
        pprint.pprint(issue)


if __name__ == "__main__":
    main()
