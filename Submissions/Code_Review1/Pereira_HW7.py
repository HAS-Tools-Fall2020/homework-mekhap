# Modified starter code from Laura

# %%
# Import modules used in this script
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import datetime
# note you may need to do pip install for sklearn

# %%
# Set the file name and path for streamflow data
filename = 'streamflow_week7.txt'
filepath = os.path.join('../../data', filename)
print(os.getcwd())
print(filepath)

# %%
# Read the data into a pandas dataframe
data = pd.read_table(filepath, sep='\t', skiprows=30,
                     names=['agency_cd', 'site_no', 'datetime', 'flow',
                            'code'], parse_dates=['datetime']
                     )

# Expand the dates to year month day
data['year'] = pd.DatetimeIndex(data['datetime']).year
data['month'] = pd.DatetimeIndex(data['datetime']).month
data['day'] = pd.DatetimeIndex(data['datetime']).dayofweek
data['dayofweek'] = pd.DatetimeIndex(data['datetime']).dayofweek

# Aggregate flow values to weekly
flow_weekly = data.resample("W", on='datetime').mean()

# %%
# Build autoregressive (AR) model, this AR model uses three 1 week time lags
# Step 1: setup the arrays used to build AR model
flow_weekly['flow_tm1'] = flow_weekly['flow'].shift(1)
flow_weekly['flow_tm2'] = flow_weekly['flow'].shift(2)
flow_weekly['flow_tm3'] = flow_weekly['flow'].shift(3)

# %%
# Step 2 - pick what portion of the time series to use as training data
# For this AR model, training = 2017-2018, testing = 2019-2020
# Note1 - drop first 2 weeks since they won't have lagged data to go with them
train = flow_weekly[1461:1566][['flow', 'flow_tm1', 'flow_tm2', 'flow_tm3']]
test = flow_weekly[1566:][['flow', 'flow_tm1', 'flow_tm2', 'flow_tm3']]

# %%
# Step 3: Fit linear regression model using 3 time lags as inputs to the model
model3 = LinearRegression()
x3 = train[['flow_tm1', 'flow_tm2', 'flow_tm3']]
y = train['flow'].values
model3.fit(x3, y)
r_sq = model3.score(x3, y)

print('coefficient of determination:', np.round(r_sq, 2))
print('intercept:', np.round(model3.intercept_, 2))
print('slope:', np.round(model3.coef_, 2))

# %%
# Step 4: Setup input variables: avg flow from 1, 2, and 3 weeks ago
flow_1wkprior = data['flow'].iloc[-7:].mean()
flow_2wkprior = data['flow'].iloc[-14:-7].mean()
flow_3wkprior = data['flow'].iloc[-21:-14].mean()

# %%
# Step 6: Define prediction function for this script (my first function ever)
# I previously had 2 similar block of code to generate 1 and 2 week prediction


def model3_2wk_predict(flow1, flow2, flow3):
    """Function that prints 1 and 2 week flow predictions based on AR model

    Inputs = (ints or floats) average flow from prior three weeks
           flow1 = average weekly flow from prior week
           flow2 = average weekly flow from 2 weeks prior
           flow3 = average weekly flow from 3 weeks prior

    Output = (array) array containing two values which represent 1 and 2 week
    forecast based on AR model
           ar_model_predictions[0] = 1 week prediciton of avgerage flow
           ar_model_predictions[1] = 2 week prediciton of avgerage flow
    """

    ar_model_predictions = np.zeros(2)
    for i in range(0, 2):
        ar_model_predictions[i] = model3.intercept_ \
                                   + model3.coef_[0] * flow1 \
                                   + model3.coef_[1] * flow2 \
                                   + model3.coef_[2] * flow3
        print('AR model ', i+1, ' week forecast is ',
              ar_model_predictions[i].round(2), ' cfs'
              )
        flow1 = ar_model_predictions[i]
        flow2 = flow1
        flow3 = flow2
    return ar_model_predictions

# %%
# Step 6: Print the AR model's predictions for 1 week and 2 week forecast
# Enter printed values into README.md file
# NOTE: Do not submit these values as forecast entries


ar_prediction = model3_2wk_predict(flow_1wkprior, flow_2wkprior, flow_3wkprior)

# %%
# Now outside of AR model, make predictions for forecast entries
# Based on avg flow over past week and past two weeks
flow_2wk_avg = data['flow'].iloc[-14:].mean()

# Enter these values in the README.md file and submit as forecast entries
print("Mekha's prediction 1 week forecast: ", flow_1wkprior.round(2), 'cfs')
print("Mekha's prediction 2 week forecast: ", flow_2wk_avg.round(2), 'cfs')

# %%
# The remaining code is optional to run
# It creates plots to visualize the AR model

# %%
# # Generate predition functions for plotting
q_pred3_train = model3.predict(train[['flow_tm1', 'flow_tm2', 'flow_tm3']])
q_pred3_test = model3.predict(test[['flow_tm1', 'flow_tm2', 'flow_tm3']])

# Set plot style
plt.style.use('classic')

# %% PLOT 1: Timeseries of observed flow values,
# and highlight of training and testing period
fig, ax = plt.subplots()
ax.plot(train['flow'], 'orange', label='training period', linewidth=6)
ax.plot(test['flow'], 'greenyellow', label='testing period', linewidth=6)
ax.plot(flow_weekly['flow'], 'b', label='observed flow', linewidth=1)
ax.set(title="Observed Flow for Model Period (1/1/2017-10/3/2020)",
       xlabel="Date", ylabel="Weekly Avg Flow [cfs]", yscale='log',
       xlim=[datetime.date(2017, 1, 1), datetime.date(2020, 10, 3)])
ax.legend()
plt.show()

# Save Figure
fig.set_size_inches(7, 5)
fig.savefig("ObservedFlow_Train_Test.png")

# %% PLOT 2: Lagged Flows (Predictive Variables)
fig, ax = plt.subplots()
ax.plot(flow_weekly['flow'], 'navy', label='observed flow')
ax.plot(flow_weekly['flow_tm1'], 'forestgreen', label='1 week time lag')
ax.plot(flow_weekly['flow_tm2'], 'gold', label='2 week time lag')
ax.plot(flow_weekly['flow_tm3'], 'tomato', label='3 week time lag')
ax.set(title="Time Lagged Flows for Training Period", xlabel="Date",
       ylabel="Weekly Avg Flow [cfs]", yscale='log',
       xlim=[datetime.date(2017, 1, 1), datetime.date(2018, 12, 31)])
ax.legend()
plt.show()

# Save Figure
fig.set_size_inches(7, 5)
fig.savefig("TimeLaggedFlows.png")

# %% PLOT 3: Observed vs Simulated Flows
fig, ax = plt.subplots()
ax.plot(train['flow'], color='cornflowerblue', linewidth=2,
        label='observed flow')
ax.plot(train.index, q_pred3_train, color='m', linestyle='--',
        label='simulated flow')
ax.set(title="Observed vs Simulated Flow", xlabel="Date",
       ylabel="Weekly Avg Flow [cfs]", yscale='log')
ax.legend()
plt.show()

# Save Figure
fig.set_size_inches(7, 5)
fig.savefig("ObservedVsSimulated.png")

# %% PLOT 4: Scatter plot of t vs t-1 flow with log log axes
fig, ax = plt.subplots()
ax.scatter(train['flow_tm1'], train['flow'], marker='^',
           color='cornflowerblue', label='Observed Flow (t-1 vs t)')
ax.set(title="Flow t vs Flow t-1", xlabel='flow t-1', ylabel='flow t',
       yscale='log', xscale='log')
ax.plot(np.sort(train['flow_tm1']), np.sort(q_pred3_train), color='m',
        label='AR model (r2 = 0.68)')
ax.legend()
plt.show()

# Save Figure
fig.set_size_inches(7, 5)
fig.savefig("Scatter_TvsT-1.png")
# %%
