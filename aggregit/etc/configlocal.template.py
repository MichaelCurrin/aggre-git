"""
Local config.

See docs/installation.md for instructions.
"""


# Github API token to authenticate with.
# This is MUST be set with a valid value - see docs/installation.md.
ACCESS_TOKEN = "..."

# Paths for repos to report on (as account name and then repo name).
# Only lookup activity within these repos.
REPO_PATHS = (
    'MichaelCurrin/aggre-git',
)
# Username of user or organization. Only lookup activity in repos under this
# account. This does not have to correspond to the REPO_PATHS value as when
# this is used it is used in place of REPO_PATHS.
REPO_OWNER = 'MichaelCurrin'

# If True, then lookup all repos within configured REPO_OWNER. Otherwise only
# lookup activity within REPO_PATHS.
BY_OWNER = False

# Lookup activity for these Github users. Note only activity within the
# selected repos will be counted, as set in either REPO_PATHS or REPO_OWNER.
USERNAMES = (
    'MichaelCurrin',
)

# Include only PRs in this state. Must be one of 'open', 'closed' or 'all'.
PR_STATE = 'all'
