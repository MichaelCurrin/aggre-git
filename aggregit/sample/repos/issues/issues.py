"""
Sample repo issues module.
"""
import pprint

from etc import config
from lib.connection import CONN


def extract(issue):
    details = {
        'number': issue.number,
        'title': issue.title,
        'comment_count': issue.comments,
        'state': issue.state,
        'repo': issue.repository.name,
        'labels': [label.name for label in issue.labels],
        'assignee': issue.assignee,
        'assignees': issue.assignees
    }
    if issue.state == 'closed':
        details['closed_at'] = issue.closed_at
        details['closed_by'] = issue.close_by.login

    if issue.comments:
        details['comments'] = [
            {'username': comment.user.login,
             'date': str(comment.created_at.date())}
            for comment in issue.get_comments()
        ]

    reactions = list(issue.get_reactions())
    if reactions:
        details['reactions'] = [
            {'username': reaction.user.login,
             'date': str(reaction.created_at.date())}
            for reaction in reactions
        ]

    return details


def main():
    for repo_name in config.REPOS:
        repo = CONN.get_repo(repo_name)
        for issue in repo.get_issues():
            data = extract(issue)
            pprint.pprint(data)
        print()
    print("===========")


if __name__ == '__main__':
    main()

