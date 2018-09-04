# Installation Instructions

## Install OS dependencies

### For Linux

```bash
$ sudo apt-get install python3
$ pip3 install virtualenv
```

### For Mac OS-X

```bash
$ brew install python@3
$ pip3 install virtualenv
```

## Install packages

```bash
$ git clone git@github.com:MichaelCurrin/aggre-git.git
$ cd aggre-git
```

Create the virtualenv environment. Make sure it is activated when installing project dependencies or running the project application.

```bash
$ virtualenv -p python3 venv
$ source venv/bin/activate
```

```bash
$ pip install -r requirements
```

## Configure the project


1. Go to [Tokens](https://github.com/settings/tokens) within the Developer Settings area of your Github account.
2. Create a new token. The following scopes are recommended:
    * repo
    * user
        - read
        - email
    * org
        - read
    * discussion
        - read
3. Copy the generated token.
4. Create a config file which contains your token.
    ```bash
    $ TOKEN=PASTEYOURTOKENHERE
    $ echo "ACCESS_TOKEN = '$TOKEN'" > aggregate/etc/config.py
    ```

_TODO: Setting up config file_
