import os
from collections import deque
from tweet_utils import parseJson as parseJson
from tweet_utils import replaceControlChars as replaceControlChars
import datetime as dt

tweetPath = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'tweet_input/tweets.txt'))
feature2FilePath = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'tweet_output/ft2.txt'))

graph = {} #simple adjacency list data structure
tweetWindow = deque() #maintains the 60 second window of tweets' tags and iso-timestamps
def updateGrapWith(tweet):
	
	#convert time to iso format, escape non-standard TZ-offset, assume UTC.
	tweetTime =  dt.datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')

	if len(tweet['entities']['hashtags']) > 1:
		#remove unicode and upper/lower-case equivalents
		tweetTags = [replaceControlChars(tag['text'].encode('ascii','ignore')).lower() for tag in tweet['entities']['hashtags']]
		tweetTags = set(tweetTags)
		tweet = { 'time': tweetTime, 'hashtags': tweetTags }
	else:			
		tweet = { 'time': tweetTime, 'hashtags': [] }
	
	if len(tweet['hashtags']) < 2:
		tweet = { 'time': tweetTime }
		tweetWindow.append(tweet)
	else:
		tweetWindow.append(tweet)
		for tag in tweetTags:
			if not tag in graph: graph[tag] = []
			adjacentTags = [adjTag for adjTag in tweetTags if (adjTag != tag)]
			graph[tag].extend(adjacentTags) #the same adjacency can exists multiple times for tracking purposes
			
	while ((tweetTime - tweetWindow[0]["time"]).total_seconds() > 60):
		evictedTweet = tweetWindow.popleft()
		if 'hashtags' in evictedTweet:
			adjacenciesToRemove = evictedTweet['hashtags']
			for tag in adjacenciesToRemove:
				tagsCopy = set(adjacenciesToRemove)
				tagsCopy.remove(tag)
				for toRemove in tagsCopy:
					graph[tag].remove(toRemove)
					if not graph[tag]: del graph[tag]
	return graph	

def main():
	outputFile = open(feature2FilePath, "w")
	
	with open(tweetPath, "r") as tweetLines:
		for line in tweetLines:
			possibleTweet = parseJson(line)
			
			#check if is tweet. Assume valid tweets cotains 'created_at' and 'entities.hashtags' according to https://dev.twitter.com/overview/api/tweets field guide
			if (('created_at' in possibleTweet) and ('entities' in possibleTweet) and ('hashtags' in possibleTweet['entities'])):	
				graph = updateGrapWith(possibleTweet)
				avgDegree = float(0)
				if graph:
					#remove multiple adjacencies use to track mutiple tweets
					trueGraph = { vertice: set(edges) for (vertice, edges) in graph.iteritems() }
					#calculate avg_deg
					avgDegree = float(sum([len(edges) for edges in trueGraph.values()])) / len(graph)
					
				average_degree = "{0:.2f}".format(avgDegree)	
				
				outputFile.write('%s\n' % average_degree)

if __name__ == "__main__":
    main()
