# Start of Laura's code, modified file namd and path

# Start code for assignment 3
# this code sets up the lists you will need for your homework
# and provides some examples of operations that will be helpful to you

# %%
# Import the modules we will use
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# %%
# ** MODIFY **
# Set the file name and path to where you have stored the data
filename = 'streamflow_week3.txt'
filepath = os.path.join('../data', filename) # Go up one directory from current and then find data folder
print(os.getcwd())
print(filepath)

# %%
# DON'T change this part -- this creates the lists you 
# should use for the rest of the assignment
# no need to worry about how this is being done now we will cover
# this in later sections. 

#Read the data into a pandas dataframe
data=pd.read_table(filepath, sep = '\t', skiprows=30,
        names=['agency_cd', 'site_no', 'datetime', 'flow', 'code']
        )

# Expand the dates to year month day
data[["year", "month", "day"]] =data["datetime"].str.split("-", expand=True)
data['year'] = data['year'].astype(int)
data['month'] = data['month'].astype(int)
data['day'] = data['day'].astype(int)

#make lists of the data
flow = data.flow.values.tolist()
date = data.datetime.values.tolist()
year = data.year.values.tolist()
month = data.month.values.tolist()
day = data.day.values.tolist()

# Getting rid of the pandas dataframe since we wont be using it this week
del(data)

# %%
# Here is some starter code to illustrate some things you might like to do
# Modify this however you would like to do your homework. 
# From here on out you should use only the lists created in the last block:
# flow, date, yaer, month and day

# Calculating some basic properites
print(min(flow))
print(max(flow))
print(np.mean(flow))
print(np.std(flow))

# Making and empty list that I will use to store
# index values I'm interested in
ilist = []

# Loop over the length of the flow list
# and adding the index value to the ilist
# if it meets some criteria that I specify
for i in range(len(flow)):
        if flow [i] > 600 and month[i] == 7:
                ilist.append(i)

# see how many times the criteria was met by checking the length
# of the index list that was generated
print(len(ilist))

# Alternatively I could have  written the for loop I used 
# above to  create ilist like this
ilist2 = [i for i in range(len(flow)) if flow[i] > 600 and month[i]==7]
print(len(ilist2))

# Grabbing out the data that met the criteria
# This  subset of data is just the elements identified 
# in the ilist
subset = [flow[j] for j in ilist]

## Start of Mekha's code for Assignment Questions

# %% Question 1 - Data types
print(type(flow))
print(type(flow[0]))
print(type(year[0]))
print(type(month[0]))
print(type(day[0]))
print(len(flow))

# %% 
# Question 2 - How many times flow exceed 300 cfs in September
ilist3 = [i for i in range(len(flow)) if flow[i] > 300 and month[i]==9]
print(len(ilist3))

ilist4 = [i for i in range(len(flow)) if month[i]==9]
print(len(ilist4))

print(len(ilist3)/len(ilist4)*100)

# %% 
# Question 3 How many times flow exceed 300 cfs in September 1989 - 2000
ilist5 = [i for i in range(len(flow)) if flow[i] > 300 and month[i]==9 and year[i] < 2001]
print(len(ilist5))

ilist6 = [i for i in range(len(flow)) if month[i]==9 and year[i] < 2001]
print(len(ilist6))

print(len(ilist5)/len(ilist6)*100)

# Question 3 How many times flow exceed 300 cfs in September 2010 - 2020
ilist7 = [i for i in range(len(flow)) if flow[i] > 300 and month[i]==9 and year[i] > 2009]
print(len(ilist7))

ilist8 = [i for i in range(len(flow)) if month[i]==9 and year[i] > 2009]
print(len(ilist8))

print(len(ilist7)/len(ilist8)*100)

# %%
# Question 4 Change in flow first half Sept to second

#First half month flows
ilist9 = [i for i in range(len(flow)) if month[i]==9 and year[i] < 2020 and day[i] < 16]

Sept_first = [flow[j] for j in ilist9]

print(min(Sept_first))
print(max(Sept_first))
print(np.mean(Sept_first))
print(np.std(Sept_first))

#Second half month flows
ilist10 = [i for i in range(len(flow)) if month[i]==9 and year[i] < 2020 and day[i] > 15]

Sept_second = [flow[j] for j in ilist10]

print(min(Sept_second))
print(max(Sept_second))
print(np.mean(Sept_second))
print(np.std(Sept_second))

## Start of Mekha's code for forecast

# %%
# Code for 1 and 2 week forecast
# Near-term forecast will be made by looking closely at the most recent weeks of data

# Look at previous week data for Sept 6-12
ilist11 = [i for i in range(len(flow)) if month[i]==9 and day[i] > 5 and day[i] < 13 and year[i] == 2020]

flow_recent = [flow[j] for j in ilist11]

print(min(flow_recent))
print(max(flow_recent))
print(np.mean(flow_recent))
print(np.std(flow_recent))

# %%
# Plot most recent two weeks of flow to look at recent trend
date.index('2020-09-12') #find index of most recent date
date_2wk = date[11564:11578] 
flow_2wk = flow[11564:11578]
fig, ax = plt.subplots(figsize=(14, 14))
ax.bar(date_2wk, flow_2wk, color="aqua")
ax.set(title="Daily Flow cfs",
       xlabel="Date", 
       ylabel="Flow cfs")
plt.show()

# %%
# Code for long term forecast
# Look at weekly avg for each week in forecast by changing variable year from 1989-2019
# Choose low flow year to base predictions on since we know this has been a dry monsoon season

HistoricalYr = 2019

# Data for 8/22-8/29
ilist12 = [i for i in range(len(flow)) if month[i]==8 and day[i] >= 22 and day[i]<=28 and year[i]==HistoricalYr]
Week1 = [flow[j] for j in ilist12]

# 8/30 - 9/5
ilist13 = [i for i in range(len(flow)) if ((month[i]==8 and day[i] >= 30) or (month[i]==9 and day[i]<=5)) and year[i]==HistoricalYr]
Week2 = [flow[j] for j in ilist13]

# 9/6/20 9/12/20
ilist14 = [i for i in range(len(flow)) if month[i]==9 and day[i] >= 6 and day[i]<=12 and year[i]==HistoricalYr]
Week3 = [flow[j] for j in ilist14]

# 9/13/20 9/19/20
ilist15 = [i for i in range(len(flow)) if month[i]==9 and day[i] >= 13 and day[i]<=19 and year[i]==HistoricalYr]
Week4 = [flow[j] for j in ilist15]

# 9/20/20 9/26/20
ilist16 = [i for i in range(len(flow)) if month[i]==9 and day[i] >= 20 and day[i]<=26 and year[i]==HistoricalYr]
Week5 = [flow[j] for j in ilist16]

# 9/27/20 10/3/20
ilist17 = [i for i in range(len(flow)) if ((month[i]==9 and day[i] >= 27) or (month[i]==10 and day[i]<=3)) and year[i]==HistoricalYr]
Week6 = [flow[j] for j in ilist17]

# 10/4/20 10/10/20
ilist18 = [i for i in range(len(flow)) if month[i]==10 and day[i] >= 4 and day[i]<=10 and year[i]==HistoricalYr]
Week7 = [flow[j] for j in ilist18]

# 10/11/20 10/17/20
ilist19 = [i for i in range(len(flow)) if month[i]==10 and day[i] >= 11 and day[i]<=17 and year[i]==HistoricalYr]
Week8 = [flow[j] for j in ilist19]

# 10/18/20 10/24/20
ilist20 = [i for i in range(len(flow)) if month[i]==10 and day[i] >= 18 and day[i]<=24 and year[i]==HistoricalYr]
Week9 = [flow[j] for j in ilist20]

#  10/25/20 10/31/20
ilist21 = [i for i in range(len(flow)) if month[i]==10 and day[i] >= 25 and day[i]<=31 and year[i]==HistoricalYr]
Week10 = [flow[j] for j in ilist21]

# 11/1/20 11/7/20
ilist22 = [i for i in range(len(flow)) if month[i]==11 and day[i] >= 1 and day[i]<=7 and year[i]==HistoricalYr]
Week11 = [flow[j] for j in ilist22]

# 11/8/20 11/14/20
ilist23 = [i for i in range(len(flow)) if month[i]==11 and day[i] >= 8 and day[i]<=14 and year[i]==HistoricalYr]
Week12 = [flow[j] for j in ilist23]

# 11/15/20 11/21/20
ilist24 = [i for i in range(len(flow)) if month[i]==11 and day[i] >= 15 and day[i]<=21 and year[i]==HistoricalYr]
Week13 = [flow[j] for j in ilist24]

# 11/22/20 11/28/20
ilist25 = [i for i in range(len(flow)) if month[i]==11 and day[i] >= 22 and day[i]<=28 and year[i]==HistoricalYr]
Week14 = [flow[j] for j in ilist25]

# 11/29/20 12/5/20
ilist26 = [i for i in range(len(flow)) if ((month[i]==11 and day[i] >= 29) or (month[i]==12 and day[i]<=5)) and year[i]==HistoricalYr]
Week15 = [flow[j] for j in ilist26]

# 12/6/20 12/12/20
ilist27 = [i for i in range(len(flow)) if month[i]==12 and day[i] >= 6 and day[i]<=12 and year[i]==HistoricalYr]
Week16 = [flow[j] for j in ilist27]


print(np.mean(Week1))
print(np.mean(Week2))
print(np.mean(Week3))
print(np.mean(Week4))
print(np.mean(Week5))
print(np.mean(Week6))
print(np.mean(Week7))
print(np.mean(Week8))
print(np.mean(Week9))
print(np.mean(Week10))
print(np.mean(Week11))
print(np.mean(Week12))
print(np.mean(Week13))
print(np.mean(Week14))
print(np.mean(Week15))
print(np.mean(Week16))


# %%
