"""
Sample repo pull request events module.

Type examples:
{'CreateEvent', e.g. branch
 'IssueCommentEvent',
 'IssuesEvent',
 'PullRequestEvent',
 'PushEvent',
 'WatchEvent'}
"""
import pprint
from collections import Counter

from etc import config
from lib.connection import CONN


def main():
    for repo_name in config.REPOS:
        repo = CONN.get_repo(repo_name)
        print(repo.name)
        events_c = Counter()

        events = list(repo.get_events())
        ev = [x.type for x in events]
        events_c.update(ev)

        for e in events:
            print(e.actor.login)
            print(str(e.created_at.date()))
            print(e.type)

            p = e.payload
            action = p.get('action')
            if action:
                print(action)
            print()
        print()

    pprint.pprint(events_c.most_common())


if __name__ == '__main__':
    main()


