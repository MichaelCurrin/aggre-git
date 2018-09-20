"""
Local config.
"""


# Github API token to authenticate with.
# This is MUST be set with a valid value - see docs/installation.md.
ACCESS_TOKEN = "..."

# Paths for repos to report on (as account name and then repo name).
# Only lookup activity within these repos.
REPO_PATHS = (
    "MichaelCurrin/aggre-git",
)
# Username of user or organization. Only lookup activity in repos under this
# account. This does not have to correspond to the REPO_NAMES value as when
# this is used it is used in place of REPO_NAMES.
REPO_OWNER = "MichaelCurrin"

# If True, then lookup all repos within configured REPO_OWNER. Otherwise only
# lookup activity within REPO_NAMES.
BY_OWNER = False

# Lookup activity for these Github users. Note only activity within the
# selected repos will be counted, as set in either REPO_NAMES or REPO_OWNER.
USERNAMES = (
    "MichaelCurrin",
)
