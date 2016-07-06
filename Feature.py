import nltk
from nltk import word_tokenize
import re
import pandas as pd
import sklearn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import svm
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from collections import Counter
from sklearn.linear_model import Ridge
import numpy
import random


'''
f=open('/home/divyat/Desktop/RTE/Data/TrainingData/training_data_1.csv', 'rU')
text=f.read()
text1=text.split()
abstracts=nltk.text(text1)
'''

'''
#Making the matrix automatically using sklearn 
vectorizer = CountVectorizer(lowercase=True, stop_words="english")
matrix = vectorizer.fit_transform(list_tweets)
print matrix.shape
'''

def make_matrix(tweets, vocab):
    matrix = []
    row=[]
    for tweet in tweets:
        for w in vocab:
        	row.append(tweet.count(w))	
        matrix.append(row)
        row=[]
       

    df = pd.DataFrame(matrix)
    df.columns = vocab
    return df

data=pd.read_excel('/home/divyat/Desktop/RTE/Data/TrainingData/Training_Set.xlsx', index_col=None, na_values=['NA'] )

#Making list of all tweets 
tweets=[]
for item in data['Tweet']:
	tweets.append(str(item))
# Replace sequences of whitespace with a space character.
tweets = [re.sub("\s", "", t.lower()) for t in tweets]

#Feature Set
features=['promurder', 'protectlife', 'hitler', 'humanity', 'voiceless', '#murder', '#voiceless', '#killing', '#protectlife', '#lifeisbeautiful', '#lifewins', '#unborn', '#jesus', '#bible', 'profeminist', 'religiousrights', 'religiousrights', '#mybodymyrights', '#yourbody', '#reprohealth', 'religiousrights', 'religiousrights', '#motherteresa', 'adoption', 'adopt', '#adopt', '#adoption']

matrix=make_matrix(tweets,features)

transform_functions = [
    lambda x: len(x),
    lambda x: x.count(" "),
    lambda x: x.count("."),
    lambda x: x.count("!"),
    lambda x: x.count("?"),
    lambda x: len(x) / (x.count(" ") + 1),
    lambda x: x.count(" ") / (x.count(".") + 1),
    lambda x: len(re.findall("\d", x)),
    lambda x: len(re.findall("[A-Z]", x)),
]
columns = []
for func in transform_functions:
    columns.append(data["Tweet"].apply(func))

meta = numpy.asarray(columns)

print matrix.shape
print meta.shape



