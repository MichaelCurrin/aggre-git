"""
Models module.

Includes data structures which require a PyGithub object as input and just
store the data of interest in this project.

This only is needed only printing, so wait until producing report rather
and store the commit or pr etc. itself rather. In nested structure.
"""
import github

import lib


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
        return f"Review {s.replace('_', ' ').title()}"

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
    Model a Gitub pull request, with just data of interest.

    Expects a PyGithub Pull Request object as returned from the API.
        https://pygithub.readthedocs.io/en/latest/github_objects/PullRequest.html

    The ID attribute on the source PR object is a hash, which we do not need.
    Therefore use the number. Note that a PR is also an Issue, so when a PR
    is created on Github its number will follow the next open Issue number
    increment.

    Github records merged as a boolean and it limits 'state' to only be 'open'
    or 'closed' values. For our own easy reporting, we rather use a system of
    three possible values on 'status', with labels set as constants on the
    class. But, we still keep merged- and closed-related values, as there is
    value in having the date and user where applicable.

    All values which are from `int` columns are across users, so bear this in
    mind when interpreting the values. For example, multiple users may
    contribute commits to a PR and the commit count is the sum of all.
    """
    STATUS_MERGED = "Merged"
    STATUS_CLOSED = "Closed"
    STATUS_OPEN = "Open"

    def __init__(self, pr: github.PullRequest.PullRequest):
        """
        Initialize customized PR object based on an existing Github PR object.
        """
        self.number = pr.number
        self.title = pr.title
        self.from_branch_name = pr.head.ref
        self.to_branch_name = pr.base.ref
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
            self.status = self.STATUS_MERGED
        elif self.closed:
            self.status = self.STATUS_CLOSED
        else:
            self.status = self.STATUS_OPEN

        self.created_at = pr.created_at.date()
        self.updated_at = pr.updated_at.date()

        self.commit_count = pr.commits
        self.comment_count = pr.comments
        self.changed_files = pr.changed_files
        self.additions = pr.additions
        self.deletions = pr.deletions

        # This is a plain list and not a paginated list.
        self.assignees = pr.assignees

        self.reviews = [Review(review) for review in pr.get_reviews()
                        if review.state in Review.STATES]

    def status_changed_at(self):
        """
        If merged or closed, get the date that the change happened on.

        :return: Closed at date of PR. If it was merged, this will be the same
            as the merged date. If the PR is still open, the value will be
            `None`.
        """
        return self.closed_at

    def merged_by_name(self):
        """
        Get the display name for the user who merged the PR, if it was merged.
        """
        return lib.display(self.merged_by) if self.merged else None

    def assignee_names(self):
        """
        Get names of assignees of the PR, if any.

        Return a sorted list of display names for users who are assigned.
        This makes more sense for Issues than PRs.
        """
        return sorted(lib.display(user) for user in self.assignees)

    def reviewer_names(self):
        """
        Get names of reviewers of the PR, if any.

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


class Commit:
    """
    Model a Github commit, with just data of interest.

    An author wrote the patch while the committer applied the patch,
    perhaps with a merge? Note that author maybe None - this was noted
    in a case where a user was labeled but not clickable in the
    Github site.

    Expect a PyGithub Commit as returned from the API:
        https://pygithub.readthedocs.io/en/latest/github_objects/Commit.html
    """

    def __init__(self, commit: github.GitCommit.GitCommit):
        """
        Initialize Commit object based on a Github commit object.

        Note that using just `commit.last_modified` gives `None` somehow, so we
        use `commit.commit.last_modified` instead. `commit.stats.last_modified`
        also works.
        """
        self.sha = commit.sha
        self.url = commit.html_url

        self.author = commit.author
        self.committer = commit.committer
        self.last_modified = lib.parse_datetime(commit.commit.last_modified)
        self.message = commit.commit.message

        self.files = commit.files
        self.additions = commit.stats.additions
        self.deletions = commit.stats.deletions

    @property
    def short_sha(self):
        """
        Return first 8 characters of the SHA value.
        """
        return self.sha[:8]

    @property
    def short_message(self):
        """
        Return truncated form of the commit message, for neat printing.
        """
        return lib.truncate(self.message, 50)

    def __repr__(self):
        """
        Summarize attributes when printing an instance.
        """
        login = self.author.login if self.author else "(not set)"
        return f"<Commit sha: '{self.short_sha}', author: '{login}'" \
               f" message: '{self.short_message}', ...>"
