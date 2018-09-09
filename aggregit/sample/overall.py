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
from etc import config
import lib
from lib.connection import CONN


login = config.MY_HANDLE

for repo_name in config.REPOS:
    repo = CONN.get_repo(repo_name)

    print("######## REPO ########")
    print(repo.full_name)
    print(repo.name)
    print(repo.description)

    u_prs = 0
    u_commits = 0
    u_additions = 0
    u_deletions = 0

    # Note that .totalCount gives an error so can't be used to count PRs
    # in a repo.

    for pr in repo.get_pulls():
        pr_author = pr.user

        if pr.user.login == login:
            u_prs += 1
            print("### PR ###")
            print("ID: {}".format(pr.number))
            print("Title: {}".format(pr.title))

            print("Author: @{}".format(pr_author.login))
            print("Commits: {}".format(pr.commits))
            print()

            print("--- Commits ---")
            if pr.commits:
                for commit in pr.get_commits():
                    # Sometimes author can be None. Perhaps if the user is
                    # inactive or it was left off the of config file.
                    if commit.author and commit.author.login == login:
                        u_commits += 1

                        date = lib.parse_commit_date(commit.stats.last_modified)
                        commit_data = dict(
                            SHA=commit.sha,
                            last_modified=str(date),
                            additions=commit.stats.additions,
                            deletions=commit.stats.deletions,
                            total=commit.stats.total
                        )
                        print(commit_data)

                        comments = list(commit.get_comments())
                        print("Comments: {}".format(len(comments)))

                        for file_ in commit.files:
                            print(file_.filename)
                            print("  Changes: {}".format(file_.changes))
                            print("  Additions: {}".format(file_.additions))
                            print("  Deletions: {}".format(file_.deletions))
                            print("  Status: {}".format(file_.status))

                            print("  Raw URL: {}".format(file_.raw_url))
                            print("  Blob URL: {}".format(file_.blob_url))
                            # See also file_.patch for the diff.

                            u_additions += file_.additions
                            u_deletions += file_.deletions
                            print()
                    else:
                        print(pr.title)
                        print("Expected: {}".format(login))
                        print(commit)

                print()
        print()
print()

print("Totals for {} for configured repos".format(login))
data = {
   'prs': u_prs,
   'commits': u_commits,
   'additions': u_additions,
   'deletions': u_deletions,
}
print(data)
