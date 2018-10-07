"""
Models module.

Includes data structures which require a PyGithub object as input and just
store the data of interest in this project.

This only is needed only printing, so wait until producing report rather
and store the commit or pr etc. itself rather. In nested structure.
"""
import github

import lib


class Commit:
    """
    Model a Git commit with just data of interest.

    Expects a PyGithub Commit object as returned from the API.
    """

    def __init__(self, commit: github.GitCommit.GitCommit):
        self.sha = commit.sha
        # Store as datetime.data object.
        self.last_modified = lib.parse_datetime(commit.stats.last_modified).date()
        self.additions = commit.stats.additions
        self.deletions = commit.stats.deletions
        self.total = commit.stats.total


class PullRequest:
    """
    Model a Git pull request with just data of interest.

    Expects a PyGithub Pull Request object as returned from the API.
    """

    def __init__(self, pull_request: github.PullRequest.PullRequest):
        self.number = pull_request.number
        self.title = pull_request.title
        self.status = pull_request.state
        self.created_at = pull_request.created_at.date()
        # Counts across all users, not just the author.
        self.commit_count = pull_request.commits
        self.changed_files = pull_request.changed_files
        self.assignees = pull_request.assignees

    def assignee_logins(self):
        return sorted([user.login for user in self.assignees])
