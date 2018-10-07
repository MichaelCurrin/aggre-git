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
        author_login = pr.user.login

        if author_login in config.USERNAMES:
            print(f"PR #{pr.number}")
            pr_data = PullRequest(pr)

            out_row = {
                'owner': repo.owner.login,
                'repo': repo.name,
                'pr_author': author_login,
                'pr_assignees': ", ".join(pr_data.assignee_logins()),
                'pr_date': str(pr_data.created_at),
                'pr_no': pr_data.number,
                'pr_title': pr_data.title,
                'pr_status': pr_data.status
            }
            out_data.append(out_row)

header = ('owner', 'repo', 'pr_author', 'pr_assignees', 'pr_date', 'pr_no',
          'pr_title', 'pr_status')
with open(config.PR_CSV_PATH, 'w') as f_out:
    writer = csv.DictWriter(f_out, fieldnames=header)
    writer.writeheader()
    writer.writerows(out_data)
