# Example solution for HW 5

# %%
# Import the modules we will use
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# %%
# ** MODIFY **
# Set the file name and path to where you have stored the data
filename = 'streamflow_week5.txt' #modified filename
filepath = os.path.join('../data', filename) #modified path to look one directory up
print(os.getcwd())
print(filepath)

#filepath = '../Assignments/Solutions/data/streamflow_week5.txt'

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

# %%
# Sorry no more helpers past here this week, you are on your own now :) 
# Hints - you will need the functions: describe, info, groupby, sort, head and tail.

# %% Start of Mekha's code

# 1 and 2 week forecast

# Look at most recent 2 weeks of data ending 9/26
print(data.tail(14))

# Calculate avg of last two week's flow
print(data.tail(14).describe())

# Calculate avg of last week's flow
print(data.tail(7).describe())

# Look at stats for 2019 because from  my previous analysis, I know it is a smiliarly dry year
data_2019 = data[data['year']==2019]
print(data_2019['flow'].describe())

# Look at stats for 2019 by month
print(data_2019.groupby(['month'])[['flow']].describe())

# %% 1. Provide a summary of the data frames properties.
# What are the column names?
# What is its index?
# What data types do each of the columns have?
print(data.info())

# %% 2.Provide a summary of the flow column including the min, mean, max, standard 
# deviation and quartiles.
print(data['flow'].describe())

# %% 3.Provide the same information but on a monthly basis. (Note: you should be 
# able to do this with one or two lines of code)
print(data.groupby(['month'])[['flow']].describe())

# %% 4.Provide a table with the 5 highest and 5 lowest flow values for the period 
# of record. Include the date, month and flow values in your summary.

# 5 highest
print(data.sort_values(by="flow",ascending=True).tail())

# 5 lowest
print(data.sort_values(by="flow",ascending=True).head())


# %% 5.Find the highest and lowest flow values for every month of the year (i.e. you 
# will find 12 maxes and 12 mins) and report back what year these occurred in.

# highest value for each month
for i in range(1,13):
        month_data = data[data['month']==i]
        print(month_data.nlargest(1,['flow']))

# lowest value for each month
for i in range(1,13):
        month_data = data[data['month']==i]
        print(month_data.nsmallest(1,['flow']))

# %% 6.Provide a list of historical dates with flows that are within 10% of your week 1 
# forecast value. If there are none than increase the %10 window until you have at 
# least one other value and report the date and the new window you used

forecast = 58.4
data_10percent = data[(data['flow'] >= (0.9*forecast)) & (data['flow'] <= (1.1*forecast))]
pd.set_option('display.max_rows', None)
print(data_10percent['datetime'])

# %%
