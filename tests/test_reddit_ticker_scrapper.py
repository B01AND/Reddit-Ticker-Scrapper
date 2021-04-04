"""Tests for reddit_ticker_scrapper"""
from unittest.mock import MagicMock

import pandas as pd
from pandas._testing import assert_frame_equal

from reddit_ticker_scrapper.reddit_ticker_scrapper import (
    count_words,
    filter_tickers,
    find_tickers,
    increment_count,
    preprocess_text,
)


def test_preprocess_text():
    text = "HELLO world"
    assert preprocess_text(text) == ["HELLO", "world"]


def test_preprocess_text_remove_punctuations():
    text = "HELLO world, this is good."
    assert preprocess_text(text) == ["HELLO", "world", "this", "is", "good"]


def test_preprocess_text_keep_dollarsign():
    text = "HELLO world, this is good. $YOLO"
    assert preprocess_text(text) == ["HELLO", "world", "this", "is", "good", "$YOLO"]


def test_increment_count_empty_key():
    frequencies = {}
    increment_count(frequencies, "")
    assert frequencies == {"": 1}


def test_increment_count_existing_key():
    frequencies = {"hello": 1}
    increment_count(frequencies, "hello")
    assert frequencies == {"hello": 2}


def test_increment_count_nonexistent_key():
    frequencies = {"hello": 1}
    increment_count(frequencies, "world")
    assert frequencies == {"hello": 1, "world": 1}


def test_count_words(excluded_words):
    frequencies = {}
    words = ["hello", "world", "hello"]
    count_words(excluded_words, frequencies, words)
    assert frequencies == {"hello": 2, "world": 1}


def test_count_words_excluded(excluded_words):
    frequencies = {}
    words = ["hello", "world", "YOLO"]
    count_words(excluded_words, frequencies, words)
    assert frequencies == {"hello": 1, "world": 1}


def test_count_words_none(excluded_words):
    frequencies = {}
    words = []
    count_words(excluded_words, frequencies, words)
    assert frequencies == {}


def test_filter_tickers_positive(tickers_df):
    frequencies = {"hello": 2, "world": 1, "TSLA": 5}
    result = [{"Ticker": "TSLA", "Company": "Tesla", "Frequency": 5}]
    result_df = pd.DataFrame(result)
    assert_frame_equal(filter_tickers(frequencies, tickers_df), result_df)


def test_filter_tickers_none(tickers_df):
    frequencies = {"hello": 2, "world": 1}
    df = filter_tickers(frequencies, tickers_df)
    assert df.shape[0] == 0


def test_find_tickers_none(excluded_words, tickers_df):
    mock_reddit = MagicMock()
    mock_reddit.subreddit.return_value = mock_subreddit = MagicMock()

    mock_post = MagicMock()
    mock_post.title = "Hello World"
    mock_post.selftext = "This is content"
    mock_post.comments = MagicMock(return_value=iter(["This is a comment", "This is another comment"]))
    mock_subreddit.hot.return_value = iter((mock_post, mock_post))
    df = find_tickers(mock_reddit, excluded_words, tickers_df, "wallstreetbets", 10, 5)
    assert df.shape[0] == 0


def test_find_tickers_positive_title(excluded_words, tickers_df):
    mock_reddit = MagicMock()
    mock_reddit.subreddit.return_value = mock_subreddit = MagicMock()

    mock_post = MagicMock()
    mock_post.title = "The Title TSLA"
    mock_post.selftext = "This is content"
    mock_post.comments = MagicMock(return_value=iter(["This is a comment", "This is another comment"]))
    mock_subreddit.hot.return_value = iter((mock_post, mock_post))
    df = find_tickers(mock_reddit, excluded_words, tickers_df, "wallstreetbets", 10, 5)
    assert df.shape[0] == 1


def test_find_tickers_positive_content(excluded_words, tickers_df):
    mock_reddit = MagicMock()
    mock_reddit.subreddit.return_value = mock_subreddit = MagicMock()

    mock_post = MagicMock()
    mock_post.title = "The Title"
    mock_post.selftext = "This is content TSLA"
    mock_post.comments = MagicMock(return_value=iter(["This is a comment", "This is another comment"]))
    mock_subreddit.hot.return_value = iter((mock_post, mock_post))
    df = find_tickers(mock_reddit, excluded_words, tickers_df, "wallstreetbets", 10, 5)
    assert df.shape[0] == 1


def test_find_tickers_positive_comments(excluded_words, tickers_df):
    mock_reddit = MagicMock()
    mock_reddit.subreddit.return_value = mock_subreddit = MagicMock()

    mock_post = MagicMock()
    mock_post.title = "The Title"
    mock_post.selftext = "This is content"
    mock_post.comments = mock_comments = MagicMock()
    mock_comment_1 = MagicMock()
    mock_comment_1.body = "This is a comment TSLA"
    mock_comment_2 = MagicMock()
    mock_comment_2.body = "This is a comment APPL"
    mock_comments.__iter__.return_value = iter([mock_comment_1, mock_comment_2])
    mock_comments.replace_more.return_value = True
    mock_subreddit.hot.return_value = iter((mock_post, mock_post))
    df = find_tickers(mock_reddit, excluded_words, tickers_df, "wallstreetbets", 10, 5)
    assert df.shape[0] == 2
