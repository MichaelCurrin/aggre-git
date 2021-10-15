"""
Overall sample report.

This script is not easy to maintain or extend but it used as a demo of
how stats can be aggregated down to a commit level for a specific user.

Iterates through configured repos and the PRs within it. Count the commits
which the configured users contributed to the PR.

https://developer.github.com/v3/git/commits/

https://stackoverflow.com/questions/18750808/difference-between-author-and-committer-in-git
The commit.author is who wrote the patch.
The commit.committer is a project maintainer and who merged the patch on behalf
of the author.
"""
import lib
from etc import config
from lib.connection import CONN

# TODO: Refactor to do counts for each user with one pass through the repos.
login = config.USERNAMES[0]

data = {
    "prs": 0,
    "commits": {"own": None, "other": None},
    "additions": 0,
    "deletions": 0,
    "review_comments": {"own": None, "other": None},
    "issue_comments": {"own": None, "other": None},
    "reviews": {"own": None, "other": None},
}

for repo_name in config.REPO_PATHS:
    repo = CONN.get_repo(repo_name)

    print("######## REPO ########")
    print(repo.full_name)
    print(repo.name)
    print(repo.description)
    print()

    # Note that .totalCount gives an error so can't be used to count PRs
    # in a repo.

    # Note - only activity in PRs is counted, not direct commits to a branch.
    # Note state could be set as 'open', 'closed' or 'all'.
    for pr in repo.get_pulls(state="all"):
        pr_author = pr.user

        if pr.user.login == login:
            data["prs"] += 1
            print("### PR ###")
            print(f"ID: {pr.number}")
            print(f"Title: {pr.title}")

            print(f"Author: @{pr_author.login}")
            print(f"Commits: {pr.commits} (by all users)")
            print(f"Reviews: {len(list(pr.get_reviews()))}")

            print(f"Changed files: {pr.changed_files}")

            # TODO: Count only comments by this user.
            print(f"Review comments: {len(list(pr.get_review_comments()))}")
            print(f"Issue comments: {len(list(pr.get_issue_comments()))}")
            print()

            print("--- Commits ---")

            if pr.commits:
                for commit in pr.get_commits():
                    # Sometimes author can be None. Perhaps if the user is
                    # inactive or it was left off the of config file.
                    if commit.author and commit.author.login == login:
                        data["commits"]["own"] += 1

                        date = lib.parse_datetime(commit.stats.last_modified).date()
                        commit_data = dict(
                            SHA=commit.sha,
                            last_modified=str(date),
                            additions=commit.stats.additions,
                            deletions=commit.stats.deletions,
                            total=commit.stats.total,
                        )
                        print(commit_data)

                        for file_ in commit.files:
                            print(file_.filename)
                            print(f"  Changes: {file_.changes}")
                            print(f"  Additions: {file_.additions}")
                            print(f"  Deletions: {file_.deletions}")
                            print(f"  Status: {file_.status}")

                            print(f"  Raw URL: {file_.raw_url}")
                            print(f"  Blob URL: {file_.blob_url}")
                            # See also file_.patch for the diff.

                            data["additions"] += file_.additions
                            data["deletions"] += file_.deletions
                            print()
                    else:
                        data["commits"]["other"] += 1
                print()
        print()
print()

print(f"Totals for {login} for configured repos")
print(data)
