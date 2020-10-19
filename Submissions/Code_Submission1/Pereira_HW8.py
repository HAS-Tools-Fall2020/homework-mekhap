# Modified starter code from Laura

# %%
# Step 1: Import modules used in this script
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import datetime

# %%
# Step 2: Set up any functions that will be used in this script
def armodel_2wk_predict(flow1, flow2, flow3):
    """Function that makes 1 and 2 week flow predictions based on an AR model.
    The AR model should be built on three time lags and be named 'model'. The
    two predictions are saved to an array and printed.

    Inputs = (ints or floats) average flow for three consecutive weeks:
           flow1 = average flow from week prior to desired week for prediction
           flow2 = average flow from week prior to flow1
           flow3 = average flow from week prior to flow2

    Output = (array) array containing two values which represent 1 and 2 week
    forecast based on AR model
           ar_model_predictions[0] = 1 week prediciton of avgerage flow
           ar_model_predictions[1] = 2 week prediciton of avgerage flow
    """

    ar_model_predictions = np.zeros(2)
    for i in range(0, 2):
        ar_model_predictions[i] = model.intercept_ \
                                   + model.coef_[0] * flow1 \
                                   + model.coef_[1] * flow2 \
                                   + model.coef_[2] * flow3
        print('AR model ', i+1, ' week forecast is ',
              ar_model_predictions[i].round(2), ' cfs'
              )
        flow1 = ar_model_predictions[i]
        flow2 = flow1
        flow3 = flow2
    return ar_model_predictions

# %%
# Step 3: Set the file name and path for streamflow data
filename = 'streamflow_week8.txt'
filepath = os.path.join('../../data', filename)
print(os.getcwd())
print(filepath)

# %%
# Step 4: Create dataframe of average weekly flows

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
flow_weekly = data.resample("W-SAT", on='datetime').mean()

# %%
# Step 5: Setup the arrays used to build autoregressive (AR) model
# This AR model uses three 1 week time lags

flow_weekly['flow_tm1'] = flow_weekly['flow'].shift(1)
flow_weekly['flow_tm2'] = flow_weekly['flow'].shift(2)
flow_weekly['flow_tm3'] = flow_weekly['flow'].shift(3)

# %%
# Step 6 - Pick what portion of the time series to use as training data
# For this AR model, training = 2017-2018, testing = 2019-2020
train = flow_weekly[1461:1566][['flow', 'flow_tm1', 'flow_tm2', 'flow_tm3']]
test = flow_weekly[1566:][['flow', 'flow_tm1', 'flow_tm2', 'flow_tm3']]

# %%
# Step 7: Fit linear regression model using 3 time lags as inputs to the model
model = LinearRegression()
x3 = train[['flow_tm1', 'flow_tm2', 'flow_tm3']]
y = train['flow'].values
model.fit(x3, y)
r_sq = np.round(model.score(x3, y), 2)

print('coefficient of determination:', np.round(r_sq, 2))
print('intercept:', np.round(model.intercept_, 2))
print('slope:', np.round(model.coef_, 2))

# %%
# Step 8: Generate plots to visualize AR model
# This step is optional, not neccessary to generate the forecasts.

# Generate predition functions for plotting
q_pred3_train = model.predict(train[['flow_tm1', 'flow_tm2', 'flow_tm3']])
q_pred3_test = model.predict(test[['flow_tm1', 'flow_tm2', 'flow_tm3']])

# Set plot style and sublot layout
plt.style.use('classic')
fig, ax = plt.subplots(2, 2, figsize=(10, 8))
ax = ax.flatten()
fig.tight_layout()
plt.subplots_adjust(hspace=0.5, wspace=0.2)

# PLOT 1: Timeseries of observed flow, highlight training and testing periods
ax[0].plot(train['flow'], 'orange', label='training period', linewidth=6)
ax[0].plot(test['flow'], 'greenyellow', label='testing period', linewidth=6)
ax[0].plot(flow_weekly['flow'], 'b', label='observed flow', linewidth=1)
ax[0].set(title="Observed Flow for Model Build (2017-2020)",
          xlabel="Date", ylabel="Weekly Avg Flow [cfs]", yscale='log',
          xlim=['2017-01-01', '2020-11-01'])
ax[0].legend(fontsize=8)
plt.setp(ax[0].get_xticklabels(), rotation=45)

# PLOT 2: Lagged Flows (Predictive Variables)
ax[1].plot(flow_weekly['flow'], 'navy', label='observed flow')
ax[1].plot(flow_weekly['flow_tm1'], 'forestgreen', label='1 week time lag')
ax[1].plot(flow_weekly['flow_tm2'], 'gold', label='2 week time lag')
ax[1].plot(flow_weekly['flow_tm3'], 'tomato', label='3 week time lag')
ax[1].set(title="Time Lagged Flows for Training Period", xlabel="Date",
          ylabel="Weekly Avg Flow [cfs]", yscale='log',
          xlim=['2017-01-01', '2019-01-01'])
ax[1].legend(fontsize=8)
plt.setp(ax[1].get_xticklabels(), rotation=45)

# PLOT 3: Observed vs Simulated Flows
ax[2].plot(train['flow'], color='cornflowerblue', linewidth=2,
           label='observed flow')
ax[2].plot(train.index, q_pred3_train, color='m', linestyle='--',
           label='simulated flow')
ax[2].set(title="Observed vs Simulated Flow", xlabel="Date",
          ylabel="Weekly Avg Flow [cfs]", yscale='log',
          xlim=['2017-01-01', '2019-01-01'])
ax[2].legend(fontsize=8)
plt.setp(ax[2].get_xticklabels(), rotation=45)

# PLOT 4: Scatter plot of t vs t-1 flow with log log axes
ax[3].scatter(train['flow_tm1'], train['flow'], marker='^',
              color='cornflowerblue', label='Observed Flow (t-1 vs t)')
ax[3].plot(np.sort(train['flow_tm1']), np.sort(q_pred3_train), color='m',
           label='AR model')
ax[3].set(title="Flow t vs Flow t-1", xlabel='flow t-1', ylabel='flow t',
          yscale='log', xscale='log')
ax[3].legend(fontsize=8)
plt.setp(ax[3].get_xticklabels(), rotation=45)

plt.show()

# Save Figure
fig.savefig("AR_Model_Visualization", bbox_inches='tight')

# %%
# Step 9: Print the AR model's predictions for 1 week and 2 week forecast
# NOTE: Do not submit these values as forecast entries

ar_prediction = armodel_2wk_predict(flow_weekly['flow'].iloc[-1:].values[0],
                                    flow_weekly['flow'].iloc[-2:-1].values[0],
                                    flow_weekly['flow'].iloc[-3:-2].values[0]
                                    )

# %%
# Step 10: Outside of AR model, make predictions for forecast entries
# Based predictions on avg flow over past week and past two weeks
myprediction_1wk = flow_weekly['flow'].iloc[-1:].values[0].round(0)
myprediction_2wk = np.mean(flow_weekly['flow'].iloc[-2:]).round(0)

# Submit these values as forecast entries
print("My prediction for 1 week forecast: ", myprediction_1wk, 'cfs')
print("My prediction for 2 week forecast: ", myprediction_2wk, 'cfs')

# %%
# Step 11: Make predictions for 16 week forecast
# Predictions will be based on weekly flow in 2019, which was a low flow year
# For this year, I will assume max weekly flow of 200 cfs
flow_2019 = flow_weekly["2019-08-31":"2019-12-14"]

lt_forecast = np.zeros(16)
for i in range(0, 16):
    if flow_2019['flow'].iloc[i] <= 200:
        lt_forecast[i] = flow_2019['flow'].iloc[i].round(0)
        print('lt_week', i+1, ' = ', flow_2019['flow'].iloc[i].round(0))
    else:
        lt_forecast[i] = 200
        print('lt_week', i+1, ' = 200 cfs')
# %%
