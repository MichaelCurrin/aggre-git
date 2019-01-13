"""
Local config.

See docs/installation.md for instructions.
"""

########
# Auth #
########

# Github API token to authenticate with.
# This is MUST be set with a valid value - see docs/installation.md.
ACCESS_TOKEN = ""


##################
# Global filters #
##################

# Lookup activity by these Github usernames.
USERNAMES = (
    'MichaelCurrin',
)

# Boolean value to switch between two inputs for reporting.
# - True: Use `REPO_OWNER` value. (So `REPO_PATHS` could be empty tuple or `None`.)
# - False: Use `REPO_PATHS` value. (So `REPO_OWNER` could be empty string or `None`.)
BY_OWNER = False

# Filter to activity within ALL repos owned by this account. This can be a
# Github user or organization.
REPO_OWNER = 'MichaelCurrin'

# Filter to activity within these Github repos. Format: 'username/repo-name'.
REPO_PATHS = (
    'MichaelCurrin/aggre-git',
)


# Cutoff date for activity - ignore commits before this date.
#
# Set as either:
# - `None`: No limit.
# - An integer: Number of days ago (inclusive). Set as 1 for yesterday and today.
# - Date as string: Earliest date (inclusive) in 'YYYY-MM-DD' format. Set
#       as yesterday's date for yesterday and today.
MIN_DATE = '2018-12-01'


#####################
# PR Report filters #
#####################

# Include only PRs in this state. Must be one of 'open', 'closed' or 'all'.
PR_STATE = 'all'
