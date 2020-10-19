# %%
import os
import numpy as np
import pandas as pd
import matplotlib as plt

# we can name our rows and columns an refer to them by name
# we don't have to have just 1 datatype

# Three things - Series, DataFrames, Indices

# loc is using row names, iloc is using row numbers
# %% 9/29 in class exercise
data = np.ones((7,3))
data_frame = pd.DataFrame(data, 
                columns = ['data1', 'data2', 'data3'],
                index=['a','b','c','d','e','f','g'])
print(data)
print(data_frame)

# %% A) Change the values for all of the vowel rows to 3

#Method1
data_frame.loc["a"] *= 3
data_frame.loc["e"] *= 3
print(data_frame)

#Method2 - changes data not dataframe
data[0:1] = [3., 3., 3.]
data[4:5] = [3., 3., 3.]
print(data)

#Method3 - using mask with conditional statement
data[(data_frame.index=='a') | (data_frame.index=='e')]=3
print(data)

#Method4 - using list of row names []
data_frame.loc[['a','e']]=3

# %% B) multiply the first 4 rows by 7

#method1
data_frame.loc[['a','b','c','d']]*=7
print(data_frame)

#method2
data_frame=data_frame.iloc[:4,:] * 7


# %% C) Make the dataframe into a checkerboard  of 0's and 1's using loc
data_frame.loc[['a','c','e','g'],['data1','data3']]=0
data_frame.loc[['b','d','f'],['data2']]=1
print(data_frame)

# %% D) Do the same thing without using loc
data_frame.iloc[0:8:2,0:3:2] = 0
data_frame.iloc[1:8:2,1:3:2] = 1
print(data_frame)
# %%
