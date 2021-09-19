# Usage

You may with to occasionally change your configured settings. See [Configure the project](installation.md#configure-the-project) instructions.

```sh
$ cd path/to/repo
$ source venv/bin/activate
$ cd aggregit
```

All remaining commands expect to start from the [aggregit](/aggregit) directory.


## Reports

### Pull Request

```bash
$ ./pr_report.py
```

### Samples

The project contains sample scripts for explorations and demonstration of PyGithub functionality, with some parsing and aggregation logic. They are not maintained much but are kept for easy references for working examples focused on a particular area such as a User, Pull Request or Event.

The scripts must be imported as modules. They do not take arguments. Example usage is shown below for a few in the [sample](/aggregit/sample) directory.

```bash
$ python -m sample.user
```

```bash
$ python -m sample.repos.issues.issues
```

Some of the sample reports could become overview reports in the main part of the project. They will not have activity associated with them. For example:

- Repos and teams in an organization.
- Repos in a team.
- Users in a team.
