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
        https://pygithub.readthedocs.io/en/latest/github_objects/Commit.html
    """

    def __init__(self, commit: github.GitCommit.GitCommit):
        self.sha = commit.sha
        # Store as datetime.date object.
        self.last_modified = lib.parse_datetime(commit.stats.last_modified).date()
        self.additions = commit.stats.additions
        self.deletions = commit.stats.deletions
        self.total = commit.stats.total


class Review:
    """
    Model a Git pull request review, with just data of interest.

    Notes on states of PR Reviews:
        The web UI gives the following options when writing a PR review.
        - Comment
        - Approve
        - Request changes

        The Github API docs also covers a dismissed state. There is a pending
        state as well which came up in testing, but this appears to be hidden
        from other users and has no value for this project so can be ignored.
        To exclude it, apply a filter to only create a Review instance
        from a review which has a state which is in the Review.STATES values.

        See:
          https://help.github.com/articles/about-pull-request-reviews/

    Expects a PyGithub Commit object as returned from the API.
        https://pygithub.readthedocs.io/en/latest/github_objects/PullRequestReview.html
    """
    STATES = (
        'APPROVED',
        'DISMISSED',
        'CHANGES REQUESTED',
        'COMMENTED',
    )

    def __init__(self, review: github.PullRequestReview.PullRequestReview):
        self._state = review.state
        self.submitted_at = review.submitted_at.date()
        self.reviewer = review.user

    @classmethod
    def format_state(cls, s):
        return f'Review {s.replace("_", " ").title()}'

    @classmethod
    def get_states(cls):
        return tuple(cls.format_state(s) for s in cls.STATES)

    @property
    def state(self):
        return self.format_state(self._state)

    def summary(self):
        return f"{self.submitted_at} {lib.display(self.reviewer)} {self.state}"


class PullRequest:
    """
    Model a Git pull request,with just data of interest.

    Expects a PyGithub Pull Request object as returned from the API.
        https://pygithub.readthedocs.io/en/latest/github_objects/PullRequest.html

    The ID attribute on the source PR object is a hash, which we do not need.
    Therefore use the number. Note that a PR is also an Issue, so when a PR
    is created on Github its number will follow the next open Issue number
    increment.

    The 'state' attribute  only records 'open' or 'closed' values.
    Therefore for easy of reporting, in this model we use status to
    represent one of 'OPEN', 'MERGED' or 'CLOSED'.

    All values which are from int columns are across users, so bear this in
    mind when interpreting the values. For example, multiple users may
    contribute commits to a PR and the commit count is the sum of all.
    """

    def __init__(self, pr: github.PullRequest.PullRequest):
        self.number = pr.number
        self.title = pr.title
        self.author = pr.user
        self.url = pr.html_url

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

        self.commit_count = pr.commits
        self.comment_count = pr.comments
        self.changed_files = pr.changed_files
        self.additions = pr.additions
        self.deletions = pr.deletions

        # This comes as a list, not a paginated list.
        self.assignees = pr.assignees

        self.reviews = [Review(review) for review in pr.get_reviews()
                        if review.state in Review.STATES]

    def status_changed_at(self):
        """
        Return the date the PR was merged or closed on.

        :return: Closed at date of PR. If it was merged, this will be the same
            as the merged date. If the PR is still open, the value will be
            `None`.
        """
        return self.closed_at

    def merged_by_name(self):
        """
        Return a display name for the user who merged the PR, if merged.
        """
        return lib.display(self.merged_by) if self.merged else None

    def assignee_names(self):
        """
        Return a sorted list of display names for users who are assigned.

        This makes more sense for Issues than PRs.
        """
        return sorted(lib.display(user) for user in self.assignees)

    def reviewer_names(self):
        """
        Return a sorted list of display names for users which performed a
        review-related action on the PR.
        """
        names = set(lib.display(review.reviewer) for review in self.reviews)

        return sorted(names)

    def review_summary(self):
        """
        Return a list of review summary data for each of the PR's reviews.
        """
        return [review.summary() for review in self.reviews]
