#!/usr/bin/env python3
"""
Pull Request report script.

Get all Pull Requests and print out summary data. This report is orientated
around PRs, so ignores any work in branches which do not have PR. It is also
focused on when a PR was created or last updated, rather than when the activity
in the PR occurred.

Requires either a configured repo owner (as user or organization) to retrieve
repos for, otherwise the paths for required repos.

Also requires configured usernames, such that only PRs created by these users
are included. A commit doesn't have to have an author - if blank assume it
was by the PR author (as it probably was).
"""
from collections import Counter

from etc import config
import lib
from models import PullRequest, Review


def to_row(repo, author, pr):
    """
    Convert PR elements to a row of data.

    After processing the input repo, author and PR, the last part is to
    get the counts for each possible review action and add them as columns to
    the row (using zero as default value).

    :param github.Repository.Repository repo: Github repo object.
    :param github.NamedUser.NamedUser author: Github user object.
    :param github.PullRequest.PullRequest pr: Github PR object.

    :return dict out_row: dict of data around a PR's repo, the PR author and
        the PR itself. The status changed, created and updated date will be kept
        as datetime.datetime objects.
    """
    pr_data = PullRequest(pr)

    out_row = {
        'Repo Owner': lib.display(repo.owner),
        'Repo Name': repo.name,
        'Repo URL': repo.html_url,

        'Author': lib.display(author),
        'PR ID': f"#{pr_data.number}",
        'PR Title': pr_data.title,
        'PR From Branch': pr_data.from_branch_name,
        'PR To Branch': pr_data.to_branch_name,
        'PR URL': pr_data.url,
        'Jira Ticket': pr_data.jira_ticket,

        'PR Updated At': pr_data.updated_at,
        'PR Created At': pr_data.created_at,

        'Latest Commit At': pr_data.latest_commit.last_modified.date(),
        'First Commit At': pr_data.first_commit.last_modified.date(),

        'Status': pr_data.status,

        'Status Changed At': pr_data.status_changed_at(),
        'Merged By': pr_data.merged_by_name(),

        'Reviewers': ", ".join(pr_data.reviewer_names()),

        'Comments': pr_data.comment_count,
        'Commits': pr_data.commit_count,
        'Changed Files': pr_data.changed_files,
        'Added Lines': pr_data.additions,
        'Deleted Lines': pr_data.deletions,
        'Changed Lines': pr_data.additions + pr.deletions,
    }

    review_states = Counter([r.state for r in pr_data.reviews])
    [review_states.setdefault(s, 0) for s in Review.get_states()]
    out_row.update(**dict(review_states))

    return out_row


def main():
    """
    Main command-line function to fetch PR data then write a CSV.

    Set the usernames value in the config so that the report will either
    filter to specific usernames or show activity for all.

    If using the BY_OWNER setting, it's best to try retrieve the profile as an
    org first, since  getting an org as a user object only gives as access to
    public repos. Fallback to getting a user object if it wasn't actually
    an org.

    Use the MIN_DATE value in the config to exclude PRs which were last updated
    before the cutoff date. The API's default setting is to return PRs ordered
    by most recently created first.
        https://developer.github.com/v3/pulls/#list-pull-requests
    Therefore if we encounter an old PR then skip remaining PRs and go the next
    repo.
    """
    if config.MIN_DATE:
        print(f"PR updates min date: {config.MIN_DATE}")
    else:
        print("No PR updates min date set")
    print()

    out_data = []
    for repo in lib.get_repos():
        print(f"REPO: {repo.name}")

        for pr in repo.get_pulls(state=config.PR_STATE):
            if config.MIN_DATE and pr.updated_at < config.MIN_DATE:
                print("Remaining PRs are inactive")
                break

            author = pr.user
            if not config.USERNAMES or author.login in config.USERNAMES:
                print(f"PR #{pr.number} - author: @{author.login}")
                try:
                    out_row = to_row(repo, author, pr)
                except Exception as e:
                    # Keep the report generation robust by logging and skipping
                    # over any errors. Create a bug issue in the aggre-git repo
                    # on Github so that the error will be addressed.
                    print(f"Could not fetch or parse PR."
                          f" {type(e).__name__}: {str(e)}")
                else:
                    out_data.append(out_row)
            else:
                print(f"PR #{pr.number} - skipping")

    header = (
        'Repo Owner', 'Repo Name', 'Repo URL',
        'PR ID', 'PR Title', 'PR From Branch', 'PR To Branch',
        'Author', 'PR URL', 'Jira Ticket',
        'Status', 'Status Changed At',
        'PR Updated At', 'PR Created At',
        'Latest Commit At', 'First Commit At',
        'Commits', 'Changed Files', 'Added Lines', 'Deleted Lines',
        'Changed Lines',
        'Comments', 'Merged By', 'Reviewers',
    ) + Review.get_states()

    lib.write_csv(config.PR_CSV_PATH, header, out_data)


if __name__ == '__main__':
    main()
