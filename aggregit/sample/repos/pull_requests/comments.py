"""
Sample repo pull request comments module.
"""
import pprint

from etc import config
from lib.connection import CONN


def main():
    for repo_name in config.REPO_PATHS:
        repo = CONN.get_repo(repo_name)
        print(repo.name)

        for comment in repo.get_pulls_comments():
            data = dict(
                date=str(comment.created_at.date()),
                username=comment.user.login,
                reactions=[]
            )

            reactions = list(comment.get_reactions())
            for r in reactions:
                reaction_data = {
                    'username': r.user.login,
                    'content': r.content,
                    'date': str(r.created_at.date())
                }
                data['reactions'].append(reaction_data)
                pprint.pprint(data)


if __name__ == '__main__':
    main()
