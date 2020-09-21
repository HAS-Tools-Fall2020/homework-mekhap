# Laura's starter code for Homework 4

# %%
# Import the modules we will use
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# %%
# ** MODIFY **
# Set the file name and path to where you have stored the data
filename = 'streamflow_week4.txt'
filepath = os.path.join('../data', filename) #modified path to look one directory up
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

# Make a numpy array of this data
flow_data = data[['year', 'month','day', 'flow']].to_numpy()

# Getting rid of the pandas dataframe since we wont be using it this week
del(data)

# %%
# Starter Code
# Count the number of values with flow > 600 and month ==7
flow_count = np.sum((flow_data[:,3] > 600) & (flow_data[:,1]==7))

# Calculate the average flow for these same criteria 
flow_mean = np.mean(flow_data[(flow_data[:,3] > 600) & (flow_data[:,1]==7),3])

print("Flow meets this critera", flow_count, " times")
print('And has an average value of', flow_mean, "when this is true")

# Make a histogram of data
# Use the linspace  funciton to create a set  of evenly spaced bins
mybins = np.linspace(0, 1000, num=15)
# another example using the max flow to set the upper limit for the bins
#mybins = np.linspace(0, np.max(flow_data[:,3]), num=15) 
#Plotting the histogram
plt.hist(flow_data[:,3], bins = mybins)
plt.title('Streamflow')
plt.xlabel('Flow [cfs]')
plt.ylabel('Count')

# Get the quantiles of flow
# Two different approaches ---  you should get the same answer
# just using the flow column
flow_quants1 = np.quantile(flow_data[:,3], q=[0,0.1, 0.5, 0.9])
print('Method one flow quantiles:', flow_quants1)
# Or computing on a colum by column basis 
flow_quants2 = np.quantile(flow_data, q=[0,0.1, 0.5, 0.9], axis=0)
# and then just printing out the values for the flow column
print('Method two flow quantiles:', flow_quants2[:,3])

# Start of Mekha's code for Homework 4

# Question 1 - Include discussion of the quantitative analysis that lead to your prediction. 
# This can include any analysis you complete but must include at least two histograms and some 
# quantitative discussion of flow quantiles that helped you make your decision.

# %% For initital look at recent data, create graph of two most recent weeks of data Sept 6 - 19

flow_Sept2020=flow_data[(flow_data[:,0] ==2020) & (flow_data[:,1]==9)]
plt.plot(flow_Sept2020[:,2],flow_Sept2020[:,3])
plt.title('Sept 2020 Streamflow')
plt.xlabel('Day of Sept 2020')
plt.ylabel('Daily Flow (cfs)')

# %% Last week's avg flow was 56.2 cfs (9/13-9/19). Calc % of time historically Sept flow greater than this

flow_count_56 = np.sum((flow_data[:,0] !=2020) & (flow_data[:,3] > 56.2) & (flow_data[:,1]==9))
print(flow_count_56)
flow_count_Sept1 = np.sum((flow_data[:,0] !=2020) & (flow_data[:,3] > -1) & (flow_data[:,1]==9))
print(flow_count_Sept1)
print(flow_count_56/flow_count_Sept1*100)

# %% 1 week prediction

# Histogram of Sept 20-26 flows for 1989-2019
# Create bins to only view low end of distribution

flow_wk1=flow_data[(flow_data[:,0] !=2020) & (flow_data[:,1]==9) & (flow_data[:,2]>=20) & (flow_data[:,2]<=26)]
mybins = np.linspace(0, 100, num=20)
plt.hist(flow_wk1[:,3], bins = mybins)
plt.title('Streamflow')
plt.xlabel('Flow [cfs]')
plt.ylabel('Count')

# Flow quantiles of Sept 20-26 flows
flow_quants1 = np.quantile(flow_wk1[:,3], q=[0,0.1, 0.5, 0.9])
print('Sept 20-26 flow quantiles (min, 10%, 50%, 90%):', flow_quants1)
flow_quants1a = np.quantile(flow_wk1[:,3], q=[0,0.025, 0.05, 0.1])
print('Sept 20-26 flow quantiles (min, 2.5%, 5%, 10%):', flow_quants1a)

# %% 2 week prediction

# Histogram of Sept 27- Oct 3 flows for 1989-2019
# Create bins to only view low end of distribution

flow_wk2=flow_data[(flow_data[:,0] != 2020) & ((flow_data[:,1]==9) & (flow_data[:,2]>=27)) | ((flow_data[:,1]==10) & (flow_data[:,2]<=3))]
mybins = np.linspace(0, 100, num=20)
plt.hist(flow_wk2[:,3], bins = mybins)
plt.title('Streamflow')
plt.xlabel('Flow [cfs]')
plt.ylabel('Count')

# Flow quantiles of Sept 27- Oct 3 flows
flow_quants2 = np.quantile(flow_wk2[:,3], q=[0,0.1, 0.5, 0.9])
print('Sept 27-Oct 3 flow quantiles (min, 10%, 50%, 90%):', flow_quants2)
flow_quants2a = np.quantile(flow_wk2[:,3], q=[0,0.025, 0.05, 0.1])
print('Sept 27-Oct 3 flow quantiles (min, 2.5%, 5%, 10%):', flow_quants2a)

# %% Question 2 - Variable

print(type(flow_data))
print(type(flow_data[0,0]))
print(flow_data.ndim)
print(flow_data.shape)
print(flow_data.size)

# %% Question 3 - Daily flow greater than 55 cfs in all September

flow_count_55 = np.sum((flow_data[:,3] > 55) & (flow_data[:,1]==9))
print(flow_count_55)
flow_count_Sept = np.sum((flow_data[:,3] > -1) & (flow_data[:,1]==9))
print(flow_count_Sept)
print(flow_count_55/flow_count_Sept*100)

# %% Question 4 - Daily flow greater than 55 cfs in September of 2000 or earlier

flow_count_55a = np.sum((flow_data[:,3] > 55) & (flow_data[:,1]==9) & (flow_data[:,0] <= 2000))
print(flow_count_55a)
flow_count_Septa = np.sum((flow_data[:,3] > -1) & (flow_data[:,1]==9) & (flow_data[:,0] <= 2000))
print(flow_count_Septa)
print(flow_count_55a/flow_count_Septa*100)

# %% Question 4 - Daily flow greater than 55 cfs in September of 2010 or later

flow_count_55b = np.sum((flow_data[:,3] > 55) & (flow_data[:,1]==9) & (flow_data[:,0] >= 2010))
print(flow_count_55b)
flow_count_Septb = np.sum((flow_data[:,3] > -1) & (flow_data[:,1]==9) & (flow_data[:,0] >= 2010))
print(flow_count_Septb)
print(flow_count_55b/flow_count_Septb*100)

# %% Question 5 - Change in daily flow from 1st to 2nd half of September

# Change in mean
Flow_mean1 = np.mean(flow_data[(flow_data[:,0] != 2020) & (flow_data[:,1]==9) & (flow_data[:,2] <= 15),3])
print("Mean 1st half: ",Flow_mean1)

Flow_mean1 = np.mean(flow_data[(flow_data[:,0] != 2020) & (flow_data[:,1]==9) & (flow_data[:,2] >= 16),3])
print("Mean 2nd half: ",Flow_mean1)

# Change in median
Flow_med1 = np.median(flow_data[(flow_data[:,0] != 2020) & (flow_data[:,1]==9) & (flow_data[:,2] <= 15),3])
print("Median 1st half: ",Flow_med1)

Flow_med2 = np.median(flow_data[(flow_data[:,0] != 2020) & (flow_data[:,1]==9) & (flow_data[:,2] >= 16),3])
print("Median 2nd half: ",Flow_med2)

# Change in median
Flow_std1 = np.std(flow_data[(flow_data[:,0] != 2020) & (flow_data[:,1]==9) & (flow_data[:,2] <= 15),3])
print("Std Dev 1st half: ",Flow_std1)

Flow_std2 = np.std(flow_data[(flow_data[:,0] != 2020) & (flow_data[:,1]==9) & (flow_data[:,2] >= 16),3])
print("Std Dev 2nd half: ",Flow_std2)

# %%
