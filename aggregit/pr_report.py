"""
Pull Request report script.

Get all Pull Requests and print out summary data.

Requires either a configured repo owner (as user or organization) to retrieve
repos for, otherwise the paths for required repos.
Also requires configured usernames, such that only PRs created by these users
are included.

A commit doesn't have to have an author - if blank assume it was by the PR
author as it probably was.
"""
import csv

from etc import config
import lib
from lib.connection import CONN
from models import PullRequest

out_data = []

if config.BY_OWNER:
    user = CONN.get_user(config.REPO_OWNER)
    repos = user.get_repos()
else:
    # TODO: Consider whether lazy=False affects memory and total time,
    # since it is useful for checking paths are valid up front. Unless
    # this can be checked another way which requires requests but then ignores
    # the objects.
    repos = [CONN.get_repo(repo_path) for repo_path in config.REPO_PATHS]

for repo in repos:
    print(f"REPO: {repo.name}")
    for pr in repo.get_pulls(state=config.PR_STATE):
        author = pr.user

        if author.login in config.USERNAMES:
            print(f"PR #{pr.number}")
            pr_data = PullRequest(pr)
            out_row = {
                'repo_url': repo.html_url,
                'repo_owner': lib.display(repo.owner),
                'repo': repo.name,

                'author': lib.display(author),
                'assignees': ", ".join(pr_data.assignee_names()),

                'no': pr_data.number,
                'title': pr_data.title,

                'created_at': str(pr_data.created_at),
                'updated_at': str(pr_data.updated_at),

                'status': pr_data.status,

                'status_changed_at': pr_data.status_changed_at(),
                'merged_by': pr_data.merged_by_name(),

                'reviewers': ", ".join(pr_data.reviewer_names()),
                'reviews': ", ".join(pr_data.review_summary()),

                'comments': pr_data.comment_count,
                'commits': pr_data.commit_count,
                'changed_files': pr_data.changed_files,
                'added_lines': pr_data.additions,
                'deleted_lines': pr_data.deletions,
            }
            out_data.append(out_row)

header = (
    'repo_url', 'repo_owner', 'repo',
    'author', 'assignees',
    'no', 'title',
    'status', 'status_changed_at', 'updated_at', 'created_at',
    'commits', 'changed_files', 'added_lines', 'deleted_lines',
    'comments', 'merged_by', 'reviewers', 'reviews',
)
with open(config.PR_CSV_PATH, 'w') as f_out:
    writer = csv.DictWriter(f_out, fieldnames=header)
    writer.writeheader()
    writer.writerows(out_data)
