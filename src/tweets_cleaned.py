import os
from tweet_utils import parseJson as parseJson
from tweet_utils import replaceControlChars as replaceControlChars

tweetPath = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'tweet_input/tweets.txt'))
cleanedPath = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'tweet_output/ft1.txt'))

#Test if a object is a tweet
#assume valid tweets cotains 'created_at' and 'text' according to https://dev.twitter.com/overview/api/tweets field guide
def isATweet(jsonTweet):
    return (('created_at' in jsonTweet) and ('text' in jsonTweet))

#get tweet-text and timestamp as defined
def getTextAndTimestamp(tweet):
    cleanedText = replaceControlChars(tweet["text"].encode('ascii','ignore'))
    time = tweet["created_at"]

    if tweet["text"] != cleanedText:
        getTextAndTimestamp.tweetsWithUnicode += 1

    return '%s (timestamp: %s)' % (cleanedText, time)
getTextAndTimestamp.tweetsWithUnicode = 0

def main():
    outputFile = open(cleanedPath, "w")

    with open(tweetPath, "r") as tweetLines:
        for line in tweetLines:
            possibleTweet = parseJson(line)
            if isATweet(possibleTweet):
                outputFile.write('%s\n' % getTextAndTimestamp(possibleTweet))  

    outputFile.write('%s tweets contained unicode.' % getTextAndTimestamp.tweetsWithUnicode)

if __name__ == "__main__":
    main()
