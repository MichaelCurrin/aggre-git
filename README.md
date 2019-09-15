# Aggre-Git
> Report on aggregated Github activity data, based around PRs and users within your organization


## Purpose

This project reports on data from the Github API. It creates PR report and a commit report CSV using input parameters.

The project uses the V3 REST API, which works fine for light reporting but does not scale well. Especially for reporting on commits, as to fetch 5000 commits takes 5000 requests, which time-consuming and uses the hourly API limit.

Therefore, if you want to do reporting at scale, rather use this project, which makes use of the V4 GraphQL API.

- [Github GraphQL Tool](https://github.com/MichaelCurrin/github-graphql-tool)


## Documentation

See the following within the [docs](/docs/) directory:

- [Installation](docs/installation.md)
- [Usage](docs/usage.md)

For collaborators - if you want to make the project better, see the [contribution guidelines](CONTRIBUTING.md).

For info on the _PyGithub_ library, go to their [docs](https://pygithub.readthedocs.io/en/latest/) and their [examples](https://pygithub.readthedocs.io/en/latest/examples.html) of library usage.
