# Aggre-Git
> Report on aggregated GitHub activity data, based around PRs and users within your organization

[![GitHub tag](https://img.shields.io/github/tag/MichaelCurrin/aggre-git)](https://github.com/MichaelCurrin/aggre-git/tags/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](#license)


## Features

- Report on historical GitHub activity for your user or organization.
- Read from the GitHub REST API, accessed through a Python library called _PyGithub_ - see the [homepage](https://pygithub.readthedocs.io/en/latest/introduction.html) and [GitHub repo](https://github.com/PyGithub/PyGithub).


## Purpose

This project reports on data from the GitHub API. It creates PR report and a commit report CSV using input parameters.

The project uses the V3 REST API, which works fine for light reporting. But performs poorly at scale - for a commit report on a given branch, it takes 5000 requests to fetch 5000 commits. That is slow to run and also means you are likely to exceed the API rate limit of 5000 requests per hour.

Therefore if you want to do reporting at scale, use this other project instead. It makes use of the GitHub V4 GraphQL API so scales well.

- [Github GraphQL Tool](https://github.com/MichaelCurrin/github-graphql-tool)



## Documentation

<div align="center">

[![view - Documentation](https://img.shields.io/badge/view-Documentation-blue?style=for-the-badge)](/docs/ "Go to docs")

</div>


## Contributing

If you want to make the project better, see the [contribution guidelines](/CONTRIBUTING.md).


## License

Released under [MIT](/LICENSE) by [@MichaelCurrin](https://github.com/MichaelCurrin).
