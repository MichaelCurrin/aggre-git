"""
Config module.

Test directly using:
$ python -m etc.config
"""
import datetime
import os


def parse_cutoff_date(value):
    """
    Convert a cutoff date in various formats.

    :param value: Cutoff date. One of:
        - Date in 'YYYY-MM-DD' format e.g. '2019-01-01'
        - Integer as number of days ago e.g. 1. Note that this will not round
              down so the current time will be used as the time for the cutoff day.
        - `None` for no limit, such that earliest possible unix date is returned.

    :return datetime.datetime cutoff: Parsed cutoff date as datetime object
        for easy comparison with Github activity datetime values.
    """
    if isinstance(value, str):
        cutoff = datetime.datetime.strptime(value, '%Y-%m-%d')
    elif isinstance(value, int):
        cutoff = datetime.datetime.today() - datetime.timedelta(days=value)
    else:
        cutoff = datetime.datetime.fromtimestamp(0)

    return cutoff


def test():
    """
    Config test function to help manually validate values when running directly.
    """
    for value in ('2019-01-01', 0, 1, 365, None):
        print(f"{str(value):>10}: {parse_cutoff_date(value)}")


# Fixed system configs.
SRC_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_PATH = os.path.join(SRC_DIR, 'var')
PR_CSV_PATH = os.path.join(OUTPUT_PATH, 'pr_report.csv')


# Import, parse and validate user's local config in this config file.
try:
    from .configlocal import *
except ImportError:
    f_path = os.path.join(os.path.dirname(__file__), 'configlocal.py')
    raise ImportError(f"You need to create a local config file at: {f_path}.")

MIN_DATE = parse_cutoff_date(MIN_DATE)

assert ACCESS_TOKEN, "Please set the ACCESS_TOKEN value in the local config" \
                     " file"


if __name__ == '__main__':
    test()
