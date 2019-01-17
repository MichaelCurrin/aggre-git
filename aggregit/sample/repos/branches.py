"""
Sample repo branches script.

Explore getting details of a branch object within a repo.

The problem with getting parent's commits and the history behind that is that
the same commits will start coming up. When there is a merge commit from
a feature branch and master, you can split into the getting the history for
each but they will eventually have a common commit. You have to check for this
and ignore that object and its parents, otherwise you'll print (or count)
the common history for both tree paths.

PyGithub docs
 - Branches:
    https://pygithub.readthedocs.io/en/latest/github_objects/Branch.html
 - Commits:
    https://pygithub.readthedocs.io/en/latest/github_objects/Commit.html
 - Files:
    https://pygithub.readthedocs.io/en/latest/github_objects/File.html
"""
import string
import time
from textwrap import shorten

from lib.connection import CONN


def display_commit(commit):
    """
    Print details and stats for a commit.
    """
    print("COMMIT")
    print(commit.sha)
    print(commit.html_url)
    if commit.author:
        # This was observed in a case where the commit in the Github site
        # has an author who wrote the patch but there is no link to his profile
        # so perhaps he was deleted. So author can be None.
        print(commit.author.login)
    else:
        print("NO AUTHOR")
    print(commit.last_modified)
    message = shorten(commit.commit.message.replace("\n", "\t"), 80)
    print(message)
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


def traverse_commits_detailed(commit, seen_commits=None):
    """
    Display details, stats and files for a given commit and all its parents.

    Include the names of files in the commit and details of the first file.
    Allow for the fact that there could be zero files such in the initial
    commit.

    Then use recursive logic to get all the commits in the chain, starting
    with the commit's parents.
    """
    if not seen_commits:
        seen_commits = set()

    if commit.sha not in seen_commits:
        display_commit(commit)

        if commit.files:
            print([file_.filename for file_ in commit.files])
            print()
            display_file(commit.files[0])
        else:
            print("No files on commit")

        time.sleep(1)

        # For a merge there could be multiple parents.
        # When storing objects rather than just printing, consider using
        # `yield` to avoid doing a return on the first only.
        for parent in commit.parents:
            traverse_commits_detailed(parent)
    else:
        print("Skipping seen commit and parents")


def traverse_commits_short(commit, depth=1, parent_index=0, seen_commits=None):
    """
    Display summarized data for commits in a chain.

    Display attributes recursively for a commit and its parents.

    Depth is the level of commits where the current commit has depth 1 and
    the parent is 2 and so on. When going into paths from a merge commit, the
    depth will drop to 1 again for that path.

    Print how many commits have been seen for interest.
    """
    if not seen_commits:
        seen_commits = set()

    if commit.sha not in seen_commits:
        seen_commits.update([commit.sha])
        seen_display = f"seen commits {len(seen_commits):3}"
        depth_display = f"depth {depth:3}"
        parent_symbol = f"path {string.ascii_uppercase[parent_index]}"
        message = shorten(commit.commit.message.replace("\n", "\t"), 70)
        elements = (commit.sha, seen_display, depth_display, parent_symbol, message)
        print(" | ".join(elements))

        for i, parent in enumerate(commit.parents):
            traverse_commits_short(parent, depth+1, i+parent_index, seen_commits)
    else:
        print("Skipping seen commit and parents")


def main():
    """
    Main command-line function to demonstration iterating through commits on
    a branch. All commits in the branch's history are printed, including ones
    that come from merging a feature branch into master. There is an escape
    though in the traversal to avoid printing a commit which has been seen
    before in the traversal.
    """
    # A good showcase of a repo with many branches.
    repo = CONN.get_repo("Python/CPython")

    fetched_branches = list(repo.get_branches())
    branch_dict = {x.name: x for x in fetched_branches}

    branch_list = []
    for b in ('master', 'develop'):
        branch = branch_dict.pop(b, None)
        if branch:
            branch_list.append(branch)

    remaining = branch_dict.values()
    branch_list.extend(remaining)

    for branch in branch_list:
        print(f"Branch: {branch.name}")

        head_commit = branch.commit
        print(head_commit)
    print()

    # Showcase iterating through commits on a repo with few branches.

    repo = CONN.get_repo('MichaelCurrin/aggre-git')
    for branch in repo.get_branches():
        head_commit = branch.commit
        traverse_commits_short(head_commit)

        # Use this instead for more verbose output including the files.
        #traverse_commits_detailed(head_commit)


if __name__ == '__main__':
    main()
