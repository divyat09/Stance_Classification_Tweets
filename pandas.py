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

#print the elelment under column target of 3rd row
print data["Target"].loc[2]

#print some specific columns combined by passing a list containing name of those columns inside that list
print data[["Target","Tweet"]]

#the dataype of all the columns of data
#print data.dty
	
#Take a subset of datindex=index+1a frame with column Local Target having only value Baby Rights
data1=data[data["Local Target"]=='Baby Rights']
print data1.shape

#Replacing all the Nan values with None Values
index=0
for item in data["Local Target"].isnull():
	if item==True:
		data["Local Target"].loc[index]='NONE'
	index=index+1

#You can even directly use this function instead of your own code to replace all the Nan values
data["Local Target"].fillna('NONE')

#Writing data from a pandas data frame to xlsx file

# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter('/home/divyat/Desktop/RTE/Data/TrainingData/Training_Set_New.xlsx', engine='xlsxwriter')
# Convert the dataframe to an XlsxWriter Excel object.
data.to_excel(writer, sheet_name='Sheet1')
# Close the Pandas Excel writer and output the Excel file.
writer.save()
workbook =writer.book
worksheet =writer.sheets['Sheet1']

