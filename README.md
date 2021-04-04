# Reddit Ticker Scrapper 🚀
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) [![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Search a given subreddit for the most mentioned tickers.

## Setup 🔨

### Prerequisites
Install poetry (Linux)
```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```

Install poetry (Windows)
```bash
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python -
```

### Install Dependencies
```bash
poetry install --no-dev
```

### Reddit API Setup
Follow this guide at
https://github.com/reddit-archive/reddit/wiki/OAuth2#getting-started to get your `CLIENT_ID` and `CLIENT_SECRET`. Then create a file named `.env` and put the following content.
```
CLIENT_ID='<YOUR CLIENT ID>'
CLIENT_SECRET='<YOUR CLIENT SECRET>'
```

## Usage 📖
```
➜ poetry run ./reddit_ticker_scrapper/reddit_ticker_scrapper.py --help
Usage: main.py [OPTIONS] SUBREDDIT

  Search SUBREDDIT for most mentioned tickers.

Options:
  -p, --post-limit INTEGER RANGE  Number of posts to parse.
  -c, --comment-limit INTEGER RANGE
                                  Number of comments to parse in each post. -1
                                  to parse all comments, 0 to parse no
                                  comments.

  -n, --num-top-tickers INTEGER RANGE
                                  Number of top tickers to print.
  -e, --excluded PATH             Text file containing words that are excluded
                                  because they are mistaken as tickers.

  -t, --tickers PATH              CSV containing all tickers.
  -o, --output PATH               The filename of the csv of ticker counts.
  --help                          Show this message and exit.
```
### Example
```
➜ poetry run ./reddit_ticker_scrapper/reddit_ticker_scrapper.py wallstreetbets
Searching r/wallstreetbets...
Ticker                                              Company  Frequency
   GME                    GameStop Corporation Common Stock        341
  PLTR      Palantir Technologies Inc. Class A Common Stock        105
   RKT           Rocket Companies Inc. Class A Common Stock         88
   AMC AMC Entertainment Holdings Inc. Class A Common Stock         37
    BB                      BlackBerry Limited Common Stock         33
    MS                          Morgan Stanley Common Stock         13
  TSLA                              Tesla Inc. Common Stock         13
  VIAC                  ViacomCBS Inc. Class B Common Stock         12
    CS       Credit Suisse Group American Depositary Shares         11
    IT                            Gartner Inc. Common Stock         10
```
### Crypto Tickers Example
To find crypto tickers supply the crypto tickers csv via the `-t` option.
```
➜ poetry run ./reddit_ticker_scrapper/reddit_ticker_scrapper.py -t data/crypto_tickers.csv SatoshiStreetBets
Searching r/SatoshiStreetBets...
Ticker                 Coin Name  Frequency
   GET Guaranteed Entrance Token         23
   BSC                  BowsCoin         22
   ETH                  Ethereum         18
   NFT                       NFT         18
  STPT               STP Network         11
  HOGE              Hoge Finance         10
   UBX              UBIX Network          9
   BNB              Binance Coin          8
   BTT                BitTorrent          8
   BOG                   Bogcoin          7
```
#### Refreshing Crypto Tickers
Run `poetry run ./get_crypto_tickers.py`, it will pull the latest crypto tickers and write to `data/crypto_tickers.csv`.
