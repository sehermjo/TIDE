from json import loads as JSONparser
import re

#Clean unicode to basic latin ascii per tweet
def replaceControlCharsFunction():
    controlChars = ''.join(map(unichr, range(0,32) + range(127,160)))
    controlCharRegEx = re.compile('[%s]' % re.escape(controlChars))
    def removeControlChars(string):
        return controlCharRegEx.sub(' ', string)
    return removeControlChars
replaceControlChars = replaceControlCharsFunction()

#parse json
def parseJson(rawTweet):
    try:
        parsedTweet = JSONparser(rawTweet)
    except ValueError:
        parsedTweet = {}
    return parsedTweet
