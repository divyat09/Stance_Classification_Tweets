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
from sklearn import svm
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

#Calculate the count of word specificially when it occurs with the Target
def count_word_target(word,target):
	count=0
	index=[]	

	#Taking a subset from data so that only those rows are taken which have target in Local Target column
	for item in data['Local Target']:
		item=str(item).lower().replace(" ","")
		index.append(target in item)
	data_sub=data[index] 

	#Making list of all tweets_sub 
	tweets_sub=[]
	for item in data_sub['Tweet']:
		tweets_sub.append(str(item))
	# Replace sequences of whitespace and lowercase
	tweets_sub = [re.sub("\s", "", t.lower()) for t in tweets_sub]
	

	#No of times the word occurs in Tweet column of new data set where all values in Local Target column contain target	
	for item in tweets_sub:
		if  word in item:			
			count=count+1	
	
	#print target,"\t",count,"\n"	
	return count

#Calculate the PMI of a knowledge source and determine if it to be selected for the feature set
def pmi(word):
	count=0
	pmi_word_t1=0
	pmi_word_t2=0
	pmi_word_t3=0
	pmi_word_t4=0
	pmi_word=0

    #Total count of word in the Tweet column of data
	for item in tweets:
		if  word in item:
			count=count+1
	#print word,"\t",count,"\n","\n"	

	target='babyrights'	
	if count!=0:	
		pmi_word_t1=count_word_target(word,target)/float(count)
	
	target='womenrights'	
	if count!=0:	
		pmi_word_t2=count_word_target(word,target)/float(count)

	target='christianity'	
	if count!=0:	
		pmi_word_t3=count_word_target(word,target)/float(count)

	target='adoption'	
	if count!=0:	
		pmi_word_t4=count_word_target(word,target)/float(count)		
	
	pmi_word=max(pmi_word_t1,pmi_word_t2,pmi_word_t3,pmi_word_t4)

	if pmi_word==pmi_word_t1 and pmi_word>= 0.85 and count>=3 :
		return word	
		
	if pmi_word==pmi_word_t2 and pmi_word>= 0.85 and count>=2:
		return word
		
	if pmi_word==pmi_word_t3 and pmi_word>= 0.85 :
		return word
		
	if pmi_word==pmi_word_t4 and pmi_word>= 0.85 and count>=3 :
		return word		
					
	return 0

#Build the Feature Set from List of Knowledege Sources
def Features():

	feature_set=[]

	list_words_1=['Medical Care','Liberal','liberalism','Women Health','Health','Profeminist', 'Prochoice','Bodily Autonomy', 'Rapeculture','Rape','Win for women','ReproductiveRights','Reproductive Health','Feminist','Feminism','ReproRights','Right','choose', 'Pregnancy']
	list_words_2=['promarriage','Mother Teresa','Death Penalty','Baby','Child','Murder','Kill', 'ProLife' , 'Promurder', 'ProLifeYouth','ProLifeGen','Probaby', 'Protect Voiceless' , 'Life','Protect Life', 'Legalised Murder', 'Human Life', 'Hitler','Humanity', 'Unborn','Voiceless','Human','Innocent']
	list_words_3=['God','atheism','atheist','Catholic','Religious','Jesus','Bible','Christian','Church','Prayer']
	list_words_4=['Fostering','Adoption','Adopt']
	list_hashtag_1=['#SCOTUS','#Feminism','#Rapeculture', '#WomensRights', '#ReproductiveRights', '#MyBodyMyRights', '#Reprojustice','#womensrights', '#Reprorights', '#Rape','#prochoice' '#YourBody', '#AbortionRight','#womenshealth','#prochoice', '#reprohealth',"#RightToChoose"]
	list_hashtag_2=['#murder', '#voiceless', '#AbortionIsMurder', '#prolife', '#ProLifeYouth','#ProLifeGen', '#killing', '#child', '#Life', '#Mother', '#InnocentLives', '#ProtectLife', '#LifeIsBeautiful', '#AllLivesMatter', '#BlackLivesMatter', '#LifeWins' , '#Unborn' , '#MotherTeresa', '#ISIS']
	list_hashtag_3=['#jesus', '#bible', '#God','#Catholic', '#Christian','Christianity']
	list_hashtag_4=['#adopt','#adoption']
	
	list_words=list_words_1+list_words_2+list_words_3+list_words_4
	list_hashtags=list_hashtag_1+list_hashtag_2+list_hashtag_3+list_hashtag_4
	list_total=list_words+list_hashtags
	# Replace sequences of whitespace and Lowercase
	list_total = [re.sub("\s", "", t.lower()) for t in list_total]
	
	for item in list_total:
		word=pmi(item)
		if word!=0:
			feature_set.append(word)

	return feature_set


def make_matrix(tweets, vocab):
    matrix = []
    row=[]
    for tweet in tweets:
        for w in vocab:
        	row.append(tweet.count(w))	
        matrix.append(row)
        print row
        row=[]
       

    df = pd.DataFrame(matrix)
    df.columns = vocab
    return df


#Main Code Starts Here


data=pd.read_excel('/home/divyat/Desktop/RTE/Data/TrainingData/Training_Set.xlsx', index_col=None, na_values=['NA'] )

#Making list of all tweets 
tweets=[]
for item in data['Tweet']:
	tweets.append(str(item))
# Replace sequences of whitespace with a space character.
tweets = [re.sub("\s", "", t.lower()) for t in tweets]

#Feature Set
'''
features_words=['bodilyautonomy','rapeculture','reproductiverights','reprorights','murder','prolifegen','humanlife','unborn','atheism','adopt']
features_hashtags=['#feminism','#rapeculture','#reproductiverights','#reprorights','#rape','#abortionright','#murder','#prolifegen','#child','#life','#alllivesmatter','#unborn','#motherteresa','#god','#adopt']
features=features_words+features_hashtags
'''
features=Features()
matrix=make_matrix(tweets,features)

label=[]
for item in data['Local Target']:
	label.append(str(item))

transform_functions= [
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

#print matrix.shape
#print meta.shape 

clf = svm.SVC()
clf.fit(matrix, label) 
index=0

for item in clf.predict(matrix):
	print item

