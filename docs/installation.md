# Installation Instructions

## Install Python and VirtualEnv

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

## Setup the project

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
