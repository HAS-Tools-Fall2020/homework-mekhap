# Step 1: Import modules used in this script
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import json
import urllib.request as req
import urllib
import dataretrieval.nwis as nwis

# Step 2: Set up any functions that will be used in this script
def model_2wk_predict(precip1, precip2, temp1, temp2):

    """Function that makes 1 and 2 week flow predictions based on a regression
    model. The model should be built on 1 week time lagged flows, precip, and
    temperature, all weekly average variables. The model should be named
    'model'. The two predictions are saved to an array and printed.

    Inputs = (int or float) avg weekly value for model variables, normalized:
           precip1 = expected average precip for next week in inches
           precip2 = expected average precip for two weeks from now in inches
           temp1 = expected average temp for next week in fahrenheit
           temp1 = expected average temp for two weeks from now in fahrenheit

    Output = (array) array containing two values which represent 1 and 2 week
    forecast based on the regression model
           model_predictions[0] = 1 week prediciton of average natural log flow
           model_predictions[1] = 2 week prediciton of average natural log flow
    """
    flow = data['flow_tm1_nm'].iloc[-1]
    precip1_nm = (precip1 - data['precip'].mean()) / data['precip'].std()
    precip2_nm = (precip1 - data['precip'].mean()) / data['precip'].std()
    temp1_nm = (temp1 - data['airtemp'].mean()) / data['airtemp'].std()
    temp2_nm = (temp1 - data['airtemp'].mean()) / data['airtemp'].std()

    model_predictions = np.zeros(2)
    for i in range(0, 2):
        log_flow = model.intercept_ \
                                   + model.coef_[0] * flow \
                                   + model.coef_[1] * precip1_nm\
                                   + model.coef_[2] * temp1_nm
        model_predictions[i] = np.exp(log_flow)
        print('AR model ', i+1, ' week forecast is ',
              model_predictions[i].round(2), ' cfs')
        flow = (log_flow - data['flow_log'].mean()) / data['flow_log'].std()
        precip1_nm = precip2_nm
        temp1_nm = temp2_nm

    return model_predictions

# Step 3: Read in USGS streamflow data and create dataframe of avg weekly flow
# Use nwis.get_record function instead of saving a local file

# Change stop_date each week
station_id = "09506000"
USGS_start = "2016-12-25"
USGS_stop = "2020-12-05"

data_flow = nwis.get_record(sites=station_id, service='dv',
                            start=USGS_start, end=USGS_stop,
                            parameterCd='00060')

# Rename columns
data_flow.columns = ['flow', 'code', 'site_no']

# Make index a recognized datetime format instead of string
data_flow.index = data_flow.index.strftime('%Y-%m-%d')

data_flow['datetime'] = pd.to_datetime(data_flow.index)

# Aggregate flow values to weekly
flow_weekly = data_flow.resample("W-SAT", on='datetime').mean()

# Step 4: Read in Mesowest precip data

# Change demotoken to your token when running
mytoken = 'ee2e11fb217d4d42b54782f4f101a397'

# This is the base url that will be the start final url
base_url = "http://api.mesowest.net/v2/stations/timeseries"

# Specific arguments for the data that we want
# Change end date each week
args = {
    'start': '201612250000',
    'end': '202012050000',
    'obtimezone': 'UTC',
    'vars': 'precip_accum_since_local_midnight',
    'stids': 'C4534',
    'units': 'precip|in',
    'token': mytoken}
apiString = urllib.parse.urlencode(args)

fullUrl = base_url + '?' + apiString

response = req.urlopen(fullUrl)
responseDict = json.loads(response.read())

# Pull out date and temperature data
dateTime = responseDict['STATION'][0]['OBSERVATIONS']['date_time']
precip = responseDict['STATION'][0]['OBSERVATIONS']['precip_accum_since_local_midnight_set_1']

# Create dataframe
data_precip = pd.DataFrame({'Precip': precip}, index=pd.to_datetime(dateTime))

# Aggregate to weekly
precip_weekly = data_precip.resample('W-SAT').mean()
precip_weekly['Precip'] = precip_weekly['Precip'].replace(np.nan, 0)

# Make index a recognized datetime format instead of string
precip_weekly.index = precip_weekly.index.strftime('%Y-%m-%d')

# Step 5: Read in Mesowest temperature data

# Change demotoken to your token when running
mytoken = 'ee2e11fb217d4d42b54782f4f101a397'

# This is the base url that will be the start final url
base_url = "http://api.mesowest.net/v2/stations/timeseries"

# Specific arguments for the data that we want
# Change end date each week
args = {
    'start': '201612250000',
    'end': '202012050000',
    'obtimezone': 'UTC',
    'vars': 'air_temp',
    'stids': 'QVDA3',
    'units': 'temp|F',
    'token': mytoken}
apiString = urllib.parse.urlencode(args)

fullUrl = base_url + '?' + apiString

response = req.urlopen(fullUrl)
responseDict = json.loads(response.read())

# Pull out date and temperature data
dateTime = responseDict['STATION'][0]['OBSERVATIONS']['date_time']
airT = responseDict['STATION'][0]['OBSERVATIONS']['air_temp_set_1']

# Create dataframe
data_temp = pd.DataFrame({'AirTemp': airT}, index=pd.to_datetime(dateTime))

# Aggregate to weekly
temp_weekly = data_temp.resample('W-SAT').mean()

# Make index a recognized datetime format
temp_weekly.index = temp_weekly.index.strftime('%Y-%m-%d')

# Step 6: Combine datasets into one dataframe
data = flow_weekly.copy()
data['precip'] = precip_weekly['Precip']
data['airtemp'] = temp_weekly['AirTemp']

# Step 7: Setup the arrays used to build regrssion model
# This model uses a single 1 week time lag of flow, precip, and temp

# We will predict natural log of flow
data['flow_log'] = np.log(data['flow'])

# Create column of normalized log flow for plotting
data['flow_log_nm'] = (data['flow_log'] - data['flow_log'].mean()) / data['flow_log'].std()

# Shift log flow to create column of 1 week lagged log flow
data['flow_tm1'] = data['flow_log'].shift(1)

# Remove first row since it is missing lagged flow
data = data.iloc[1:]

# 1st model input variable: normalized lagged flow
data['flow_tm1_nm'] = (data['flow_tm1'] - data['flow_tm1'].mean()) / data['flow_tm1'].std()

# 2nd model input variable: normalized precip
data['precip_nm'] = (data['precip'] - data['precip'].mean()) / data['precip'].std()

# 3rd model input variable: normalized temp
data['airtemp_nm'] = (data['airtemp'] - data['airtemp'].mean()) / data['airtemp'].std()

# Step 8: Pick what portion of the time series to use as training data
# For this AR model, training = 2017-2018, testing = 2019-2020
train = data['2017-01-07':'2018-12-29'][['flow_log', 'flow_tm1_nm', 'precip_nm', 'airtemp_nm']]
test = data['2019-01-05':][['flow_log', 'flow_tm1_nm', 'precip_nm', 'airtemp_nm']]

# Step 9: Fit linear regression model
model = LinearRegression()
x = train[['flow_tm1_nm', 'precip_nm', 'airtemp_nm']]
y = train['flow_log'].values
model.fit(x, y)
r_sq = np.round(model.score(x, y), 2)

print('coefficient of determination:', np.round(r_sq, 2))
print('intercept:', np.round(model.intercept_, 2))
print('slope:', np.round(model.coef_, 2))

# Step 10: Set up prediction functions to view model performance
q_pred_train = model.predict(train[['flow_tm1_nm', 'precip_nm', 'airtemp_nm']])
q_pred_test = model.predict(test[['flow_tm1_nm', 'precip_nm', 'airtemp_nm']])

# Step 11: Forecast predictions
# Manually input expected precipitation and temperture for the next two weeks
precip_1wk = 0
precip_2wk = 0
temp_1wk = 45
temp_2wk = 41

# Call function to make prediction
model_predictions = model_2wk_predict(precip_1wk, precip_2wk, temp_1wk, temp_2wk)
print(model_predictions)

# Step 12: Make predictions for 16 week forecast
# Predictions will be based on weekly flow in 2019, which was a low flow year
# For this year, I will assume max weekly flow of 200 cfs

flow_2019 = data["2019-08-31":"2019-12-14"]

lt_forecast = np.zeros(16)
for i in range(0, 16):
    if flow_2019['flow'].iloc[i] <= 200:
        lt_forecast[i] = flow_2019['flow'].iloc[i].round(0)
        print('lt_week', i+1, ' = ', flow_2019['flow'].iloc[i].round(0))
    else:
        lt_forecast[i] = 200
        print('lt_week', i+1, ' = 200')

print(lt_forecast)
