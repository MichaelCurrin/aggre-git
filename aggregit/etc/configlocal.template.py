"""
Local config.

See docs/installation.md for instructions.
"""

########
# Auth #
########

# GitHub API token to authenticate with.
# This is MUST be set with a valid value - see docs/installation.md.
ACCESS_TOKEN = ""


##################
# Global filters #
##################

# Filter activity to those by GitHub usernames. Set as None or empty tuple
# to disable filter.
USERNAMES = ("MichaelCurrin",)

# Boolean value to switch between two inputs for reporting.
# - True: Use `REPO_OWNER` value. (So `REPO_PATHS` could be empty tuple or `None`.)
# - False: Use `REPO_PATHS` value. (So `REPO_OWNER` could be empty string or `None`.)
BY_OWNER = False

# Filter to activity within ALL repos owned by this account. This can be a
# GitHub user or organization.
REPO_OWNER = "MichaelCurrin"

# Filter to activity within these GitHub repos. Format: 'username/repo-name'.
REPO_PATHS = ("MichaelCurrin/aggre-git",)


# Cutoff date for activity.
# For the PR report, any PRs which have not been updated since this date will be
# ignored.
#
# Set as either:
# - An integer: Number of days ago (inclusive). Set as 1 for yesterday and today.
#       This will be parsed to a datetime object relative to today's date.
# - Date as string: Earliest date (inclusive) in 'YYYY-MM-DD' format. Set
#       as yesterday's date for yesterday and today. This will be parsed to a
#       datetime object.
# - `None`: No limit.
MIN_DATE = None


#####################
# PR Report filters #
#####################

# Include only PRs in this state. Must be one of 'open', 'closed' or 'all'.
PR_STATE = "all"
