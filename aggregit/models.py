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

    def reviewer_login(self):
        return self.reviewer.login

    def summary(self):
        return f"{str(self.submitted_at)}:{self.reviewer_login()}:{self.state}"


class PullRequest:
    """
    Model a Git pull request,with just data of interest.

    Expects a PyGithub Pull Request object as returned from the API.
    """

    def __init__(self, pr: github.PullRequest.PullRequest):
        self.number = pr.number
        self.title = pr.title
        self.author = pr.user.login

        self.state = pr.state
        self.merged = pr.merged
        if pr.merged:
            self.merged_at = pr.merged_at.date()
            self.merged_by = pr.merged_by.login
        else:
            self.merged_at = None
            self.merged_by = None

        self.created_at = pr.created_at.date()
        self.updated_at = pr.updated_at.date()

        # Counts across all users, not just the author.
        self.commit_count = pr.commits

        self.changed_files = pr.changed_files

        # This is optional but not sure if this is assigned to do the work or
        # review, as its separate to reviewers. This comes as a list not a
        # paginated list.
        self.assignees = pr.assignees

        # TODO: Add methods to get dates and results of reviews.
        self.reviews = [Review(review) for review in pr.get_reviews()]

    def status(self):
        if self.state == 'closed':
            return 'CLOSED'

        if self.merged:
            return 'MERGED'
        else:
            return 'OPEN'

    def assignee_logins(self):
        return sorted([user.login for user in self.assignees])

    def reviewer_logins(self):
        return sorted([review.reviewer_login() for review in self.reviews])

    def review_summary(self):
        return [review.summary() for review in self.reviews]
