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
    Model a Git commit, with just data of interest.

    Expects a PyGithub Commit object as returned from the API.
    """

    def __init__(self, commit: github.GitCommit.GitCommit):
        self.sha = commit.sha
        # Store as datetime.data object.
        self.last_modified = lib.parse_datetime(commit.stats.last_modified).date()
        self.additions = commit.stats.additions
        self.deletions = commit.stats.deletions
        self.total = commit.stats.total


class Review:
    """
    Model a Git pull request review, with just data of interest.

    Expects a PyGithub Commit object as returned from the API.
    Review state should be one of:
        'COMMENTED' 'APPROVED' 'DISMISSED' 'CHANGES_REQUESTED'
    """

    def __init__(self, review: github.PullRequestReview.PullRequestReview):
        self.state = review.state
        self.submitted_at = review.submitted_at.date()
        self.reviewer = review.user

    def summary(self):
        return f"{self.submitted_at} {lib.display(self.reviewer)} {self.state}"


class PullRequest:
    """
    Model a Git pull request,with just data of interest.

    Expects a PyGithub Pull Request object as returned from the API.

    The 'state' attribute  only records 'open' or 'closed' values.
    Therefore for easy of reporting, in this model we use status to
    represent one of 'OPEN', 'MERGED' or 'CLOSED'.
    """

    def __init__(self, pr: github.PullRequest.PullRequest):
        self.number = pr.number
        self.title = pr.title
        self.author = pr.user

        self.merged = pr.merged
        if pr.merged:
            self.merged_at = pr.merged_at.date()
            self.merged_by = pr.merged_by
        else:
            self.merged_at = None
            self.merged_by = None
        self.closed = (pr.state == 'closed')
        self.closed_at = pr.closed_at.date() if self.closed else None

        if self.merged:
            self.status = 'MERGED'
        elif self.closed:
            self.status = 'CLOSED'
        else:
            self.status = 'OPEN'

        self.created_at = pr.created_at.date()
        self.updated_at = pr.updated_at.date()

        # Note that counts are across all users who contributed.
        self.commit_count = pr.commits
        self.comment_count = pr.comments
        self.changed_files = pr.changed_files
        self.additions = pr.additions
        self.deletions = pr.deletions

        # This comes as a list not a paginated list.
        self.assignees = pr.assignees

        self.reviews = [Review(review) for review in pr.get_reviews()]

    def status_changed_at(self):
        """
        Return the date the PR was merged or closed on, or "N/A" if open.
        If a PR is merged, it is also closed and has a closed_at date.
        """
        return self.closed_at or "N/A"

    def merged_by_name(self):
        return lib.display(self.merged_by) if self.merged else None

    def assignee_names(self):
        return sorted([lib.display(user) for user in self.assignees])

    def reviewer_names(self):
        return sorted([lib.display(review.reviewer) for review in self.reviews])

    def review_summary(self):
        return [review.summary() for review in self.reviews]
