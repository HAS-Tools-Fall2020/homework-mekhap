# Modified code from Laura

# %%
import pandas as pd
import matplotlib.pyplot as plt
import urllib.request as req
import xarray as xr
import rioxarray
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import seaborn as sns
import geopandas as gpd
import fiona
import shapely
from netCDF4 import Dataset

# %%
# Net CDF file historical time series
data_path = os.path.join('../data',
                         'X72.222.162.26.325.17.2.0.nc')

# Read in the dataset as an x-array
dataset = xr.open_dataset(data_path)
# look at it
dataset


# We can inspect the metadata of the file like this:
metadata = dataset.attrs
metadata
# And we can grab out any part of it like this:
metadata['dataset_title']
metadata['history']

# we can also look at other  attributes like this
dataset.values
dataset.dims
dataset.coords

# Focusing on just the precip values
temp = dataset['air']
temp

# Now to grab out data first lets look at spatail coordinates:
dataset['air']['lat'].values
# The first 4 lat values
dataset['air']['lat'].values
dataset['air']['lon'].values

# Now looking at the time;
dataset["air"]["time"].values
dataset["air"]["time"].values.shape


# Now lets take a slice: Grabbing data for just one point
lat = dataset["air"]["lat"].values[0]
lon = dataset["air"]["lon"].values[0]
print("Long, Lat values:", lon, lat)
one_point = dataset["air"].sel(lat=lat,lon=lon)
one_point.shape

# use x-array to plot timeseries
one_point.plot.line()
precip_val = one_point.values

# Make a nicer timeseries plot
f, ax = plt.subplots(figsize=(12, 6))
one_point.plot.line(hue='lat',
                    marker="o",
                    ax=ax,
                    color="grey",
                    markerfacecolor="purple",
                    markeredgecolor="purple")
ax.set(title="Time Series For a Single Lat / Lon Location")

# %%
# convert to weekly avg temp 
# daily_temp = one_point.to_dataframe()
temp_weekly = daily_temp.resample("W-SAT").mean()

#Plot weekly temp data
fig, ax = plt.subplots()
ax.plot(temp_weekly['air'], 'orange', label='Weekly Avg Temp', linewidth = 1)
ax.set(title="Weekly Average Temperature (35', 247.5') - NCEP Reanalysis Data", 
       xlabel="Date", ylabel="Mean Weekly Temp (degK)")
ax.legend()
plt.show()

fig.set_size_inches(7,5)
fig.savefig("NCEPReanalysis_Temp.png")


# %%
