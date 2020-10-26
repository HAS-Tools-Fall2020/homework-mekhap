# %%
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import datetime

# %%
filename = 'streamflow_week8.txt'
filepath = os.path.join('../data', filename)
data = pd.read_table(filepath, sep='\t', skiprows=30,
                     names=['agency_cd', 'site_no',
                            'datetime', 'flow', 'code'],
                     parse_dates=['datetime'], index_col='datetime'
                     )

# %%
data['flow'].iloc[2:5]
data.flow.iloc[2:5]
# %%
data['flow'].loc['1989-01-03':'1989-01-05']
data.loc['1989-01-03':'1989-01-05', 'flow']
# %%
data.iloc[2:5, 2]
# %% return multiple columns skip (columns 0-5, go by 2)
data.iloc[2:5, 0:6:2]
# %%
data.flow.head()[2:5]

# %%
data.flow['1989-01-03':'1989-01-05']