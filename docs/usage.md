# Usage

You may with to occasionally change your configured settings. See [Configure the project](installation.md#configure-the-project) instructions.

```sh
$ source venv/bin/activate
```


## Reports

### Pull Request report

```sh
$ cd aggregit
$ ./pr_report.py
```

### Commit report

```sh
$ cd aggregit
$ ./commit_report.py
```

### Open source PRs report

Windows:

```python
$ cd aggregit
$ python -m sample.repos.search.issues
```

Linux and macOS, using `make`:

```console
$ make open-source-prs
Total
140
By month view - 7 months
Month   | PRs
---     | ---
2021-12 |   1
2021-11 |   6
2021-10 |   4
2021-09 |  11
2021-08 |  12
2021-07 |  17
2021-06 |  20

Detailed view - 3 items
{'closed_at': datetime.datetime(2021, 12, 1, 23, 56, 24),
 'created_at': datetime.datetime(2021, 12, 1, 11, 1, 27),
 'repo': 'create-pull-request',
 'state': 'closed',
 'title': 'docs: update marketplace logo',
 'url': 'https://github.com/peter-evans/create-pull-request/pull/992'}
{'closed_at': datetime.datetime(2021, 11, 27, 8, 59, 47),
 'created_at': datetime.datetime(2021, 11, 26, 20, 30, 1),
 'repo': 'clintjb.github.io',
 'state': 'closed',
 'title': 'Update a350_csv.html',
 'url': 'https://github.com/clintjb/clintjb.github.io/pull/4'}
{'closed_at': datetime.datetime(2021, 11, 29, 18, 12, 33),
 'created_at': datetime.datetime(2021, 11, 25, 20, 22, 26),
 'repo': 'jekyll-github-sample',
 'state': 'closed',
 'title': 'Update README.md',
 'url': 'https://github.com/bwillis/jekyll-github-sample/pull/25'}
```

<!-- The above is in the `samples` directory, but could moved out -->

### Samples

The project contains sample scripts for explorations and demonstration of PyGithub functionality, with some parsing and aggregation logic. They are not maintained much but are kept for easy references for working examples focused on a particular area such as a User, Pull Request or Event.

The scripts must be imported as modules. They do not take arguments. 

Example usage is shown below for a few in the [sample](/aggregit/sample/) directory.

```sh
$ cd aggregit
$ python -m sample.user
```

```sh
$ cd aggregit
$ python -m sample.repos.issues.issues
```

Some of the sample reports could become overview reports in the main part of the project. They will not have activity associated with them. For example:

- Repos and teams in an organization.
- Repos in a team.
- Users in a team.
