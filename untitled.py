import nltk
reply_text = 'naman is a good boy. I love him. John big idea isnt all that bad.'
nltk_word = nltk.word_tokenize(reply_text)
nltk_word = nltk.pos_tag(nltk_word)
print nltk_word
