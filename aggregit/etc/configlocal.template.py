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


#####################
# General filtering #
#####################

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


#####################
# PR Report filters #
#####################

# Include only PRs in this state. Must be one of 'open', 'closed' or 'all'.
PR_STATE = 'all'
