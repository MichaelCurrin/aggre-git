# Installation Instructions


## Setup system environment

Note that **Python 3.6** or higher is required to run this project.

- For Linux
   ```bash
   $ sudo apt-get install python3
   ```
- For Mac
   ```bash
   $ brew install python@3
   ```


## Setup project environment

1. Clone the repo.
   ```bash
   $ git clone git@github.com:MichaelCurrin/aggre-git.git
   $ cd aggre-git
   ```
2. Create a virtual environment named `venv`. Make sure it is activated whenever installing project dependencies or running the project application.
   ```bash
   $ python3 -m venv venv
   $ source venv/bin/activate
   ```
3. Install Python packages.
   ```bash
   $ pip install --upgrade pip
   $ pip install -r requirements.txt
   ```

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
2. Create a new token. The following scopes are recommended to be set:
    * ☐ repo
       - ☑ repo:status
       - ☑ public:repo
    * ☐ admin:org
        - ☑ read:org
    * ☐ write:discussion
        - ☑ read:discussion
    * ☐ user
        - ☑ read
        - ☑ email
3. Copy the generated token value.
4. Open `configlocal.py` and paste your value for `ACCESS_TOKEN`.
