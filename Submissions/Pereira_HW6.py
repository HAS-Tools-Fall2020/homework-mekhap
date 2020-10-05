# Modified starter code from Laura

# %%
# Import the modules we will use
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import datetime
#note you may need to do pip install for sklearn

# %%
# ** MODIFY **
# Set the file name and path to where you have stored the data
filename = 'streamflow_week6.txt'
filepath = os.path.join('../data', filename)
print(os.getcwd())
print(filepath)

# %%
#Read the data into a pandas dataframe
data=pd.read_table(filepath, sep = '\t', skiprows=30,
        names=['agency_cd', 'site_no', 'datetime', 'flow', 'code'],
        parse_dates=['datetime']
        )

# Expand the dates to year month day
data['year'] = pd.DatetimeIndex(data['datetime']).year
data['month'] = pd.DatetimeIndex(data['datetime']).month
data['day'] = pd.DatetimeIndex(data['datetime']).dayofweek
data['dayofweek'] = pd.DatetimeIndex(data['datetime']).dayofweek

# Aggregate flow values to weekly 
flow_weekly = data.resample("W", on='datetime').mean()

# %%
# Step 1: setup the arrays you will build your model on

flow_weekly['flow_tm1'] = flow_weekly['flow'].shift(1)
flow_weekly['flow_tm2'] = flow_weekly['flow'].shift(2)
flow_weekly['flow_tm3'] = flow_weekly['flow'].shift(3)
flow_1wkprior = 57.3 # Avg flow 9/27-10/3 
flow_2wkprior = 58.4 # Avg flow 9/20-9/26 
flow_3wkprior = 56.2 # Avg flow 9/13-9/19 

# Step 2 - pick what portion of the time series to use as training data
# Note1 - dropping the first two weeks since they wont have lagged data to go with them  
train = flow_weekly[1461:1566][['flow', 'flow_tm1', 'flow_tm2','flow_tm3']]
test = flow_weekly[1566:][['flow', 'flow_tm1', 'flow_tm2','flow_tm3']]

# %% Step 3: Fit a linear regression model using sklearn with one time lag
model = LinearRegression()
x=train['flow_tm1'].values.reshape(-1,1) #See the tutorial to understand the reshape step here 
y=train['flow'].values
model.fit(x,y)

#Look at the results
# r^2 values
r_sq = model.score(x, y)
print('coefficient of determination:', np.round(r_sq,2))
print('intercept:', np.round(model.intercept_, 2))
print('slope:', np.round(model.coef_, 2))

# Model prediction based on last week's flow
prediction = model.intercept_ + model.coef_ * flow_1wkprior
print("Prediction for next week's flow: ", prediction)

# %% Step 3: Fit a linear regression model using two time lags as inputs to the model 
model2 = LinearRegression()
x2=train[['flow_tm1','flow_tm2']]
model2.fit(x2,y)
r_sq = model2.score(x2, y)
print('coefficient of determination:', np.round(r_sq,2))
print('intercept:', np.round(model2.intercept_, 2))
print('slope:', np.round(model2.coef_, 2))

# Model prediction based on last two weeks' flow
prediction = model2.intercept_ + model2.coef_[0] * flow_1wkprior + model2.coef_[1] * flow_2wkprior
print("Prediction for next week's flow: ", prediction)

# %% Step 3: Fit a linear regression model using three time lags as inputs to the model 
model3 = LinearRegression()
x3=train[['flow_tm1','flow_tm2','flow_tm3']]
model3.fit(x3,y)
r_sq = model3.score(x3, y)
print('coefficient of determination:', np.round(r_sq,2))
print('intercept:', np.round(model3.intercept_, 2))
print('slope:', np.round(model3.coef_, 2))

# Model prediction based on last three weeks' flow
prediction = model3.intercept_ + model3.coef_[0] * flow_1wkprior + model3.coef_[1] * flow_2wkprior + model3.coef_[2] * flow_3wkprior
print("Prediction for next week's flow: ", prediction)

# %% Based on the r squared value and 1 week predictions of the three models above, 
# I will go with model 3 which uses 3 time lags

# Step 4a Make a prediction with your model 
# Predict the model response for a  given flow value
# generate preditions with the funciton
q_pred3_train = model3.predict(train[['flow_tm1', 'flow_tm2', 'flow_tm3']])
q_pred3_test = model3.predict(test[['flow_tm1', 'flow_tm2', 'flow_tm3']])

#alternatievely you can calcualte this yourself like this:
#q_pred3 = model3.intercept_ + model3.coef_[0]* train['flow_tm1'] +  model3.coef_[1]* train['flow_tm2'] + model3_coef[2]* train['flow_tm3'] 

# %% Set plot style
plt.style.use('classic')

# %% PLOT 1: Timeseries of observed flow values, and highlight of training and testing period
fig, ax = plt.subplots()
ax.plot(train['flow'], 'orange', label='training period', linewidth = 6)
ax.plot(test['flow'], 'greenyellow', label='testing period', linewidth = 6)
ax.plot(flow_weekly['flow'], 'b', label='observed flow', linewidth = 1)
ax.set(title="Observed Flow for Model Period (1/1/2017-10/3/2020)", xlabel="Date", ylabel="Weekly Avg Flow [cfs]",
        yscale='log', xlim=[datetime.date(2017, 1, 1), datetime.date(2020, 10, 3)])
ax.legend()
plt.show()

# Save Figure
fig.set_size_inches(7,5)
fig.savefig("ObservedFlow_Train_Test.png")

# %% PLOT 2: Lagged Flows (Predictive Variables)
fig, ax = plt.subplots()
ax.plot(flow_weekly['flow'], 'navy', label='observed flow')
ax.plot(flow_weekly['flow_tm1'], 'forestgreen', label='1 week time lag')
ax.plot(flow_weekly['flow_tm2'], 'gold', label='2 week time lag')
ax.plot(flow_weekly['flow_tm3'], 'tomato', label='3 week time lag')
ax.set(title="Time Lagged Flows for Training Period", xlabel="Date", ylabel="Weekly Avg Flow [cfs]",
        yscale='log', xlim=[datetime.date(2017, 1, 1), datetime.date(2018, 12, 31)])
ax.legend()
plt.show()

# Save Figure
fig.set_size_inches(7,5)
fig.savefig("TimeLaggedFlows.png")

# %% PLOT 3: Observed vs Simulated Flows
fig, ax = plt.subplots()
ax.plot(train['flow'], color='cornflowerblue', linewidth=2, label='observed flow')
ax.plot(train.index, q_pred3_train, color='m', linestyle='--', 
        label='simulated flow')
ax.set(title="Observed vs Simulated Flow", xlabel="Date", ylabel="Weekly Avg Flow [cfs]",
        yscale='log')
ax.legend()
plt.show()

# Save Figure
fig.set_size_inches(7,5)
fig.savefig("ObservedVsSimulated.png")


# %% PLOT 4: Scatter plot of t vs t-1 flow with log log axes
fig, ax = plt.subplots()
ax.scatter(train['flow_tm1'], train['flow'], marker='^',
              color='cornflowerblue', label='Observed Flow (t-1 vs t)')
ax.set(title ="Flow t vs Flow t-1", xlabel='flow t-1', ylabel='flow t', yscale='log', xscale='log')
ax.plot(np.sort(train['flow_tm1']), np.sort(q_pred3_train), color='m', label='AR model (r2 = 0.68)')
ax.legend()
plt.show()

# Save Figure
fig.set_size_inches(7,5)
fig.savefig("Scatter_TvsT-1.png")
# %%
