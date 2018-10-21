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


def main():
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
                try:
                    pr_data = PullRequest(pr)
                    out_row = {
                        'Repo URL': repo.html_url,
                        'Repo Owner': lib.display(repo.owner),
                        'Repo Name': repo.name,

                        'Author': lib.display(author),
                        'PR ID': f"#{pr_data.number}",
                        'PR Title': pr_data.title,
                        'PR URL': pr_data.url,

                        'Created At': pr_data.created_at,
                        'Updated At': pr_data.updated_at,

                        'Status': pr_data.status,

                        'Status Changed At': pr_data.status_changed_at(),
                        'Merged By': pr_data.merged_by_name(),

                        'Reviewers': ", ".join(pr_data.reviewer_names()),
                        'Reviews': ", ".join(pr_data.review_summary()),

                        'Comments': pr_data.comment_count,
                        'Commits': pr_data.commit_count,
                        'Changed Files': pr_data.changed_files,
                        'Added Lines': pr_data.additions,
                        'Deleted Lines': pr_data.deletions,
                        'Changed Lines': pr_data.additions + pr.deletions,
                    }
                    out_data.append(out_row)
                except Exception as e:
                    # Keep the report generation robust by logging and skipping over
                    # any errors.
                    print(f"Could not fetch or parse PR."
                          f" {type(e).__name__}: {str(e)}")

    header = (
        'Repo Owner', 'Repo Name', 'Repo URL',
        'PR ID', 'PR Title', 'Author', 'PR URL',
        'Status', 'Status Changed At', 'Updated At', 'Created At',
        'Commits', 'Changed Files', 'Added Lines', 'Deleted Lines', 'Changed Lines',
        'Comments', 'Merged By', 'Reviewers', 'Reviews',
    )
    with open(config.PR_CSV_PATH, 'w') as f_out:
        writer = csv.DictWriter(f_out, fieldnames=header)
        writer.writeheader()
        writer.writerows(out_data)


if __name__ == '__main__':
    main()
