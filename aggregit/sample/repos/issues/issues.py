"""
Sample repo issues module.
"""
import pprint

from etc import config
from lib.connection import CONN


def extract(issue):
    labels = [label.name for label in issue.labels]
    details = {
        "number": issue.number,
        "title": issue.title,
        "repo": issue.repository.name,
        "created_at": issue.created_at,
        "updated_at": issue.updated_at,
        "url": issue.html_url,
        "state": issue.state,
        "labels": labels,
        "comment_count": issue.comments,
        "assignee": issue.assignee,
        "assignees": issue.assignees,
    }

    if issue.state == "closed":
        details["closed_at"] = issue.closed_at
        details["closed_by"] = issue.close_by.login

    if issue.comments:
        comments = [
            {"username": comment.user.login, "date": str(comment.created_at.date())}
            for comment in issue.get_comments()
        ]
        details["comments"] = comments

    reactions_resp = list(issue.get_reactions())
    if reactions_resp:
        reactions = [
            {"username": reaction.user.login, "date": str(reaction.created_at.date())}
            for reaction in reactions_resp
        ]
        details["reactions"] = reactions

    return details


def main():
    for repo_name in config.REPO_PATHS:
        repo = CONN.get_repo(repo_name)
        issues = repo.get_issues()

        for issue in issues:
            issue_data = extract(issue)
            pprint.pprint(issue_data)
        print()
    print("===========")


if __name__ == "__main__":
    main()
