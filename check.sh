#!/bin/sh
poetry run yapf -i main.py
poetry run isort main.py
poetry run pylint main.py
poetry run mypy main.py