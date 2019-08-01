#!/usr/bin/env bash

pip install bandit
bandit -ll -r GitHubUserQuery.py app && python -m unittest discover -s tests -t .
