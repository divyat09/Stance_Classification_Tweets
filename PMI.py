import urllib
import pandas as pd

A=[]
B=[]
C=[]
D=[]

def count_word_target(word,target):
	count=0
	data1=data[data['Local Target']==target]		
	for item in data1['Tweet']:
		if  word.lower() in str(item).lower():			
			count=count+1	
	return count


def PMI(word):
	count=0
	pmi_word_t1=0
	pmi_word_t2=0
	pmi_word_t3=0
	pmi_word_t4=0
	pmi_word=0

	for item in data['Tweet']:
		if  word.lower() in str(item).lower():
			count=count+1
	
	target='Baby Rights'	
	if count!=0:	
		pmi_word_t1=count_word_target(word,target)/float(count)
	
	target='Women Rights'	
	if count!=0:	
		pmi_word_t2=count_word_target(word,target)/float(count)

	target='Christianity'	
	if count!=0:	
		pmi_word_t3=count_word_target(word,target)/float(count)

	target='Adoption'	
	if count!=0:	
		pmi_word_t4=count_word_target(word,target)/float(count)		
	
	pmi_word=max(pmi_word_t1,pmi_word_t2,pmi_word_t3,pmi_word_t4)

	if pmi_word==pmi_word_t1 and pmi_word>= 0.8:
		A.append(word)	
	
	if pmi_word==pmi_word_t2 and pmi_word>= 0.8:
		B.append(word)

	if pmi_word==pmi_word_t3 and pmi_word>= 0.8:
		C.append(word)
	
	if pmi_word==pmi_word_t4 and pmi_word>= 0.8:
		D.append(word)					

	print pmi_word,"\n"

count=0
#data=pd.read_csv('/home/divyat/Desktop/RTE/Data/TrainingData/training_data_1.csv', delimiter="\t", quoting=3)
data=pd.read_excel('/home/divyat/Desktop/RTE/Data/TrainingData/Training_Set.xlsx', index_col=None, na_values=['NA'] )

list_words_1=['Profeminist','Pro feminist', 'Prochoice', 'Pro choice', 'Bodily Autonomy', 'Rapeculture','Rape culture', 'Win for women','Reproductive Rights','ReproductiveRights','Feminist','Feminism','Repro Rights','ReproRights']
list_words_2=['Murder','Killing', 'Fight for Unborn', 'ProLife' , 'Promurder', 'ProLifeYouth', 'Protect Voiceless' , 'Protect Life', 'Legalised Murder', 'Human Life', 'Hitler','Humanity', 'Unborn', 'Life','Voiceless','Human']
list_words_3=['God', 'Catholic', 'God’s Laws','Religious Rights','ReligiousRights','Jesus','Bible','Christian','Christianity']
list_words_4=['Fostering','Adoption','Adopt']

list_hashtag_1=['#Feminism','#Rapeculture', '#WomensRights', '#ReproductiveRights', '#MyBodyMyRights', '#Reprojustice', '#Reprorights', '#Rape', '#YourBody', '#AbortionRight', '#NoChoiceIsNeverEasy', '#womenshealth', '#reprohealth', '#ReproJustice']
list_hashtag_2=['#murder', '#voiceless', '#AbortionIsMurder', '#prolifegen', '#ProLifeYouth', '#killing', '#child',  '#Life', '#Mother', '#InnocentLives', '#ProtectLife', '#LifeIsBeautiful', '#AllLivesMatter', '#BlackLivesMatter', '#LifeWins' , '#Unborn' , '#MotherTeresa', '#ISIS']
list_hashtag_3=['#jesus', '#bible', '#God','#Catholic', '#Christian', '#GodIsLoveSoLoveWins','Christianity']
list_hashtag_4=['#adopt','#adoption']

list_words=list_words_1+list_words_2+list_words_3+list_words_4
list_hashtags=list_hashtag_1+list_hashtag_2+list_hashtag_3+list_hashtag_4

for item in list_hashtags+list_words:
	PMI(item)		
	
for item in data['Stance']:
	 if str(item)=='NONE':
	 	count=count+1
print count
print A,"\n",B,"\n",C,"\n",D