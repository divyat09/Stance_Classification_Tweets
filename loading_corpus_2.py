import urllib
import pandas as pd

#data=pd.read_csv('/home/divyat/Desktop/RTE/Data/TrainingData/training_data_1.csv', delimiter="\t", quoting=3)
data=pd.read_excel('/home/divyat/Desktop/RTE/Data/TrainingData/training_data_1.xlsx', index_col=None, na_values=['NA'] )

print data.columns
print data.shape
