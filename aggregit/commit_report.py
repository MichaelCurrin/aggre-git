"""
Commit report script.

Create a report of Github commits across configured repos and available
branches. The report is bound by the configured usernames, repos and
minimum date. The result is written out to a CSV.

PyGithub doc on Branches:
    https://pygithub.readthedocs.io/en/latest/github_objects/Branch.html
"""
from etc import config
import lib
from models import Commit


def traverse_commits(commit, seen_commits):
    """
    Get the details for a commit and all its parents.

    Return the details for the current commit and recursively return the details
    of its parents. Note that there may be two parents such as a for a merge
    commit. In that case, the tree path structure will be flattened out when
    to the one parent line's commits followed by the other parent line's
    commits, so order is not by time.

    Skip any commits which are older than the configured minimum date.

    For each commit which is returned, print a character to show progress.

    :param commit: A Github commit object to report on.
    :param seen_commits: Commit SHA values which have been seen before.
        This should be a set a of str values. This variable is passed by
        reference so additions to it take effect outside of the function.
        The set is also past to recursive calls of the function, so that
        one increasing history of seen commits is shared across calls.

        Note - this is setup to use short SHA values, created from getting
        the first 8 characters only. This saves on memory and is sufficient
        for comparing commits within a branch as collisions are unlikely.

    :return: Generator which yields details for the current commit and then its
        parent commits, within the configured date range. If the commit
        has multiple parents such as for a merge commit, then both paths
        will be followed, one after the other.

        When a commit has been seen, it is outside of the date range or it
        has no parent commits (it is the inital commit), then None will be
        returned. This will stop the generator.
    """
    if commit.sha in seen_commits:
        print("(skipping seen)")

        return None

    sha = commit.sha[:7]
    seen_commits.update([sha])

    last_modified = lib.parse_datetime(commit.commit.last_modified)
    if config.MIN_DATE and last_modified < config.MIN_DATE:
        print("(skipping old)")

        return None

    out_commit = Commit(commit)

    print(".", end="")
    yield out_commit
    for parent in commit.parents:
        yield from traverse_commits(parent, seen_commits)


def main():
    """
    Main command-line function to create a report of Github commit activity.

    For the configured repos, get all available branches. Start with
    master, then develop, then the feature branches (which are already
    in alphabetical order. Get the stats across the commits by starting
    with the HEAD commit and get its parents recursively. Skip commits older
    than the min date. Once commits are fetched (each requiring a GET request),
    then filter to just those by the configured users. Filter out commits
    which have no author set.

    Keep track of the SHA commit values seen when iterating through a branch
    (since a merge commit will have two histories which should have a common
    commit which they diverged from). Additionally, we keep track of SHA commit
    values across branches in a repo, so that after we have traversed master
    all the way back to its initial commit (if the date range allows), then
    we only have to look at commits which are previously traversed branches
    when going through develop (if it exists) and any feature branches.

    Write out the commits out as a CSV report, where each row includes the
    commit details of a commit along with its repo and branch.
    """
    if config.MIN_DATE:
        print(f"Commit min date: {config.MIN_DATE}")
    else:
        print("No commit min date set")
    print()

    for repo in lib.get_repos():
        print(f"REPO: {repo.name}")

        seen_commits = set()

        for branch in repo.get_branches():
            print(f"BRANCH: {branch.name}")

            print("Fetching commits ", end="")
            commits = list(traverse_commits(branch.commit, seen_commits))
            print(f"\nFound: {len(commits)}")

            if config.USERNAMES:
                commits = [x for x in commits if
                           x.author and x.author.login in config.USERNAMES]
                print(f"After filtering: {len(commits)}")

            print()
        print()


if __name__ == '__main__':
    main()
