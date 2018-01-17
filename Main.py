import re
import pandas as pd
import sklearn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import svm
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from collections import Counter
import numpy as np
import random


def make_matrix(tweets, features):
    matrix = []
    row=[]
    for tweet in tweets:
        for feature in features:
        	#Each element of row is count of feature in tweet
        	row.append(tweet.count(feature))	
        matrix.append(row)
        row=[]

    df = pd.DataFrame(matrix)
    df.columns = features
    
    return df


def Label(df,target):
	label=[]
	for item in df[target]:
		label.append(str(item))
	return label
		
def Tweets(df):
	tweet=[]
	for item in df['Tweet']:
		tweet.append(str(item))

	removelist="#"
	# Lowercase, then replace any non-letter, space, or digit character in the headlines except Hashtag
	tweet = [re.sub(r'[^\w\s\d'+removelist+']','',t.lower()) for t in tweet]
	# Replace sequences of whitespace with a space character.
	tweet = [re.sub("\s+", " ", t) for t in tweet]
	# Replace all spaces in string
	tweet = [re.sub(" ", "", t) for t in tweet]

	return tweet

def Features(target):
	
	f=open('/home/divyat/Desktop/RTE/Data/TrainingData/'+target+'.txt','r')
	feature_set=f.read().split("\n")
	feature=[]
	for item in feature_set:
		feature.append(item)
	f.close()

	return feature

def Analysis(clf,matrix,label,target,Classes):
	
	index=0
	error=0
	for item in clf.predict(matrix):
		#If item in predicted label set is not same as the item in label set at the same index
		if item!=label[index]:
			error=error+1
		index=index+1

	f=open('/home/divyat/Desktop/RTE/Data/TrainingData/Analysis.txt','a')

	f.write('Analysis for '+target+'\n'+'\n')
	#Calculate the count of each class
	for Class in Classes:
		#It counts the no of times item appears in the label set
		f.write('Old Count of'+Class+':  '+str(label.count(Class))+'\n')
		#It counts the no of times item appears in the predicted label set
		f.write('New Count of'+Class+':  '+str(clf.predict(matrix).tolist().count(Class))+'\n'+'\n')
		
	f.write('Total Wrong Cases: '+ str(error)+"\n")
	f.write('Accuracy: '+ str(clf.score(matrix,label,sample_weight=None)) +'\n'+'\n')
	f.close()

def train_svm_stance(target,sec_target):

	#If No element in data frame with specified secondary target
	if not target in sec_target:
		return 0
	#Taking data specific to the target
	sub_data=data[target==sec_target]
	#Making list of all tweets 
	sub_tweets=Tweets(sub_data)
	#Feature Set made by selecting words with high pmi from all the words form tweets
	sub_features =Features(target)
	#Convert the tweets into feature vectors and make a matrix of feature vectors
	sub_matrix=make_matrix(sub_tweets,sub_features)
	
	#Mark the classes of training set tweets for training the SVM
	sub_label=Label(sub_data,'Stance')

	#Implementing the Support Vector Machine
	clf = svm.SVC(kernel='linear')
	print clf
	#Train the SVM on training data using the sub_label
	clf.fit(sub_matrix, sub_label) 

	#Analysis on Trained SVM
	#Analysis(clf,sub_matrix,sub_label,target,['FAVOR','AGAINST','NONE'])

	return clf

def train_svm(tweets,features):
	
	'''			
	#Adding some meta features
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
	'''
	#Convert the tweets into feature vectors and make a matrix of feature vectors
	matrix=make_matrix(tweets,features)
	#Mark the classes of training set tweets for training the SVM
	label=Label(data,'Local Target')
	
	#Implementing the Support Vector Machine
	clf = svm.SVC(kernel='linear')
	print clf
	#Train the classfier for predicitng the secondary targets using the labelled secondary targets in label list
	clf.fit(matrix, label)

	#Analysis on Trained SVM for secondary target classification
 	#Analysis(clf,matrix,label,'Secondary Targets',['Baby Rights','Women Rights','Christianity','Adoption','Abortion','Other'])
	
	#Train the Stance Classifier for each of the subsets we have made using Secondary Targets 
	clf1=train_svm_stance('Baby Rights',clf.predict(matrix))
	clf2=train_svm_stance('Women Rights',clf.predict(matrix))
	#clf3=train_svm_stance('Christianity',clf.predict(matrix))
	clf4=train_svm_stance('Adoption',clf.predict(matrix))
	clf5=train_svm_stance('Abortion',clf.predict(matrix))
	clf6=train_svm_stance('Other',clf.predict(matrix))
	#Making a list of all classifiers to use for predicting over test data
	classifiers =[]
	classifiers.append(clf)
	classifiers.append(clf1)
	classifiers.append(clf2)
	#classifiers.append(clf3)
	classifiers.append(clf4)
	classifiers.append(clf5)
	classifiers.append(clf6)

	#Check if a classifier is not eympty or we had no data available in trainnig set for that particular secondary target
	for item in classifiers:
		if item==0:
			classifiers.remove(item)
	
	return classifiers

#Main Code Starts Here

#Reading the data into data frame objects from excel sheets 
data=pd.read_excel('/home/divyat/Desktop/RTE/Data/TrainingData/Training_Set_New.xlsx', index_col=None, na_values=['NA'] )
data_test=pd.read_excel('/home/divyat/Desktop/RTE/Data/TestData/test_data.xlsx', index_col=None, na_values=['NA'] )

#Making list of all tweets 
tweets=Tweets(data)
#Feature Set made by selecting words with high pmi from all the words form tweets
features = Features('features')

#Train SVM classifier to classify tweets into secondary targets
classifiers=train_svm(tweets, features)

#Making list of all tweets in test set
test_tweets=Tweets(data_test)
#Convert the tweets into feature vectors and make a matrix of feature vectors which  serve as an input to classifier trained on Training Data
matrix=make_matrix(test_tweets,features)

#Predicting Stance for the Test Data 
stance_predicted=[]
list_target=['Baby Rights','Women Rights','Christianity','Adoption','Abortion','Other']

#Secondary Target Classification of Test Tweets
target_predicted=classifiers[0].predict(matrix)
#Check if a particular secondary target occurs in list of secondary targets predicted for the training data
for item in list_target:
	if not item in target_predicted:
		list_target.remove(item)

#Predicting Stance for test Set by looping over the list of secondary targets in the predicted secondary target list 
for i in range(0,len(classifiers)-1):

	#Making new data test specific to a secondary target
	new_data=data_test[list_target[i]==target_predicted]
	#Making list of all tweets specific to a secondary category
	new_tweets=Tweets(new_data)
	#Making list of features specific to a secondary category
	new_features=Features(list_target[i])
	#Making matrix specific to a secondary target
	new_matrix=make_matrix(new_tweets,new_features)
	
	stance_predicted=stance_predicted + classifiers[i+1].predict(new_matrix).tolist()

#Adding the secondary targets and stance prediced to the Test Set
data_test['Target_Predicted'] = pd.Series(target_predicted, index=data_test.index)
data_test['Stance_Predicted'] = pd.Series(np.asarray(stance_predicted), index=data_test.index)

# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter('/home/divyat/Desktop/RTE/Data/TestData/test_data.xlsx', engine='xlsxwriter')
# Convert the dataframe to an XlsxWriter Excel object.
data_test.to_excel(writer, sheet_name='Sheet1')
# Close the Pandas Excel writer and output the Excel file.
writer.save()
