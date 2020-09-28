# %%
import numpy as np
import os

# Training activities Earth Science textbook Ch 14
# %% 1D array
month_precip = np.array([.70, .75, 1.85])
print(month_precip)

# %% 2d array
precip_03_13 = np.array([[1.07,.44,1.5],[.27,1.13,1.72]])
print(precip_03_13)

# %% practice array (try importing csv data later)
precip_03_13 = np.array([[1.07,0.44,1.5,0.2,3.2,1.18,0.09,1.44,1.52,2.44,0.78,0.02],[0.27,1.13,1.72,4.14,2.66,0.61,1.03,1.4,18.16,2.24,0.29,0.5]])
print(precip_03_13)

print(month_precip.ndim)
print(month_precip.shape)
print(precip_03_13.ndim)
print(precip_03_13.shape)

# %% can perform calcs on numpy arrays, unlike lists

print(month_precip)
#month_precip_mm = month_precip*25.4
#print(month_precip_mm)

#month_precip *= 25.4
#print(month_precip)

# %% Summary stats 1D arrays
mean_month_precip = np.mean(month_precip)
median_month_precip = np.median(month_precip)

# %% Summary stats 2D arrays
print(np.mean(precip_03_13,axis=0)) # 12 values, mean of each column
print(np.mean(precip_03_13,axis=1)) # 2 values, mean of each row
max_precip_03_13 = np.max(precip_03_13,axis=0)
print(max_precip_03_13)

# %% Indexing 1D
print(month_precip)
print(month_precip[0])
print(month_precip[1])
print(month_precip[2])

# %% Indexing 2D
test2d = np.array([[1,2,3],[4,5,6]])
print(test2d)
print(test2d[0,2]) # index = row,column

# %% Slicing 1D
avg_monthly=np.array([0.7,0.75,1.85,2.93,3.05,2.02,1.93,1.62,1.84,1.31,1.39,0.84])
print(avg_monthly[11]) # last element - explicit
print(avg_monthly[-1]) # las element - universal

# %% Slicing 2D
print(precip_03_13)
print(precip_03_13[1,5]) # row 2, col 6
print(precip_03_13[1,11]) # last element, row 2, col 12
print(precip_03_13[-1,-1]) # last element, universal
print(precip_03_13[0:1, 0:2]) # row 1, col 1 & 2
print(precip_03_13[0:2, 0:1]) # row 1&2, col 1
print(precip_03_13[1:2, 1:3]) # row 2, col 2&3
print(precip_03_13[:2, :2]) # first 2 rows and cols

# %% Shorcuts
print(precip_03_13)
print(precip_03_13[:,0]) # entire 1st col
print(precip_03_13[0,:]) # entire 1st row
precip_03 = precip_03_13[0,:] # new numpy array of first row 2003 values
precip_13 = precip_03_13[1] # to select a row, just provide index for row by itelf
print(precip_13)

# Python Data Science Handbook trainings

# %% Basics of Numpy Arrays

np.random.seed(0) # seed for reproducibility

x1 = np.random.randint(10, size=6) # One-dimensional array
x2 = np.random.randint(10, size=(3, 4)) # Two-dimensional array
x3 = np.random.randint(10, size=(3, 4, 5)) # Three-dimensional array

print("x3 ndim: ", x3.ndim)
print("x3 shape:", x3.shape)
print("x3 size: ", x3.size)
print("dtype:", x3.dtype)
print("itemsize:", x3.itemsize, "bytes")
print("nbytes:", x3.nbytes, "bytes")
x1 # entire array
x1[0] # 1st element
x1[4] # 5th element
x1[-1] #last element
x1[-2] #2nd to last element
x2
x2[2,-1] #3rd row, las col
x2[0,0] = 12 # set first element to 12
x1[0] = 3.14159 # this will become an int

# %% slicing 1d
x = np.arange(10)
# slicing sytax x[start:stop:step]
x[:5] # first five elements
x[5:] # elements after index 5
x[4:7] # middle sub-array
x[::2] # every other element
x[1::2] # every other element, starting at index 1
x[::-1] # all elements, reversed
x[5::-2] # reversed every other from index 5

# %% slicing 2d
x2
x2[:2, :3] # two rows, three columns
x2[:3, ::2] # all rows, every other column
x2[::-1, ::-1] # dimensions reversed together
print(x2[:, 0]) # first column of x2
print(x2[0, :]) # first row of x2
print(x2[0]) # simplification for row only, equivalent to x2[0, :]

# %% extract slices
print(x2)
x2_sub = x2[:2, :2] # extract 2x2 subarray
print(x2_sub)
x2_sub[0, 0] = 99 # this will change original array x2
print(x2_sub)
print(x2)

# %% make copy of arrray
x2_sub_copy = x2[:2, :2].copy()
print(x2_sub_copy)
x2_sub_copy[0, 0] = 42 # will not modify original
print(x2_sub_copy)
print(x2)

# %% Reshaping arrays
grid = np.arange(1, 10).reshape((3, 3)) #arrange numbers 1-9 in 3x3 grid
print(grid)

y = np.array([1, 2, 3])
# row vector via reshape
y.reshape((1, 3))

# row vector via newaxis
y[np.newaxis, :]

# column vector via reshape
y.reshape((3, 1))

# column vector via newaxis
y[:, np.newaxis]

# %% Concatenation

x = np.array([1, 2, 3])
y = np.array([3, 2, 1])
np.concatenate([x, y])
z = [99, 99, 99]
print(np.concatenate([x, y, z]))

# concatenate 2D
grid = np.array([[1, 2, 3], [4, 5, 6]])
# concatenate along the first axis
np.concatenate([grid, grid])

# concatenate along the second axis (zero-indexed)
np.concatenate([grid, grid], axis=1)

# stack arrays of diff sizes
x = np.array([1, 2, 3])
grid = np.array([[9, 8, 7], [6, 5, 4]])
# vertically stack the arrays
np.vstack([x, grid])

# horizontally stack the arrays
y = np.array([[99],[99]])
np.hstack([grid, y])

# %% Splitting of arrays

x = [1, 2, 3, 99, 99, 3, 2, 1]
x1, x2, x3 = np.split(x, [3, 5]) #Notice that N split-points, leads to N + 1 subarray
print(x1, x2, x3)

grid = np.arange(16).reshape((4, 4))
grid
upper, lower = np.vsplit(grid, [2])
print(upper)
print(lower)
left, right = np.hsplit(grid, [2])
print(left)
print(right)

# %% Computations

# we have an array of values and we'd like to compute the reciprocal of each

#for loop method
np.random.seed(0)
def compute_reciprocals(values):
    output = np.empty(len(values))
    for i in range(len(values)):
        output[i] = 1.0 / values[i]
    return output
 
values = np.random.randint(1, 10, size=5)
compute_reciprocals(values)

# takes a long time because of type checking
big_array = np.random.randint(1, 100, size=1000000)
%timeit compute_reciprocals(big_array)

# faster method using universal functions

print(compute_reciprocals(values))
print(1.0 / values) # computation on scalar and array

np.arange(5) / np.arange(1, 6) # computatoin on two 1D arrays
x = np.arange(9).reshape((3, 3))# computation on multidimensional arrays
2 ** x

# %% Array arthimetic
x = np.arange(4)
print("x =", x)
print("x + 5 =", x + 5)
print("x - 5 =", x - 5)
print("x * 2 =", x * 2)
print("x / 2 =", x / 2)
print("x // 2 =", x // 2) # floor division
print("-x = ", -x)
print("x ** 2 = ", x ** 2)
print("x % 2 = ", x % 2)
print(-(0.5*x + 1) ** 2)
print(np.add(x, 2))

# + np.add Addition (e.g., 1 + 1 = 2 )
# - np.subtract Subtraction (e.g., 3 - 2 = 1 )
# - np.negative Unary negation (e.g., -2 )
# * np.multiply Multiplication (e.g., 2 * 3 = 6 )
# / np.divide Division (e.g., 3 / 2 = 1.5 )
# // np.floor_divide Floor division (e.g., 3 // 2 = 1 )
# ** np.power Exponentiation (e.g., 2 ** 3 = 8 )
# % np.mod Modulus/remainder (e.g., 9 % 4 = 1 )

x = np.array([-2,-1, 0, 1, 2])
abs(x)
np.absolute(x)
np.abs(x)

# ufunc can also handle complex data, in which the absolute value returns the magnitude:
x = np.array([3 - 4j, 4 - 3j, 2 + 0j, 0 + 1j])
np.abs(x)

# %% Trig functions
theta = np.linspace(0, np.pi, 3) # define array of angles
print("theta = ", theta)
print("sin(theta) = ", np.sin(theta))
print("cos(theta) = ", np.cos(theta))
print("tan(theta) = ", np.tan(theta))

# inverse trig functions
x = [-1, 0, 1]
print("x = ", x)
print("arcsin(x) = ", np.arcsin(x))
print("arccos(x) = ", np.arccos(x))
print("arctan(x) = ", np.arctan(x))

# %% Exponential functions
x = [1, 2, 3]
print("x =", x)
print("e^x =", np.exp(x))
print("2^x =", np.exp2(x))
print("3^x =", np.power(3, x))

x = [1, 2, 4, 10]
print("x =", x)
print("ln(x) =", np.log(x))
print("log2(x) =", np.log2(x))
print("log10(x) =", np.log10(x))

# maintain precision small inputs
x = [0, 0.001, 0.01, 0.1]
print("exp(x) - 1 =", np.expm1(x))
print("log(1 + x) =", np.log1p(x))

# %% Specialized functions
from scipy import special

# Gamma functions (generalized factorials) and related functions
x = [1, 5, 10]
print("gamma(x) =", special.gamma(x))
print("ln|gamma(x)| =", special.gammaln(x))
print("beta(x, 2) =", special.beta(x, 2))

# Error function (integral of Gaussian)
# its complement, and its inverse
x = np.array([0, 0.3, 0.7, 1.0])
print("erf(x) =", special.erf(x))
print("erfc(x) =", special.erfc(x))
print("erfinv(x) =", special.erfinv(x))

# Specify function output

x = np.arange(5)
y = np.empty(5)
np.multiply(x, 10, out=y) # store output in y
print(y)

y = np.zeros(10)
np.power(2, x, out=y[::2]) # specify array view of y
print(y)

# Aggregates

#reduce repeatedly applies an operation on all elements until a single value remains
x = np.arange(1, 6)
np.add.reduce(x)
np.multiply.reduce(x)
np.add.accumulate(x) # store intermediate steps
np.multiply.accumulate(x)

#outer product
# any ufunc can compute the output of all pairs of two diwerent inputs using the outer method.
x = np.arange(1, 6)
np.multiply.outer(x, x)


# summing values in array
L = np.random.random(100)
sum(L)
np.sum(L)

#big_array = np.random.rand(1000000)
#%timeit sum(big_array)
#%timeit np.sum(big_array)

np.min(big_array)
np.max(big_array)

print(big_array.min(), big_array.max(), big_array.sum()) #shorter syntax

M = np.array([[0,0,0,0],[1,1,1,1],[2,2,2,2],[3,3,3,3]])
print(M)
M.sum()
M.min(axis=0) # min of each col
M.max(axis=1) # max of each row

# NOTE: Function NameNaN-safe Version Description
# np.sum np.nansum Compute sum of elements
# np.prod np.nanprod Compute product of elements
# np.mean np.nanmean Compute mean of elements
#np.std np.nanstd Compute standard deviation
#np.var np.nanvar Compute variance
#np.min np.nanmin Find minimum value
#np.max np.nanmax Find maximum value
#np.argmin np.nanargmin Find index of minimum value
#np.argmax np.nanargmax Find index of maximum value
#np.median np.nanmedian Compute median of elements
#np.percentile np.nanpercentile Compute rank-based statistics of elements
#np.any N/A Evaluate whether any elements are true
#np.all N/A Evaluate whether all elements are true


# %% INTRO TO BROADCASTING

# operations performed on element by element basis
a = np.array([0, 1, 2])
b = np.array([5, 5, 5])
a + b

a + 5 # add scalar through broadcasting

#arrays diff sizes
M = np.ones((3, 3))
M
M + a

a = np.arange(3)
b = np.arange(3)[:, np.newaxis]
print(a)
print(b)
a + b # both arrays exanpded to match size of other, then added

# Rules of Broadcasting
# Broadcasting in NumPy follows a strict set of rules to determine the interaction
# between the two arrays:
# Rule 1: If the two arrays differ in their number of dimensions, the shape of
# the one with fewer dimensions is padded with ones on its leading (lex)
# side.
# Rule 2: If the shape of the two arrays does not match in any dimension, the
# array with shape equal to 1 in that dimension is stretched to match the
# other shape.
# Rule 3: If in any dimension the sizes disagree and neither is equal to 1, an
# error is raised.

# %% Proadcasting examples
M = np.ones((2, 3))
a = np.arange(3)
print(M)
print(a)
print(M + a)

a = np.arange(3).reshape((3, 1))
b = np.arange(3)
print(a)
print(b)
print(a+b)

M = np.ones((3, 2))
a = np.arange(3)
print(M)
print(a)
# print(M+a) does not work, dimensions not compatible

a[:, np.newaxis]
a[:, np.newaxis].shape
print(M+a[:, np.newaxis])

# %% Centering array
# Imagine you have an array of 10 observations, each of which consists of 3 values.

X = np.random.random((10, 3))

Xmean = X.mean(0) # mean of each feature
Xmean

X_centered = X - Xmean
X_centered
X_centered.mean(0)

# %% Plotting 2D function

# x and y have 50 steps from 0 to 5
x = np.linspace(0, 5, 50)
y = np.linspace(0, 5, 50)[:, np.newaxis]
z = np.sin(x) ** 10 + np.cos(10 + y * x) * np.cos(x)





#%% In class practice

list2 = [True, 'test', 3.14, 4]
print(type(list2))
[type(i) for i in list2]

# %%
list3 = [1,1.3,5]
# list3 + 7 #this does not work
[i+7 for i in list3] #this works

# %%
# numpy arrays
array1 = np.array([1,1.3,5]) #all values now floats
print(array1.ndim)
print(array1.shape)
print(array1.size)
print(array1+7)

# %%
arr_zero = np.zeros(10, dtype=int)
print(arr_zero.ndim)
print(arr_zero.shape)
print(arr_zero.size)
print(arr_zero+7)

# %% 1d arrat of zeros
arr_0 = np.zeros(10)
print(arr_0)

# %% 2d array of sevens
arr_sev= np.ones((3,5))*7
print(arr_sev)

# %% 2d array of sevens
arr_7 = np.full((3,5),7.)
print(arr_7)

# %% Course materials, content, class python

# NOTE: axis0 = rows, axis1 = columns
