# Installation Instructions

## Project Requirements

You need the following to run this project:

- GitHub account
- GitHub API token with access to repos
- Internet connection
- Python 3.6+


## Install project dependencies

It is usually best-practice in Python projects to install into a sandboxed _virtual environment_, which is set to a specific Python version and contains on the packages you install into it so that your Python projects do not get affected.

Follow this guide to [Setup a Python 3 Virtual Environment](https://gist.github.com/MichaelCurrin/3a4d14ba1763b4d6a1884f56a01412b7). 

You can then continue to the [Usage](/docs/usage.md) doc.


## Configure the project

### Create local config file

1. Create a config file using the template.
    ```bash
    $ cd aggregit/etc
    $ cp configlocal.template.py configlocal.py
    ```
2. Open the file with a text editor.
    ```bash
    $ edit configlocal.py
    ```
3. You can leave or the override in the `configlocal.py` based on your requirements. To set the `ACCESS_TOKEN` value, see below.


### Set your token

The minimum requirement to run the project is to create a Github token for your account and set it locally.

1. Go to the [Tokens](https://github.com/settings/tokens) page within the Developer Settings area of your Github account.
1. Create a new token. The following scopes are recommended to be set:
    * ☑ repo 
        - Tick the top level for access to private repos. Otherwise just tick _repo:status_ and _public:repo_.
    * ☐ admin:org
        - ☑ read:org
    * ☐ write:discussion
        - ☑ read:discussion
    * ☐ user
        - ☑ read
        - ☑ email
1. Copy the generated token value.
1. Open `configlocal.py` and paste your value for `ACCESS_TOKEN`.
