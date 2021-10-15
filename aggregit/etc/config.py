"""
Config module.

Test directly using:
$ python -m etc.config
"""
import datetime
import os

_VALID_PR_STATES = ("open", "closed", "merged", "all")


def parse_cutoff_date(value):
    """
    Convert a cutoff date from various formats to a datetime object.

    :param value: Cutoff date to convert. One of:
        - Date in 'YYYY-MM-DD' format e.g. '2019-01-01'
        - Integer as number of days ago e.g. 1.
        - Or anything else. Return None for no limit.

    :return datetime.datetime cutoff: Parsed cutoff date as a datetime
        object with time set to midnight, or None if input value was None.
    """
    if isinstance(value, str):
        cutoff = datetime.datetime.strptime(value, "%Y-%m-%d")
    elif isinstance(value, int):
        date = (
            datetime.date.today()
            - datetime.timedelta(days=value)
            + datetime.timedelta(days=1)
        )
        cutoff = datetime.datetime(date.year, date.month, date.day)
    else:
        cutoff = None

    return cutoff


def test():
    """
    Config test function to help manually validate values when running directly.
    """
    for value in ("2019-01-01", 0, 1, 365, None):
        print(f"{str(value):>10}: {parse_cutoff_date(value)}")


# Fixed system configs.
SRC_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_PATH = os.path.join(SRC_DIR, "var")
PR_CSV_PATH = os.path.join(OUTPUT_PATH, "pr_report.csv")
COMMIT_CSV_PATH = os.path.join(OUTPUT_PATH, "commit_report.csv")

# Import, parse and validate user's local config in this config file.
try:
    from .configlocal import (
        ACCESS_TOKEN,
        BY_OWNER,
        MIN_DATE,
        PR_STATE,
        REPO_OWNER,
        REPO_PATHS,
        USERNAMES,
    )
except ImportError:
    f_path = os.path.join(os.path.dirname(__file__), "configlocal.py")

    raise ImportError(f"You need to create a local config file at: {f_path}.")

MIN_DATE = parse_cutoff_date(MIN_DATE)

assert ACCESS_TOKEN, "Please set the ACCESS_TOKEN value in the local config" " file"
assert (
    PR_STATE in _VALID_PR_STATES
), f"Expected one of {_VALID_PR_STATES!r} but got: {PR_STATE!r}"

if __name__ == "__main__":
    test()
