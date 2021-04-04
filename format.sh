#!/bin/sh
poetry run isort reddit_ticker_scrapper/ tests/
poetry run black reddit_ticker_scrapper/ tests/