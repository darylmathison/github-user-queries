#!/usr/bin/env bash

echo "Running with the devil"
python -m unittest discover -s tests -t .
exit 2
