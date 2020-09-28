# %%
import numpy as np
import os

# %% Create 3x3 matrix with values ranging  from 2-10 by combining row and column vector
x=np.arange(2,5,1)
y=np.arange(0,7,3).reshape(3,1)
z = x+y
print(z)
print(z+x)

# %% #1. Get the largest integer that is less than or equal to the division
# of the inputs x1 and x2 where x1 is all the integers from 1-10 and x2=1.3

x1 = np.divide(np.arange(1,11,1),1.3).astype(int)

x2 = np.arange(1,11)
x3 = 1.3
answer = np.floor_divide(x2,x3)

# %% 2. given an array x1=[0, 4, 37,17] and a second array with the values
# x2=[1.2, 3, 4.6, 7] return x1/x2 rounded to two decimal places

x1=[0, 4, 37,17]
x2=[1.2, 3, 4.6, 7]
answer = np.round(np.divide(x1,x2), decimals=2)
print(answer)

# %% 3. Create a 10 by 100 matrix with 1000 random numbers and report the 
# average and standard deviation across the entire matrix and 
# for each of the 10 rows. Round your answer to  two decimal places

# hint np.random, np.round, np.std

# %%
x2 = np.random.randint(1000, size=(10, 100)) # Two-dimensional array
np.std

# %%