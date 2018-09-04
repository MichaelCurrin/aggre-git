"""
Sample organization module.
"""
from etc import config
from lib.connection import CONN


o = CONN.get_organization(config.ORGANIZATION)

events = list(o.get_events())
members = list(o.get_members())
issues = list(o.get_issues())
repos = list(o.get_repos())
print('Events: {}'.format(len(events)))
print('Members: {}'.format(len(members)))
print('Issues: {}'.format(len(issues)))
print('Repos: {}'.format(len(repos)))

teams = o.get_teams()

print("All teams and member count")
for t in teams:
    print(t.name, t.members_count)
print()

print("Actual members for configured teams")
for t in teams:
    if t.name in config.TEAMS:
        print(t.name)
        members = [("@{}".format(u.login), u.name if u.name else "N/A",
                    u.company if u.company else "N/A")
                   for u in t.get_members()]
        for m in members:
            print(*m)
        print()
