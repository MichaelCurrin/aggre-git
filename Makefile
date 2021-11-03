default: install install-dev

all: install install-dev checks


h help:
	@grep '^[a-z]' Makefile


install:
	pip install pip --upgrade
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

upgrade:
	pip install pip --upgrade
	pip install -r requirements.txt --upgrade
	pip install -r requirements-dev.txt --upgrade


fmt-fix:
	black .
	isort .
fmt-check:
	black . --diff --check
	isort . --check

l lint:
	flake8 . --select=E9,F63,F7,F82 --show-source
	flake8 . --exit-zero

checks: fmt-check lint


open-source-prs:
	cd aggregit && \
		python -m sample.repos.search.issues
