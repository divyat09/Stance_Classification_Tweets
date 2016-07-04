import nltk
from nltk import word_tokenize
import urllib
import pandas as pd

#You cannot tokenise a xlsx file but you can tokenize a csv file
#data=pd.read_excel('/home/divyat/Desktop/RTE/Data/TrainingData/Training_Set.xlsx', index_col=None, na_values=['NA'] )

f=open('/home/divyat/Desktop/RTE/Data/TrainingData/training_data_1.csv', 'rU')
text=f.read()
text1=text.split()
abstracts=nltk.text(text1)
