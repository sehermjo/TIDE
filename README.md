# TIDE
Challenge submission

##How to run
- `git clone` repo
- place serialized json twitter-tweets in `tweets.txt` in \tweet_input
- in root dir run `bash run.sh`
- wait for calculations
- \tweet_output should contain `ft1.txt` and `ft2.txt` files containing transformed data

##Dependencies
Requires python 2.7 to run.

##TODO:
- add unit tests of `tweets_cleaned.py`,`average_degree.py`, and `tweet_utils.py`

##Future improvements:
- investigate whether [isjon](https://pypi.python.org/pypi/ijson) can bed used to short the parsing process so only relevant fields are parsed.
- improve speed by changing to a better algorithm

##License
- MIT
