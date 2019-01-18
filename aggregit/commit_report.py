"""
Commit report script.

Create a report of Github commits across configured repos and available
branches. The report is bound by the configured usernames, repos and
minimum date. The result is written out to a CSV.
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
        parent commits, within the configured date range. The commit objects are
        returned as Commit instances, formatted using the PyGithub GitCommit
        object given as an argument.

        If the commit has multiple parents such as for a merge commit,
        then both paths will be followed, one after the other.

        When a commit has been seen, it is outside of the date range or it
        has no parent commits (it is the initial commit), then None will be
        returned. This will stop the generator.
    """
    if commit.sha in seen_commits:
        print("(skipping seen)", end="")

        return None

    sha = commit.sha[:8]
    seen_commits.update([sha])

    last_modified = lib.parse_datetime(commit.commit.last_modified)
    if config.MIN_DATE and last_modified < config.MIN_DATE:
        print("(skipping old)", end="")

        return None

    print("-", end="")
    yield Commit(commit)

    if len(commit.parents) >= 2:
        print("(merge)", end="")

    for parent in commit.parents:
        if len(commit.parents) >= 2:
            print("\n<", end="")
        yield from traverse_commits(parent, seen_commits)


def to_row(repo, branch, commit_data):
    """
    Format input data around a single commit and return as a row for a CSV.

    :param repo: The repo the commit is in.
    :param branch: The branch the commit is in.
    :param commit: Instance of Commit, containing data for a single commit.

    :return dict out_row: Formatted dict of repo, branch and commit data for
        a single commit.
    """
    out_row = {
        'Repo Owner': lib.display(repo.owner),
        'Repo Name': repo.name,
        'Branch': branch.name,
        'Commit SHA': commit_data.short_sha,
        'Commit Modified': commit_data.last_modified.date(),
        'Commit Author': lib.display(commit_data.author),
        'Changed Files': commit_data.changed_files,
        'Added Lines': commit_data.additions,
        'Deleted Lines': commit_data.deletions,
        'Changed Lines': commit_data.additions + commit_data.deletions,
    }

    return out_row


def main():
    """
    Main command-line function to create a report of Github commit activity.

    Fetch and write commits out as a CSV report, where each row includes the
    details of a single commit including stats, metadata and the repo and branch
    labels.

    For the configured repos, get all available branches. Start with
    master, then develop, then the feature branches (leaving them
    in alphabetical order). Get the stats across the commits by starting
    with the HEAD commit and get its parents recursively. Skip commits older
    than the min date. Once commits are fetched (each requiring a GET request),
    then filter to just those by the configured users. Filter out commits
    which have no author set.

    We keep track of the SHA commit values seen when iterating through a branch
    (since a merge commit will have two histories which should have a common
    commit which they diverged from). Additionally, we keep track of SHA commit
    values across branches in a repo, so that after we have traversed master
    all the way back to its initial commit (if the date range allows), then
    we only have to look at commits which are previously traversed branches
    when going through develop (if it exists) and any feature branches.
    """
    if config.MIN_DATE:
        print(f"Commit min date: {config.MIN_DATE}")
    else:
        print("No commit min date set")
    print()

    out_data = []
    for repo in lib.get_repos():
        print(f"REPO: {repo.name}\n")

        seen_commits = set()

        fetched_branches = repo.get_branches()
        branch_list = []

        for branch in fetched_branches:
            if not branch_list:
                branch_list.append(branch)
            elif branch.name == 'master':
                branch_list.insert(0, branch)
            elif branch.name in ('develop', 'development'):
                dev_insert_index = 1 if branch_list[0] == 'master' else 0
                branch_list.insert(dev_insert_index, branch)
            else:
                branch_list.append(branch)

        for branch in branch_list:
            print(f"BRANCH: {branch.name}")

            print("Fetching commits")
            commits = list(traverse_commits(branch.commit, seen_commits))
            print(f"\nFound: {len(commits)}")

            if config.USERNAMES:
                commits = [x for x in commits if
                           x.author and x.author.login in config.USERNAMES]
                print(f"After filtering: {len(commits)}")

            for commit in commits:
                try:
                    out_row = to_row(repo, branch, commit)
                except Exception as e:
                    # Report error without aborting.
                    print(f"Could not parse Commit."
                          f" {type(e).__name__}: {str(e)}")
                else:
                    out_data.append(out_row)
            print()

    header = (
        'Repo Owner',
        'Repo Name',
        'Branch',
        'Commit SHA',
        'Commit Modified',
        'Commit Author',
        'Changed Files',
        'Added Lines',
        'Deleted Lines',
        'Changed Lines',
    )
    lib.write_csv(config.COMMIT_CSV_PATH, header, out_data)


if __name__ == '__main__':
    main()
