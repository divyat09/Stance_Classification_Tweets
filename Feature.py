import re
import pandas as pd
from collections import Counter

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

	#Making list of all tweets 
	tweets_sub=[]
	for item in data_sub['Tweet']:
		tweets_sub.append(str(item))

	removelist="#"
	# Lowercase, then replace any non-letter, space, or digit character in the headlines except Hashtag
	tweets_sub = [re.sub(r'[^\w\s\d'+removelist+']','',t.lower()) for t in tweets_sub]
	
	# Replace all spaces in string
	tweets_sub = [re.sub("\s+", " ", t) for t in tweets_sub]
	tweets_sub = [re.sub(" ", "", t) for t in tweets_sub]

	#No of times the word occurs in Tweet column of new data set where all values in Local Target column contain target	
	for item in tweets_sub:
		if  word in item:			
			count=count+1	
	
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
	print word,"\t",count,"\n","\n"	
	#Find the PMI of each word with various targets
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
	
	#Select the class which has max PMI for word and further checks for PMI	
	pmi_word=max(pmi_word_t1,pmi_word_t2,pmi_word_t3,pmi_word_t4)

	if pmi_word==pmi_word_t1 and pmi_word>= 0.65 :
		return word	
		
	if pmi_word==pmi_word_t2 and pmi_word>= 0.65 :
		return word
		
	if pmi_word==pmi_word_t3 and pmi_word>= 0.65 :
		return word
		
	if pmi_word==pmi_word_t4 and pmi_word>= 0.65 :
		return word		
					
	#Return value to show that this word is not right to selected in the feature set				
	return 0

#Build the Feature Set from List of Knowledege Sources
def Features(feature_set):
	
	features=[]
	list_total=[]
	'''
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
	'''
	list_total=feature_set
	for item in list_total:
		word=pmi(item)
		if word!=0:
			features.append(word)

	return features

def stance_feature_set(target):
	#Making list of all tweets 
	sub_data=data[target==data['Local Target']]
	sub_tweets=[]
	for item in sub_data['Tweet']:
		sub_tweets.append(str(item))

	removelist="#"
	# Lowercase, then replace any non-letter, space, or digit character in the headlines except Hashtag from tweets
	sub_tweets = [re.sub(r'[^\w\s\d'+removelist+']','',t.lower()) for t in sub_tweets]
	# Replace sequences of whitespace with a space character from tweets so that we can split it into words using " "
	sub_tweets = [re.sub("\s+", " ", t) for t in sub_tweets]

	#Feature Set made by selecting all the words form tweets
	sub_feature_set = list(set(" ".join(sub_tweets).split(" ")))	

	#Removing StopWords from our feaure set as they are useless and wont yeild much 
	f =open('/home/divyat/Desktop/RTE/Data/TrainingData/stop_words.txt','r')
	stop_words=f.read().split('\n')
	sub_feature_set = [w for w in sub_feature_set if w not in stop_words]	

	#Printing the result to a file
	f=open('/home/divyat/Desktop/RTE/Data/TrainingData/'+target+'.txt','w')
	for item in sub_feature_set:
		print item
		f.write(item+'\n')
	f.close()

def target_feature_set():

	#Feature Set made by selecting all the words form tweets
	feature_set = list(set(" ".join(tweets).split(" ")))	

	#Removing StopWords from our feaure set as they are useless and wont yeild much 
	f =open('/home/divyat/Desktop/RTE/Data/TrainingData/stop_words.txt','r')
	stop_words=f.read().split('\n')
	feature_set = [w for w in feature_set if w not in stop_words]	

	#Selecting features with high pmi from list of feature_set
	features= Features(feature_set)
	print len(features)

	#Printing the result to a file
	f=open('/home/divyat/Desktop/RTE/Data/TrainingData/features.txt','w')
	for item in features:
		print item
		f.write(item+'\n')
	f.close()	


#Main Code Starts Here

#Making some global variables
data=pd.read_excel('/home/divyat/Desktop/RTE/Data/TrainingData/Training_Set_New.xlsx', index_col=None, na_values=['NA'] )

#Making list of all tweets 
tweets=[]
for item in data['Tweet']:
	tweets.append(str(item))

removelist="#"
# Lowercase, then replace any non-letter, space, or digit character in the headlines except Hashtag from tweets
tweets = [re.sub(r'[^\w\s\d'+removelist+']','',t.lower()) for t in tweets]
# Replace sequences of whitespace with a space character from tweets so that we can split it into words using " "
tweets = [re.sub("\s+", " ", t) for t in tweets]

#Making features for case of classifying tweeets into their secondary targets
target_feature_set()

#Making features for specific case of stance analysis after I have classified all tweets into their secondary targets
stance_feature_set('Baby Rights')
stance_feature_set('Women Rights')
stance_feature_set('Christianity')
stance_feature_set('Adoption')
stance_feature_set('Abortion')
stance_feature_set('Other')
