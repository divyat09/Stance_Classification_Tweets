# encoding=utf8
import urllib
import pandas as pd
from collections import Counter
import re

#These will contain the special features for the 4 secondary targets 
A=[]
B=[]
C=[]
D=[]

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
	
	print target,"\t",count,"\n"	
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

	if pmi_word==pmi_word_t1 and pmi_word>= 0.9 :
		A.append(word)	
		#print word,"\t",count,"\n","\n"
	
	if pmi_word==pmi_word_t2 and pmi_word>= 0.9 :
		B.append(word)
		#print word,"\t",count,"\n","\n"

	if pmi_word==pmi_word_t3 and pmi_word>= 0.9 :
		C.append(word)
		#print word,"\t",count,"\n","\n"
	
	if pmi_word==pmi_word_t4 and pmi_word>= 0.9 :
		D.append(word)		
		#print word,"\t",count,"\n","\n"	
		
	print word,"\t",count,"\n","\n"	



#Build the Feature Set from List of Knowledege Sources
def Features():

	list_words_1=['Medical Care','Liberal','Women Health','Healthcare','Profeminist', 'Prochoice','Bodily Autonomy', 'Rapeculture','Rape','Win for women','ReproductiveRights','Feminist','Feminism','ReproRights','Right','choose','right to choose','prochoice']
	list_words_2=['promarriage','Mother Teresa','Death Penalty','Baby','Children','Murder','Kill','Killing', 'Fight for Unborn', 'ProLife' , 'Promurder', 'ProLifeYouth', 'Protect Voiceless' , 'Life','Protect Life', 'Legalised Murder', 'Human Life', 'Hitler','Humanity', 'Unborn', 'Life','Voiceless','Human','Innocent']
	list_words_3=['God', 'Catholic', 'God’s Laws','Religious Rights','ReligiousRights','Jesus','Bible','Christian','Christianity','Church','Prayer']
	list_words_4=['Fostering','Adoption','Adopt']
	list_hashtag_1=['#Feminism','#Rapeculture', '#WomensRights', '#ReproductiveRights', '#MyBodyMyRights', '#Reprojustice', '#Reprorights', '#Rape', '#YourBody', '#AbortionRight', '#NoChoiceIsNeverEasy', '#womenshealth','#prochoice', '#reprohealth', '#ReproJustice']
	list_hashtag_2=['#murder', '#voiceless', '#AbortionIsMurder', '#prolifegen', '#ProLifeYouth', '#killing', '#child',  '#Life', '#Mother', '#InnocentLives', '#ProtectLife', '#LifeIsBeautiful', '#AllLivesMatter', '#BlackLivesMatter', '#LifeWins' , '#Unborn' , '#MotherTeresa', '#ISIS']
	list_hashtag_3=['#jesus', '#bible', '#God','#Catholic', '#Christian','Christianity']
	list_hashtag_4=['#adopt','#adoption']
	list_words=list_words_1+list_words_2+list_words_3+list_words_4
	list_hashtags=list_hashtag_1+list_hashtag_2+list_hashtag_3+list_hashtag_4
	
	list_total=list_words+list_hashtags
	# Replace sequences of whitespace and Lowercase
	list_total = [re.sub("\s", "", t.lower()) for t in list_total]
	
	for item in list_total:
		pmi(item)		
		
	#print A,"\n",B,"\n",C,"\n",D
	#print 'total features before',"\t",len(list_words)+len(list_hashtags),"\n"
	#print 'total features now',"\t",len(A)+len(B)+len(C)+len(D)
	feature_set=A+B+C+D
	return feature_set



#data=pd.read_csv('/home/divyat/Desktop/RTE/Data/TrainingData/training_data_1.csv', delimiter="\t", quoting=3)
data=pd.read_excel('/home/divyat/Desktop/RTE/Data/TrainingData/Training_Set.xlsx', index_col=None, na_values=['NA'] )
#Making list of all tweets 
tweets=[]

for item in data['Tweet']:
	tweets.append(str(item))
# Replace sequences of whitespace and lowercase.
tweets = [re.sub("\s", "", t.lower()) for t in tweets]

print Features()



