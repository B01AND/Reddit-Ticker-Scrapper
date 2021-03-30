#!/usr/bin/env python3
"""Search a subreddit for the most mentioned tickers.

The program pulls in the specified number (defaults to 50) of 'hot' posts and their comments
(defaults to 1000) from the given subreddit and calculates the frequency of mentions for
each ticker found.
"""
import itertools
import re
from typing import Dict, List, Set

import click
import pandas as pd
from dotenv import dotenv_values
from praw import Reddit

regex = re.compile(r'[^\$a-zA-Z ]')


def increment_count(frequencies: Dict[str, int], word: str) -> None:
    """Helper function to increment frequency count of word.

    Args:
        frequencies: The dictionary containing the frequency count of all words.
        word: The word to increment the count of.
    """
    if word in frequencies:
        frequencies[word] += 1
    else:
        frequencies[word] = 1


def preprocess_text(text: str) -> List[str]:
    """Removes symbols and split text into list of words.

    Removes characters other than alphabets, space and $ sign first
    and then the text is split into a list of words. The $ sign is kept
    because it is used to denote a ticker, Eg $TSLA.

    Args:
        text: The text string to be processed.

    Returns:
        The list of words extracted from the text.
    """
    return regex.sub('', text).split(' ')


def count_words(excluded_words: Set, frequencies: Dict[str, int], words: List[str]) -> None:
    """Count the frequencies of a list of words.

    Args:
        excluded_words: Words that are excluded because they are mistaken as tickers.
        frequencies: Dictionary that stores the frequencies of words.
        words: List of words to be counted.
    """
    for word in words:
        if word.startswith('$'):  # words that starts with $ are tickers and should not be exclueded
            increment_count(frequencies, word[1:])
        elif word in excluded_words:
            pass
        else:
            increment_count(frequencies, word)


def filter_tickers(frequencies: Dict[str, int], ticker_df: pd.DataFrame) -> pd.DataFrame:
    """Filter out non tickers from a dict of words.

    Args:
        frequencies: The dictionary containing the frequency count of all words.
        ticker_df: Dataframe of all tickers.

    Returns:
        Dataframe of tickers that have at least 1 occurance and their occurance frequency.
    """
    word_df = pd.DataFrame.from_dict(frequencies.items()).rename(columns={0: 'Ticker', 1: 'Frequency'})
    return pd.merge(ticker_df, word_df, on='Ticker').sort_values('Frequency', ascending=False)


def find_tickers(reddit: Reddit, excluded_words: Set, ticker_df: pd.DataFrame, subreddit: str, post_limit: int, comment_limit: int) -> pd.DataFrame:
    """Find tickers from subreddit.

    Tickers written in lowercase will not be found.

    Args:
        reddit: PRAW Reddit instance.
        excluded_words: Words that are excluded because they are mistaken as tickers.
        ticker_df: Dataframe of all tickers.
        subreddit: The subreddit to search for tickers from.
        post_limit: Number of posts to parse.
        comment_limit: Number of comments to parse in each post.

    Returns:
        Dataframe of tickers that have at least 1 occurance and their occurance frequency.
    """
    frequencies: Dict[str, int] = {}
    for post in reddit.subreddit(subreddit).hot(limit=post_limit):
        words = preprocess_text(f'{post.title} {post.selftext}')
        count_words(excluded_words, frequencies, words)

        post.comments.replace_more(limit=0)  # only process post top level comments
        if comment_limit != -1:
            for comment in itertools.islice(post.comments, comment_limit):
                count_words(excluded_words, frequencies, preprocess_text(comment.body))
        else:
            for comment in post.comments:
                count_words(excluded_words, frequencies, preprocess_text(comment.body))

    return filter_tickers(frequencies, ticker_df)


@click.command()
@click.option('--post-limit', '-p', type=click.IntRange(min=1), default=50, help='Number of posts to parse.')
@click.option('--comment-limit',
              '-c',
              type=click.IntRange(min=-1),
              default=1000,
              help='Number of comments to parse in each post. -1 to parse all comments, 0 to parse no comments.')
@click.option('--num-top-tickers', '-n', type=click.IntRange(min=1), default=10, help='Number of top tickers to print.')
@click.option('--excluded',
              '-e',
              type=click.Path(exists=True),
              default='./data/excluded.txt',
              help='Text file containing words that are excluded because they are mistaken as tickers.')
@click.option('--tickers', '-t', type=click.Path(exists=True), default='./data/tickers.csv', help='CSV containing all tickers.')
@click.option('--output', '-o', type=click.Path(file_okay=True, writable=True), help='The filename of the csv of ticker counts.')
@click.argument('subreddit', type=str)
def main(**kwargs):
    """Search SUBREDDIT for most mentioned tickers."""
    secrets = dotenv_values('.env')
    reddit = Reddit(client_id=secrets['CLIENT_ID'], client_secret=secrets['CLIENT_SECRET'], user_agent='Scrapper (by /u/PotatoDrug)')

    with open(kwargs['excluded'], 'r') as f:
        excluded_words = set(f.read().splitlines())
    ticker_df = pd.read_csv(kwargs['tickers'])
    print(f'Searching r/{kwargs["subreddit"]}...')

    stonks_df = find_tickers(reddit, excluded_words, ticker_df, kwargs['subreddit'], kwargs['post_limit'], kwargs['comment_limit'])

    if kwargs['output'] is not None:
        stonks_df.to_csv(kwargs['output'], index=False)

    print(stonks_df.head(kwargs['num_top_tickers']).to_string(index=False))


if __name__ == '__main__':
    main()
