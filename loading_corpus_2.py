import urllib
import pandas as pd

#data=pd.read_csv('/home/divyat/Desktop/RTE/Data/TrainingData/training_data_1.csv', delimiter="\t", quoting=3)
data=pd.read_excel('/home/divyat/Desktop/RTE/Data/TrainingData/Training_Set.xlsx', index_col=None, na_values=['NA'] )

#print all the columns
print data.columns

#print dimensions of data
print data.shape

#total number of rows
print data.shape[0]

#print the 3rd row: this commands a object of Data Type Series
print data.loc[2]

#print specific rows by passing a list as an argument 
print data.loc[[1,10,19]]

#print the column Target
print data["Target"]

#print some specific columns combined by passing a list containing name of those columns inside that list
print data[["Target","Tweet"]]


#print the data type of all the columns of data
#print data.dtype

#Take a subset of data frame with column Local Target having only value Baby Rights
data=data[data["Local Target"]=='Baby Rights']
print data.shape