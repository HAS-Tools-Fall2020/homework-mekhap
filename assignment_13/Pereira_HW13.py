# Modified starter code from Laura

# %%
# Step 1: Import modules used in this script
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from sklearn.linear_model import LinearRegression
import datetime
import json
import urllib.request as req
import urllib
import dataretrieval.nwis as nwis
import geopandas as gpd
import fiona
from shapely.geometry import Point
import contextily as ctx

# %%
# Step 2: Set up any functions that will be used in this script

def model_2wk_predict(precip1, precip2, temp1, temp2):

    """Function that makes 1 and 2 week flow predictions based on a regression
    model. The model should be built on 1 week time lagged flows, precip, and
    temperature, all weekly average variables. The model should be named
    'model'. The two predictions are saved to an array and printed.

    Inputs = (ints or floats) average weekly value for model variables, all normalized:
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

# %%
# Step 3: Make a map to orient ourselves

# Dataset 1: USGS stream gauges
# Download Gauges II USGS stream gauge dataset here:
# https://water.usgs.gov/GIS/metadata/usgswrd/XML/gagesII_Sept2011.xml#stdorder
# Read in using geopandas
file = os.path.join('../data/GIS_files', 'gagesII_9322_sept30_2011.shp')
gages = gpd.read_file(file)

# Filter to only AZ gauges
gages.columns
gages.STATE.unique()
gages_AZ = gages[gages['STATE'] == 'AZ']

# Dataset 2: Watershed boundaries for the Lower Colorado
# Download WBD_15_HU2_GDB.gdb from USGS here:
# https://www.usgs.gov/core-science-systems/ngp/national-hydrography/access-national-hydrography-products
# https://viewer.nationalmap.gov/basic/?basemap=b1&category=nhd&title=NHD%20View
# Read in using geopandas
file = os.path.join('../data/GIS_files', 'WBD_15_HU2_GDB.gdb')
fiona.listlayers(file)
HUC6 = gpd.read_file(file, layer="WBDHU6")

# Filter to only Verde River Watershed
HUC6.columns
HUC6.name.unique()
HUC6_Verde = HUC6[HUC6['name'] == 'Verde']

# Dataset 3: Major rivers/streams
# Download USA Rivers and Streams from Esri here:
# https://hub.arcgis.com/datasets/esri::usa-rivers-and-streams?geometry=-115.952%2C31.858%2C-109.014%2C33.476
# Read in using geopandas
file = os.path.join('../data/GIS_files', 'USA_Rivers_and_Streams.shp')
rivers_USA = gpd.read_file(file)

# Filter to only AZ
rivers_USA.columns
rivers_USA.State.unique()
rivers_AZ = rivers_USA[rivers_USA['State'] == 'AZ']

# Filter to only Verde
rivers_AZ.columns
rivers_AZ.Name.unique()
river_Verde = rivers_AZ[rivers_AZ['Name'] == 'Verde River']

# Dataset 4: Add point location of our stream gage
# https://waterdata.usgs.gov/nwis/inventory/?site_no=09506000&agency_cd=USGS
# Stream gauge:  34.44833333, -111.7891667
point_list = np.array([[-111.7891667, 34.44833333]])

# Make point into spatial feature
point_geom = [Point(xy) for xy in point_list]
point_geom

# Make a dataframe of the point
point_df = gpd.GeoDataFrame(point_geom, columns=['geometry'],
                            crs=HUC6.crs)

# Re-project datasets to match gages_AZ
points_project = point_df.to_crs(gages_AZ.crs)
HUC6_project = HUC6.to_crs(gages_AZ.crs)
HUC6_Verde_project = HUC6_Verde.to_crs(gages_AZ.crs)
rivers_AZ_project = rivers_AZ.to_crs(gages_AZ.crs)
river_Verde_project = river_Verde.to_crs(gages_AZ.crs)

# Plot projected datasets together
fig, ax = plt.subplots(figsize=(5, 7))

# Set map extent to zoom in on Verde River watershed
xlim = ([-1600000, -1300000])
ylim = ([1250000, 1600000])
ax.set_xlim(xlim)
ax.set_ylim(ylim)

# Draw layers in specified order using zorder
HUC6_project.boundary.plot(ax=ax, color=None, edgecolor='black', zorder=1,
                           label='Watersheds (HUC2)', linewidth=0.75)
HUC6_Verde_project.boundary.plot(ax=ax, color=None, edgecolor='black',
                                 linewidth=2, zorder=2)
rivers_AZ_project.plot(ax=ax, linewidth=0.5, color='b',
                       label='Rivers/Streams', zorder=3)
river_Verde_project.plot(ax=ax, linewidth=2, color='b', zorder=4)
gages_AZ.plot(ax=ax, markersize=40, marker='^', color='limegreen',
              edgecolor='black', label='USGS stream gage', zorder=5)
points_project.plot(ax=ax, color='yellow', marker='^', edgecolor='black',
                    markersize=70, label='Verde River forecast gage', zorder=6)

# Set map title and axes names
ax.set_title('Verde River Watershed')
ax.set_xlabel('Easting (m)')
ax.set_ylabel('Northing (m)')
ax.ticklabel_format(style="sci", scilimits=(0,0))
ax.legend(loc='upper right', fontsize=7)

# Add Topo basemap and reproject basemap to match gages_AZ
ctx.add_basemap(ax, crs=gages_AZ.crs, url=ctx.providers.OpenTopoMap)
plt.show()

# Save Figure
fig.savefig("VerdeWatershed_Map", bbox_inches='tight')

# %%
# Step 4: Read in USGS streamflow data and create dataframe of avg weekly flow
# Use nwis.get_record function instead of saving a local file

# Change stop_date each week
station_id = "09506000"
USGS_start = "2016-12-25"
USGS_stop = "2020-11-21"

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

# %%
# Step 5: Read in Mesowest precip data

# Change demotoken to your token when running
mytoken = 'ee2e11fb217d4d42b54782f4f101a397'

# This is the base url that will be the start final url
base_url = "http://api.mesowest.net/v2/stations/timeseries"

# Specific arguments for the data that we want
# Change end date each week
args = {
    'start': '201612250000',
    'end': '202011210000',
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

# %%
# Step 6: Read in Mesowest temperature data

# Change demotoken to your token when running
mytoken = 'ee2e11fb217d4d42b54782f4f101a397'

# This is the base url that will be the start final url
base_url = "http://api.mesowest.net/v2/stations/timeseries"

# Specific arguments for the data that we want
# Change end date each week
args = {
    'start': '201612250000',
    'end': '202011210000',
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

# %%
# Step 7: Combine datasets into one dataframe
data = flow_weekly.copy()
data['precip'] = precip_weekly['Precip']
data['airtemp'] = temp_weekly['AirTemp']

# %%
# Step 8: Setup the arrays used to build regrssion model
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

# %%
# Step 9: Pick what portion of the time series to use as training data
# For this AR model, training = 2017-2018, testing = 2019-2020

train = data['2017-01-07':'2018-12-29'][['flow_log', 'flow_tm1_nm', 'precip_nm', 'airtemp_nm']]
test = data['2019-01-05':][['flow_log', 'flow_tm1_nm', 'precip_nm', 'airtemp_nm']]

# %%
# Step 10: Fit linear regression model
model = LinearRegression()
x = train[['flow_tm1_nm', 'precip_nm', 'airtemp_nm']]
y = train['flow_log'].values
model.fit(x, y)
r_sq = np.round(model.score(x, y), 2)

print('coefficient of determination:', np.round(r_sq, 2))
print('intercept:', np.round(model.intercept_, 2))
print('slope:', np.round(model.coef_, 2))

# %%
# Step 11: Set up prediction functions to view model performance
q_pred_train = model.predict(train[['flow_tm1_nm', 'precip_nm', 'airtemp_nm']])
q_pred_test = model.predict(test[['flow_tm1_nm', 'precip_nm', 'airtemp_nm']])

# %%
# Step 12: Generate plots to visualize regression model and datasets
# This step is optional, not neccessary to generate the forecasts.

# Set plot style and sublot layout
plt.style.use('classic')
fig, ax = plt.subplots(1, 3, figsize=(12, 4))
ax = ax.flatten()
fig.tight_layout()
plt.subplots_adjust(hspace=0.5, wspace=0.2)

# PLOT 1: Model Period
ax[0].plot(train['flow_log'], 'orange', label='training period', linewidth=6)
ax[0].plot(test['flow_log'], 'greenyellow', label='testing period', linewidth=6)
ax[0].plot(data['flow_log'], 'b', label='observed flow', linewidth=1)
ax[0].set(title="Model Period (2017-2020)",
          xlabel="Date", ylabel="Weekly Avg Natual Log Flow [cfs]",
          xlim=['2017-01-07', '2020-11-21'])
ax[0].legend(fontsize=8)
plt.setp(ax[0].get_xticklabels(), rotation=45)

# PLOT 2: Normalized Predictive Variables
ax[1].plot(data['flow_log_nm'], 'navy', label='observed flow')
ax[1].plot(data['flow_tm1_nm'], 'cornflowerblue', label='lagged flow')
ax[1].plot(data['precip_nm'], 'forestgreen', label='precip')
ax[1].plot(data['airtemp_nm'], 'orange', label='temperature')
ax[1].set(title="Normalized Predictive Variables", xlabel="Date",
          xlim=['2017-01-07', '2018-12-29'])
ax[1].legend(fontsize=8)
plt.setp(ax[1].get_xticklabels(), rotation=45)

# PLOT 3: Model Performance
ax[2].scatter(np.sort(test['flow_log']), np.sort(q_pred_test), 
              color='m', edgecolor='purple', label='Model Predictions')
ax[2].plot([0,9], [0,9], 
              color='blue', alpha=0.5)
ax[2].set(title="Model Performance - Testing Period", xlabel="Observed Natural Log Flow",
          ylabel="Simulated Natural Log Flow", xlim = [3,9], ylim = [3,9])
ax[2].legend(fontsize=8)
plt.setp(ax[2].get_xticklabels(), rotation=45)

plt.show()

# Save Figure
fig.savefig("Regression_Model_Visualization", bbox_inches='tight')

# %%
# Step 13: Forecast predictions
# Manually input expected precipitation and temperture for the next two weeks
precip_1wk = 0
precip_2wk = 0
temp_1wk = 50
temp_2wk = 50

# Call function to make prediction
model_predictions = model_2wk_predict(precip_1wk, precip_2wk, temp_1wk, temp_2wk)

# %%
# Step 14: Make predictions for 16 week forecast
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
        print('lt_week', i+1, ' = 200 cfs')
# %%
