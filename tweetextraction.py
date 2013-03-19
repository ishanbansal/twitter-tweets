import tweepy
import urllib2
import codecs
import re
import string
import nltk
import porter2 as porter
import correct
import urllib
import logging
import topicExtraction
logging.basicConfig(filename='logname2',mode='w',format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from gensim import corpora, models, similarities
from BeautifulSoup import BeautifulSoup
from sets import Set

consumer_key = "jNUo9Y41T7FSQPqlQhJCA"
consumer_secret = "ZQfVlxEf3SMRTjbwmv5JdjCMCuNZ6LNIjPJMMAdU"
token_key = "120139491-u26WvP3uvmi3X2Nt3CuALGUAyL7jTGx2BZot3iUo"
token_secret = "8y1M1FMFj3Fj8yDiGKyjEle4NTS0N8nnW1NDK6FyA"

consumer_keynew = "jNUo9Y41T7FSQPqlQhJCA"
consumer_secretnew = "fZQfVlxEf3SMRTjbwmv5JdjCMCuNZ6LNIjPJMMAdU"
token_keynew = "120139491-U2SbXdf2zFEofwdrx31nu72U1C3NfE5rHOcZSM2i"
token_secretnew = "mpJr6HosbTRQiLfCsX2WrmZY2L0r1HxnZPmobQWpKw"


auth = tweepy.OAuthHandler(consumer_keynew, consumer_secretnew)
auth.set_access_token(token_keynew, token_secretnew)
api = tweepy.API(auth)

#fout = codecs.open('TheEllenShow_3088testernn', encoding = 'utf-8', mode = 'a+')

def get_page(url):
	try:
		return BeautifulSoup(urllib2.urlopen(url).read())
	except:
		return ""

def get_favorite_count(text):
	content = text.find("a", {"class" : "request-favorited-popup"})
	content = content.find("strong")
	result = re.compile(r'<strong>(.*?)</strong>').findall(str(content))
	result = re.sub(r'[^0-9]', '', result[0])
	return result


def parse_reply(id_str):
	url = "https://twitter.com/priyankachopra/status/" + id_str
	return get_page(str(url))

#module to remove punctuations
def removePunctuations(reply,num):
	returnlist = []
	hashtag = []
	pattern = re.compile(r"(-)\1{1,}", re.DOTALL)
	for token in reply.split():
		#weeds out urls
		if token.startswith('http:'):
			continue
		if token.startswith('@'):
			continue
		if token.startswith('#'):
			hashtag.append(token)
		if len(pattern.findall(token)) > 0:
			continue
		for punct in string.punctuation:
			if not (punct=='#'):
				token = token.replace(punct, '')
				token = token.rstrip(punct)
			elif len(pattern.findall(token)) > 0:
				continue
		if len(token) > 0:
			returnlist.append(token.rstrip('\n'))
	if num:
		return returnlist, hashtag
	else:
		return returnlist


def word_stem_stop_word(reply_text,num):
	stopwordsfile = open('stopwords.txt')
	stopwords = stopwordsfile.read().split('\r\n')
	nltk_word = nltk.word_tokenize(reply_text)
	nltk_word = nltk.pos_tag(nltk_word)
	reply = []
	proper_nouns = Set([])
	for word, tag in nltk_word:
		if str(word.lower()) not in stopwords:
			if (tag == 'NNP' or tag == 'NNPS'):
				proper_nouns.add(word.lower())
			else:
				word = correct.correct(word)
				word = porter.stem(word)
				word = correct.correct(word)
			reply.append(word.lower())
	#print reply
	#print proper_nouns
	reply = ' '.join(reply)
	if num:
		return reply,proper_nouns
	else:
		return reply

def time_impact(text,tweet_time):
	content = text.findAll("span", {"class" : "_timestamp js-short-timestamp js-relative-timestamp"})
	relative_content = text.findAll("span", {"class" : "_timestamp js-short-timestamp "})
	if content:
		last_reply_time = BeautifulSoup(str(content[0])).findAll(text=True)
		last_reply_time = re.sub(r'[^0-9]', '', last_reply_time[0])
		return float(last_reply_time)/24
	elif relative_content:
		last_reply_time = BeautifulSoup(str(relative_content[0])).findAll(text=True)
		last_reply_time = re.sub(r'[^0-9]', '', last_reply_time[0])
		return int(last_reply_time)-int(tweet_time.day)
	else:
		return 0

def text_correction(text):
	unigrams = removePunctuations(text,0)
	ascii_word = []
	for word in unigrams:
		word = re.sub(r'[^a-zA-Z]', '', word)
		if word:
			ascii_word.append(str(word))
	reply = ' '.join(ascii_word)
	reply = word_stem_stop_word(reply,0)
	return reply

def get_replies(text):
	content = text.findAll("p", {"class" : "js-tweet-text"})
	reply_count = 0
	reply_text = ''
	proper_nouns = Set([])
	for reply in content:
		reply_count = reply_count +1
		reply = ''.join(BeautifulSoup(str(reply)).findAll(text=True))
		unigrams,hashtag = removePunctuations(reply,1)
		ascii_word = []
		for word in unigrams:
			word = re.sub(r'[^a-zA-Z]', '', word)
			if word:
				ascii_word.append(word)
		reply = ' '.join(ascii_word)
		reply,nouns = word_stem_stop_word(reply,1)
		for words in nouns:
			proper_nouns.add(words)
		for tag in hashtag:
			tag = re.sub(r'[^a-zA-Z]', '', tag)
			proper_nouns.add(tag.lower())
		if len(reply):
			reply_text = reply_text+'"'+reply+'",'
	return reply_text, reply_count, proper_nouns
	
class tweetdescription:
	def __init__(self):
		self.id_str=""
		self.title_tweet=""
		self.createdtime=""
		self.favorite_count=0
		self.retweet_count=0
		self.topic=[]
		self.reply_count=0
		self.last_reply_time=0.0

	def _add(self,id_str,title_tweet,createdtime,favorite_count,retweet_count,topic,reply_count,last_reply_time):
		self.id_str=id_str
		self.title_tweet=title_tweet
		self.createdtime=createdtime
		self.favorite_count=favorite_count
		self.retweet_count=retweet_count
		self.topic=topic
		self.reply_count=reply_count
		self.last_reply_time=last_reply_time
	
	
d=[tweetdescription()] * 10
index=0	
fout3= open('lsi','w')
fout1=open('lda','w')
for page in tweepy.Cursor(api.user_timeline, id = "priyankachopra", count =10, include_rts = 0).pages(2000):
	for item in page:
#writing entire corpus consisting of tweet and replies into reply_corpus
		fout = open('reply_corpus','w')
		#print item.text
		title_tweet = text_correction(item.text)
		print "corrected tweet : ",
		print  title_tweet #title tweet corrected
		print "status : ",		
		print item.id_str
		print "time : ",		
		print item.created_at #timestamp
		print "No of retweets : ",		
		print item.retweet_count #retweet count
		#print dir(item)
		#fout.write(unicode(item.created_at)+'\n')
		url_text = parse_reply(item.id_str)
		favorite_count = get_favorite_count(url_text) #favorite count
		print "No of favorites : ",	
		print favorite_count
		tweet_reply, reply_count, proper_nouns = get_replies(url_text)
		last_reply_time = time_impact(url_text,item.created_at)
		for x in range(0, 3):
			tweet_reply = tweet_reply+'"'+title_tweet+'",'
		
		if len(tweet_reply):
			print "tweet+reply corpus: "
			print tweet_reply  #tweet+reply corpus
			print "No of replies : ",
			print reply_count   #number of replies
			print "last reply time : ",
			print last_reply_time   #hours between first and last reply
			print "proper nouns : ",
			print proper_nouns    #set of proper nouns and hash tag
		topic=[]
		fout.write(tweet_reply)
		fout.close()
		topicExtraction.latent_lsi(fout3)#final call to lsi function topic will be saved to lsi.txt
		topicExtraction.latent_lda(fout1)#final call to lda function topic will be saved to lda.txt
		d[index]._add(item.id_str,title_tweet,item.created_at,favorite_count,item.retweet_count,topic,reply_count,last_reply_time)
		index=index+1	
		propr=open('proper','w')
		#print("printing proper nouns: ")
		#for item in proper_nouns:
			#s = urllib.urlopen('http://en.wikipedia.org/w/index.php?action=raw&title='+item).read()		
			#print>>propr,s
		 # 	print>>propr, item
		#propr.write('"'+proper_nouns+'"')#proper nouns being saved to proper.txt
		propr.close()
fout3.close()
fout1.close()
