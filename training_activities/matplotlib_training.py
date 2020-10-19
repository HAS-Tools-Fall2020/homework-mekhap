# %%
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

# %% Create dummy dataset for plotting
x=np.linspace(0,10,100)
y=np.sin(x)

# set style, don't have to set a style at top
plt.style.use('classic') 

#easiest plot
plt.plot(x,y)

#fancier plot
plt.plot(x,y,color='red',linestyle='dashed')
plt.plot(x,y,':r') # shorthand for red dashed line

# Changing axes, title, etc with additional commands
plt.plot(x,y,color='red',linestyle='dashed',label="sinx")
plt.plot(x,np.cos(x),label="cosx")
plt.xlim(-1,5)
plt.ylim(-2,2)
plt.xlabel('xx')
plt.ylabel('sinxx')
plt.title('demo plot')
plt.legend()

# pts instead of line
plt.plot(x,y,'p',color='red')

#can combine with a line too
plt.plot(x,y,'d',color='red',linestyle='solid')

#can control the color and style for both lines and points
plt.plot(x,y,'-p',color='gray',
        markersize=4, linewidth=1,
        markerfacecolor='purple',markeredgecolor='yellow',
        markeredgewidth = '0.5')

# %% sophisticated way to make scatter plot
plt.scatter(x,y, marker='p')

#Can have color change with xvalue
plt.scatter(x,y, c=x, marker='p')

#Can have size change with a random value
size = 1000*np.random.rand(len(x))
plt.scatter(x,y, c=x, s=size, marker=',')

#A bettwe way to set up your plot

#Thi creates a plottin gobject we will use
# Fig is our overall figure, use this to chaneg things like plot dimensions
# ax is our graph inside the figures
fig,ax = plt.subplots()

ax.plot(x,y,color='red',linestyle='dashed',label="sinx")
ax.plot(x,np.cos(x),label="cosx")
ax.set_xlim(-1,5)
ax.set_ylim(-2,2)
ax.set_xlabel('xx')
ax.set_ylabel('sinxx')
ax.set_title('demo plot')

plt.show()

# can be consie like this
fig,ax = plt.subplots()
ax.plot(x,y,color='red',linestyle='dashed',label="sinx")
ax.plot(x,np.cos(x),label="cosx")
ax.set(xlim=(-1,5),ylim=(-2,2),xlabel="xx", ylabel='sinxx')

# Can make multiplot and refer to them using this approach
fig,ax=plt.subplots(2,2)
ax=ax.flatten()
ax[0].plot(x,y)
ax[1].plot(x,y)
ax[3].plot(x,np.cos(x),color='red')
ax[2].plot(x,np.cos(x))
ax[1].set_xlim(2,4)
plt.show()

# without flatten
fig, [[ax1,ax2],[ax3,ax4]]=plt.subplots(2,2)
ax=ax.flatten()
ax1.plot(x,y)
ax2.plot(x,y)
ax3.plot(x,np.cos(x),color='red')
ax4.plot(x,np.cos(x))
ax1.set_xlim(2,4)
plt.show()

# %%
# Plot flow timeseries with 25% error, separate lines

flow = np.random.randn(100)
day = range(len(flow))
upper = 1.25 * flow
lower = .75 * flow

fig, ax = plt.subplots()
ax.plot(flow, label='flow')
ax.plot(upper, label='25% error',linestyle='--', color='grey')
ax.plot(lower,linestyle='--', color='grey')
ax.legend()
plt.show()

# %%
# Plot flow timeseries with 25% error, fill between
fig, ax = plt.subplots()
ax.plot(flow, label='flow')
ax.fill_between(day, flow*0.75, flow*1.25, color='gray',alpha=0.2, label='25% error')
ax.legend()
plt.show()

# %%
# Plot flow timeseries with 25% error, error bar
dy = flow*0.25
plt.errorbar(day, flow, yerr=dy, fmt='.k');

# %% fund with functions
x = np.arange(2,11).reshape(3,3)
y = 3
answer = np.floor(np.divide(x,y))
print(answer)

# %%
def get_floor(numerator, denominator):
        fl = np.floor(np.divide(numerator, denominator))
        return fl


get_floor(x,y) # returns array but doesn't save variable
floor = get_floor(x,y) # saves variable but wil not return anything
print(floor)

# %%
def get_floor(numerator, denominator):
        fl = np.floor(np.divide(numerator, denominator))
        print(fl)


floor = get_floor(x,y)

# %%
def get_floor(numerator, denominator):
        fl = np.floor(np.divide(numerator, denominator))
        print(fl)
        return(fl)


floor = get_floor(x,y)
