# Installation Instructions


## Setup system environment

Install Python and pip

- For Linux
   ```bash
   $ sudo apt-get install python3
   ```
- For Mac
   ```bash
   $ brew install python@3
   ```

Install virtualvenv

```bash
$ pip3 install virtualenv
```


## Setup project environment

1. Clone the repo.
   ```bash
   $ git clone git@github.com:MichaelCurrin/aggre-git.git
   $ cd aggre-git
   ```
2. Create a `virtualenv` environment. Make sure it is activated when installing project dependencies or running the project application.
   ```bash
   $ virtualenv -p python3 venv
   $ source venv/bin/activate
   ```
3. Install Python packages
   ```bash
   $ pip install -r requirements.txt
   ```

## Configure the project


1. Go to the [Tokens](https://github.com/settings/tokens) page within the Developer Settings area of your Github account.
2. Create a new token. The following scopes are recommended:
    * repo
    * user
        - read
        - email
    * org
        - read
    * discussion
        - read
3. Copy the generated token value.
4. Create a config file which contains your token.
    ```bash
    $ TOKEN=PASTEYOURTOKENHERE
    $ echo "ACCESS_TOKEN = '$TOKEN'" > aggregit/etc/configlocal.py
    ```

_TODO: Setting up config file_
