# Aggre-Git
> Report on aggregated Github activity data, based around PRs and users within your organization

[![GitHub tag](https://img.shields.io/github/tag/MichaelCurrin/aggre-git)](https://github.com/MichaelCurrin/aggre-git/tags/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](#license)

- Report on historical Github activity for your user or organization. 
- Reads from the Github REST API, accessed through a Python library called PyGithub - see [homepage](https://pygithub.readthedocs.io/en/latest/introduction.html) and [Github repo](https://github.com/PyGithub/PyGithub).


## Purpose

This project reports on data from the Github API. It creates PR report and a commit report CSV using input parameters.

The project uses the V3 REST API, which works fine for light reporting. But performs poorly at scale - for a commit report on a given branch, it takes 5000 requests to fetch 5000 commits. That is slow to run and also means you are likely to exceed the API rate limit of 5000 requests per hour.

Therefore if you want to do reporting at scale, use this other project instead. It makes use of the Github V4 GraphQL API so scales well.

- [Github GraphQL Tool](https://github.com/MichaelCurrin/github-graphql-tool)


## Documentation

See the following within the [docs](/docs/) directory:

- [Installation](/docs/installation.md)
- [Usage](/docs/usage.md)

For collaborators - if you want to make the project better, see the [contribution guidelines](CONTRIBUTING.md).

For info on the _PyGithub_ library, go to their [docs](https://pygithub.readthedocs.io/en/latest/) and their [examples](https://pygithub.readthedocs.io/en/latest/examples.html) of library usage.


## License

Released under [MIT](/LICENSE).
