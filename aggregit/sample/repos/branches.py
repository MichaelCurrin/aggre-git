"""
Sample repo branches script.

Explore getting details of a branch object within a repo.

PyGithub doc on Branches:
    https://pygithub.readthedocs.io/en/latest/github_objects/Branch.html
"""
import time

from lib.connection import CONN


def display_commit(commit):
    """
    Print details and stats for a commit.
    """
    print("COMMIT")
    print(commit.sha)
    print(commit.url)
    print(commit.author.login)
    print(commit.last_modified)
    print(f"{commit.stats.total} | +{commit.stats.additions} | -{commit.stats.deletions})")
    print()


def display_file(file_):
    """
    Print details and stats for a file on a commit.
    """
    print("FILE")
    print(file_.filename)
    print(file_.blob_url)
    print(file_.last_modified)
    print(file_.status)
    print(f"{file_.changes} | +{file_.additions} | -{file_.deletions}")
    print()


def traverse_commits(commit):
    """
    Display details, stats and files for a given commit and all its parents.

    Include the names of files in the commit and details of the first file.
    Allow for the fact that there could be zero files such in the initial
    commit.

    Then use recursive logic to get all the commits in the chain, starting
    with the commit's parents.
    """
    display_commit(commit)

    if commit.files:
        print([file_.filename for file_ in commit.files])
        print()
        display_file(commit.files[0])
    else:
        print("No files on commit")

    time.sleep(1)

    # For a merge there could be multiple parents.
    for parent in commit.parents:
        traverse_commits(parent)


def main():
    repo = CONN.get_repo("PyGithub/PyGithub")
    branches = list(repo.get_branches())
    branch = branches[0]
    print(branch.name)

    head_commit = branch.commit

    traverse_commits(head_commit)


if __name__ == '__main__':
    main()
