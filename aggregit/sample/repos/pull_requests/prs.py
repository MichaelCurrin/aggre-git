"""
Sample pull requests module.

Repos notes:
    https://pygithub.readthedocs.io/en/latest/github_objects/Repository.html

    Repository.get_pulls(state=NotSet, sort=NotSet, direction=NotSet,
                         base=NotSet, head=NotSet)
        state
            string Either open, closed, or all to filter by state.
                   Default: open
        sort
            string What to sort results by. Can be either created, updated,
            popularity (comment count) or long-running (age, filtering by
            pulls updated in the last month). Default: created

        direction
            string The direction of the sort. Can be either asc or desc.
            Default: desc when sort is created or sort is not specified,
            otherwise asc.

        If a PR is closed, it could be merged or not merged.
        See PullRequest.merged or .merged() and then merged_at and merged_by.

Pull Request notes:
    https://pygithub.readthedocs.io/en/latest/github_objects/PullRequest.html

    Pull Request review comments are comments on a portion of the unified diff.
    These are separate from Commit Comments (which are applied directly to a
    commit, outside of the Pull Request view), and Issue Comments (which do not
    reference a portion of the unified diff).
"""
import pprint
import re

from etc import config
from lib.connection import CONN


# Look for Jira ticket (i,e, issue) URL, if any, and take ticket ID.
# There is one group and the whole pattern is not repeated, so there can be
# at most one group in the results.
# Expect jira.com or jira.my_org.com as domains.
JIRA_PATTERN = re.compile(r"https:\/\/jira.+/browse/([A-Z]+-\d+)")


def report(pr):
    print('User')
    user = {
        'username': pr.user.login,
        'assignee': pr.assignee.login if pr.assignee else None,
        'assignees': [u.login for u in pr.assignees],
    }
    pprint.pprint(user)
    print()

    print('data')
    body = pr.body.replace("\r\n", "\n")
    match = JIRA_PATTERN.search(body)
    jira_ticket = match.group(1) if match else None

    data = {
        'state': pr.state,
        'title': pr.title,
        'description': body,
        'jira_ticket': jira_ticket,
        'additions': pr.additions,
        'deletions': pr.deletions,
        'created_at': str(pr.created_at.date()),
        'comments': pr.comments,
    }
    if pr.closed_at:
        data['closed_at'] = str(pr.closed_at.date())
    if pr.merged:
        data['merge_by'] = pr.merged_by.login
        data['merged_at'] = str(pr.merged_at.date())
    pprint.pprint(data)
    print()

    print('counts')
    counts = {
        'issue_comments': len(list(pr.get_issue_comments())),
        'review_comments': len(list(pr.get_review_comments())),
        'reviews': len(list(pr.get_reviews())),
    }
    print(counts)
    print()

    print('review requests')
    # Tuple of users and teams.
    users, teams = pr.get_review_requests()
    usernames = [u.login for u in users]
    teamnames = [t.name for t in teams]
    if usernames:
        pprint.pprint(usernames)
        pprint.pprint(teamnames)


def main():
    repos = [CONN.get_repo(repo_name) for repo_name in config.REPO_PATHS]

    for repo in repos:
        print(f"### REPO: {repo.name} ###")
        print()

        for pr in repo.get_pulls():
            if pr.number == 595:
                report(pr)
                print("---")
        print()


if __name__ == '__main__':
    main()
