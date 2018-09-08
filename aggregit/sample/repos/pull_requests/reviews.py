"""
Sample repo pull request reviews module.

https://developer.github.com/v3/pulls/
"""
from etc import config
from lib.connection import CONN


def main():
    for repo_name in config.REPOS:
        repo = CONN.get_repo(repo_name)
        print(repo.name)
        print()

        prs = repo.get_pulls()

        for pr in prs:
            print(pr.title)

            reviews = list(pr.get_reviews())
            if reviews:
                for rev in reviews:
                    # 'COMMENTED' 'APPROVED' 'DISMISSED' 'CHANGES_REQUESTED'
                    print(rev.state)
                    print(str(rev.submitted_at.date()))
                    print(rev.user.login)
            else:
                print('skip')
            print()


if __name__ == '__main__':
    main()


