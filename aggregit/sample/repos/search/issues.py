"""
Search issues module.

Handle a search for Issues and Pull Requests.
"""
import collections
import pprint

import github.Issue
from etc import config
from lib.connection import CONN

# Open soure contributions - merged Pull Requests created by the user, in
# public repos of other users. Public filter is used here in case using a token
# with private access. Using `-is:private` gave inconsisent results.
SEARCH_QUERY = (
    f"is:pr is:merged is:public"
    f" author:{config.REPO_OWNER} -user:{config.REPO_OWNER} sort:created-desc "
)


def extract(issue: github.Issue) -> dict:
    """
    Process a fetched issue and return as a dict of useful fields.
    """
    return {
        "title": issue.title,
        "url": issue.html_url,
        "repo": issue.repository.name,
        "state": issue.state,
        "created_at": issue.created_at,
        "closed_at": issue.closed_at if issue.state == "closed" else None,
    }


def group_by_month(issues) -> collections.Counter():
    """
    They won't all be merged always so safer to group by created at date.

    Expects `PaginatedList[Issue]`, except that is not valid as a type even when
    using `github.PaginatedList.PaginatedList`.
    """
    counter = collections.Counter()

    for issue in issues:
        date = issue["created_at"]
        key = (date.year, date.month)
        counter.update([key])

    return counter


def display(issues_resp, max_groups=7, max_items=3) -> None:
    """
    Print report of issues data.
    """
    total = issues_resp.totalCount

    print("Total")
    print(total)

    issues = [extract(issue) for issue in issues_resp]

    print(f"By month view - {max_groups} months")
    groups = group_by_month(issues)

    print("Month   | PRs")
    print("---     | ---")
    for i, (k, count) in enumerate(groups.items()):
        y, m = k
        print(f"{y}-{m:02d} | {count:3d}")

        if i + 1 == max_groups:
            break
    print()

    print(f"Detailed view - {limit} items")
    for issue in issues[:limit]:
        pprint.pprint(issue)


def main():
    """
    Command-line entry-point.
    """
    print(f"Search query:")
    print(f"    {SEARCH_QUERY}")

    issues_resp = CONN.search_issues(SEARCH_QUERY)
    display(issues_resp)


if __name__ == "__main__":
    main()
