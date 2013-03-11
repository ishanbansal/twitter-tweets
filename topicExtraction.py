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
logging.basicConfig(filename='logname2',mode='w',format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from gensim import corpora, models, similarities
from BeautifulSoup import BeautifulSoup
from sets import Set

def latent_lsi(fout3):
		fin=open('reply_corpus','r')
		documents=fin.read().split(',')	
		fi=open('stopwords.txt','r')
		stoplist = set(fi.read().split())
		texts = [[word for word in document.lower().split() if word not in stoplist]
			 for document in documents]
		#print texts
		dictionary = corpora.Dictionary(texts)
		dictionary.save('/tmp/deerwester3.dict') # store the dictionary, for future reference
		#print dictionary.token2id
		corpus = [dictionary.doc2bow(text) for text in texts]
		corpora.MmCorpus.serialize('/tmp/deerwester3.mm', corpus) # store to disk, for later use
		#from gensim import corpora, models, similarities
		dictionary = corpora.Dictionary.load('/tmp/deerwester3.dict')
		corpus = corpora.MmCorpus('/tmp/deerwester3.mm')
		#print corpus
		tfidf = models.TfidfModel(corpus) # step 1 -- initialize a model
		corpus_tfidf = tfidf[corpus]
		lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=1) # initialize an LSI transformation
		#lda = models.ldamodel.LdaModel(corpus_tfidf, id2word=dictionary, num_topics=1, update_every=1, chunksize=10000,passes=1)
		#lda.print_topics(20)		
		corpus_lsi = lsi[corpus_tfidf]
		lsi.print_topics(0)
		#line for line in open('logname2') if 'apple' in line
		print("LSI topic:")
		contents=[ line for line in open('logname2') if 'topic' in line]
		print contents
		fout3.writelines([ line for line in open('logname2') if 'topic' in line])
		fout4= open('logname2','w')
		fout4.close()
		fin.close()
		fi.close()

def latent_lda(fout3):
		fin=open('reply_corpus','r')
		documents=fin.read().split(',')	
		fi=open('stopwords.txt','r')
		stoplist = set(fi.read().split())
		texts = [[word for word in document.lower().split() if word not in stoplist]
			 for document in documents]
		#print texts
		dictionary = corpora.Dictionary(texts)
		dictionary.save('/tmp/deerwester3.dict') # store the dictionary, for future reference
		#print dictionary.token2id
		corpus = [dictionary.doc2bow(text) for text in texts]
		corpora.MmCorpus.serialize('/tmp/deerwester3.mm', corpus) # store to disk, for later use
		#from gensim import corpora, models, similarities
		dictionary = corpora.Dictionary.load('/tmp/deerwester3.dict')
		corpus = corpora.MmCorpus('/tmp/deerwester3.mm')
		#print corpus
		tfidf = models.TfidfModel(corpus) # step 1 -- initialize a model
		corpus_tfidf = tfidf[corpus]
#		lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=1) # initialize an LSI transformation
		lda = models.ldamodel.LdaModel(corpus_tfidf, id2word=dictionary, num_topics=1, update_every=1, chunksize=10000,passes=1)
		lda.print_topics(0)		
		#corpus_lsi = lsi[corpus_tfidf]
#		lsi.print_topics(0)
		#line for line in open('logname2') if 'apple' in line
		print("LDA topic:")
		contents=[ line for line in open('logname2') if 'topic #0' in line]
		print contents
		fout3.writelines([ line for line in open('logname2') if 'topic #0' in line])
		fout4= open('logname2','w')
		fout4.close()
		fin.close()
		fi.close()


