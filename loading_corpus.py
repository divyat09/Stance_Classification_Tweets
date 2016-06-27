import nltk
from nltk.book import *
f=open('/home/divyat/Desktop/RTE/Data/SemEval2016-Task6-testdata/SemEval2016-Task6-subtaskA-testdata.txt','rU')
text=f.read()
text1=text.split()
abstracts=nltk.Text(text1)
