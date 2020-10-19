# %%
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import datetime

# %%
# Given the following dataframe: data = np.random.rand(4, 5)
# Write a function and use it to calculate the mean of every column

data = np.random.rand(4, 5)

# %% Diana - using numpy ases to avergae columns without a loop (implicit, faster)
def get_mean(data):
    mymean = data.mean(axis=0)
    return mymean

get_mean(data)

# %% Jake
ans=[]
for i in range(5):
    ans.append(data[:,i].mean())

# %% Jake modified - using indexing, go col by col, slower
def get_mean2(data):
    ans=[]
    for i in range(5):
        ans.append(data[:,i].mean())
    return ans

get_mean2(data)

# %% Laura - Call function in a loop
def simple_mean(input):
    average = np.mean(input)
    return average

# this will give you avg of all the data
simple_mean(data)

# %%
# option 1, make starter array of correct size, better for troubleshooting
# average = np.zeros(5)
average = np.zeros(data.shape[1])
for i in range(data.shape[1]):
    average[i] = simple_mean(data[:,i])

# %% option 2, make an empty array and insert
average = []
for i in range(data.shape[1]):
    average.append(simple_mean(data[:,i]))

# %%
# Set the file name and path to where you have stored the data
filename = 'streamflow_week5.txt' #modified filename
filepath = os.path.join('../data', filename) #modified path to look one directory up
print(os.getcwd())
print(filepath)

# %%
#Read the data into a pandas dataframe
data=pd.read_table(filepath, sep = '\t', skiprows=30,
        names=['agency_cd', 'site_no', 'datetime', 'flow', 'code']
        )

# Expand the dates to year month day
data[["year", "month", "day"]] =data["datetime"].str.split("-", expand=True)
data['year'] = data['year'].astype(int)
data['month'] = data['month'].astype(int)
data['day'] = data['day'].astype(int)

