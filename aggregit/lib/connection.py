"""
Connection module.

Note that username and password can be used as arguments instead of token, but
you can error if your account is setup for security to use OTP.
"""
from github import Github

from etc import config


CONN = Github(config.ACCESS_TOKEN)
