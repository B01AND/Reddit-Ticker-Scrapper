"""Fixtures for tests"""
import pandas as pd
import pytest


@pytest.fixture
def excluded_words():
    """
    Returns a list of words that are excluded because they are mistaken as tickers.
    """
    return {"YOLO", "DD"}


@pytest.fixture
def tickers_df():
    """
    Returns a Dataframe of Stock Tickers.
    """
    tickers = {"TSLA": "Tesla", "APPL": "Apple"}
    return pd.DataFrame.from_dict(tickers.items()).rename(columns={0: "Ticker", 1: "Company"})
