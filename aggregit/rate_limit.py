#!/usr/bin/env python
"""
Rate limit report.

Get rate limiting status and reset time for the configured Github API token.

Check in the browser using your browser user rather than a token.
    https://developer.github.com/v3/rate_limit/
    "Note: Accessing this endpoint does not count against your REST API rate
    limit."
"""
import datetime
import time

from lib.connection import CONN


def main():
    """
    Main command-line function.
    """
    reset_time = datetime.datetime.fromtimestamp(CONN.rate_limiting_resettime)
    wait = reset_time - datetime.datetime.now()

    print(f"Reset time: {reset_time.time()}")
    print(f"Wait time : {wait}")
    print()

    while True:
        remaining, total = CONN.rate_limiting
        percent = remaining / total
        print(f"Remaining : {remaining:,d} / {total:,d} ({percent:3.2%})")
        print("Waiting...")
        time.sleep(5)


if __name__ == '__main__':
    main()
