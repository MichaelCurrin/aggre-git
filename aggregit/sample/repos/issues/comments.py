"""
Sample repo issue comments module.
"""
from etc import config
from lib.connection import CONN


def main():
    for repo_name in config.REPO_PATHS:
        repo = CONN.get_repo(repo_name)
        print(repo.name)

        for comment in repo.get_issues_comments():
            data = {'username': comment.user.login,
                    'date': str(comment.created_at.date())}
            print(data)
        print()


if __name__ == '__main__':
    main()
