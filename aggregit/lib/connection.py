"""
Connection module.
"""
from etc import config

from github import Github


CONN = Github(config.ACCESS_TOKEN)
