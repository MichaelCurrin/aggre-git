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
    for repo_name in config.REPO_PATHS:
        repo = CONN.get_repo(repo_name)
        print(repo.name)
        events_c = Counter()

        events = list(repo.get_events())
        ev = [x.type for x in events]
        events_c.update(ev)

        for e in events:
            data = dict(
                username=e.actor.login,
                created_at=str(e.created_at.date()),
                type=e.type
            )
            print(data)

            p = e.payload
            payload_data = dict(
                action=p.get('action'),
                comments=p.get('comment'),
                pull_request=p.get('pull_request'),
                issue=p.get('issue')
            )
            for k, v in payload_data.items():
                if v:
                    if isinstance(v, dict):
                        new_v = list(v.keys())
                        payload_data[k] = new_v
            pprint.pprint(payload_data)
        print()

    pprint.pprint(events_c.most_common())


if __name__ == '__main__':
    main()
