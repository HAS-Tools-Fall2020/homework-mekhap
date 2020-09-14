# Week 3 Training Activities

# %%
list = [1,3,8,"text"]
list[3]

# %%
precip_by_location =[46.23,"inches","New York City"]
precip_by_location[2]

# %%
precip_by_location[2]="New Jersey"
precip_by_location
# %%
precip_by_location.insert(0,"January")
precip_by_location

# %%
del precip_by_location[0]
precip_by_location
# %%
precip_by_location.append("XXX")
precip_by_location
# %%
addition = [-9999]+precip_by_location
addition
# %%
precip_by_location += [-3333]
precip_by_location
# %%
listoflists = [[1,2,3],[7,8,9]]
listoflists[0]
type(listoflists)
type(listoflists[0])
# %% Arithmetic
a=2
b=3
a+b
b-a
b/a
a*b
a**b #exponent
# %%Assignment Operators with Arithmetic
c = 10
c *=4 #set C equal to c times 4
c
# %%
months = ["Jan", "Feb"]
months += ["Mar", "Apr"]
months
# %%
list2 = [1,2,3,5]
list2 *=10
list2 #end up printing lsit 10 times
# %% Relational Operators (Boolean)
a == b
a != b
a > b
a >= b

# %%
check = (3>2)
check
# %%
precip = "precipitation"
"tation" in precip
# %%
temps = [70,75,80]
70 in temps
65 not in temps
70 in temps and 75 in temps
65 in temps or 70 in temps
# %%
l1 = [1,2,3]
l2 = [1,2,3]
l1 == l2 # true because same content
l1 is l2 # false because diff objects w/ diff python ids
l3 = l1
l3 is l1 #true

# %%
boulder_precip_months = ["jan", "feb", "mar", "apr", "may", "june", "july", "aug", "sept", "oct", "nov", "dec"]
boulder_precip_inches = [0.70, 0.75, 1.85 , 2.93, 3.05 , 2.02, 1.93, 1.62, 1.84, 1.31, 1.39, 0.84]
mmconversion = 25.4
boulder_precip_mm = boulder_precip_inches.copy()
boulder_precip_mm[0]*=mmconversion
boulder_precip_mm[1]*=mmconversion
boulder_precip_mm[2]*=mmconversion
boulder_precip_mm[3]*=mmconversion
boulder_precip_mm[4]*=mmconversion
boulder_precip_mm[5]*=mmconversion
boulder_precip_mm[6]*=mmconversion
boulder_precip_mm[7]*=mmconversion
boulder_precip_mm[8]*=mmconversion
boulder_precip_mm[9]*=mmconversion
boulder_precip_mm[10]*=mmconversion
boulder_precip_mm[11]*=mmconversion

# %%
all_boulder_data = [[boulder_precip_months],boulder_precip_mm]
all_boulder_data

# %%
# Import necessary plot package
import matplotlib.pyplot as plt

# Plot monthly precipitation values
fig, ax = plt.subplots(figsize=(12, 12))
ax.bar(boulder_precip_months, 
       boulder_precip_mm, 
       color="aqua")
ax.set(title="Boulder Monthly Precip mm",
       xlabel="Month", 
       ylabel="Precip mm")
plt.show()
# %%
oldlist = [10,20,30]
newlist = [i *10 for i in oldlist]
newlist
# %% Conditional Statements
 x = 11
 if x == 10:
     print("x is 10")
else:
    print("x is",x,",not 10")

# %%
if 0.70 in boulder_precip_inches:
    print("Value is in list")
else:
    print("Value is not in list")

# %%
if "QWERTY" in "POIUYQWERTY":
    print("This text string contain the word QWERTY")
else:
    print("This text string does not contain the word QWERTY")

# %%
x = 0.5
if type(x) is int:
    print(x, "is an integer.")
else:
    print(x, "is not an integer.")
# %%
x = 15
y = 10
if x < y:
    print("x started with value of", x)
    x += 5
    print("It now has a value of", x, "which is equal to y.")
elif x > y:
    print("x started with value of", x)
    x -= 5
    print("It now has a value of", x, "which is equal to y.")
else:
    print("x started with a value of", x, "which is already equal to y.")
# %%
if "precip" in "avg_monthly_temp":
    fname = "avg_monthly_temp"
    print(fname)
elif "precip" in "avg_monthly_preci":
    fname = "avg_monthly_precip"
    print(fname)  
else:
    print("Neither textstring contains the word precip.")
# %%
avg_monthly_precip = [0.70,  0.75, 1.85, 2.93, 3.05, 2.02, 1.93, 1.62, 1.84, 1.31, 1.39]
# Add value to list depending on existing last value
if avg_monthly_precip[-1] == 0.84:   
    print(avg_monthly_precip[-1]) # Print last value in the list

elif avg_monthly_precip[-1] == 1.39:   
    avg_monthly_precip += [0.84] # Add Dec value
    print(avg_monthly_precip)    

else:     
    print("The last item in the list is neither 0.84 nor 1.39.")
# %%
# Set x equal to 5 and y equal to 10
x = 5
y = 10

# Add x and y if they are both integers
if type(x) is int and type(y) is int:
    print(x + y)
else:
    print("Either x or y is not an integer.")
# %%
months = ["Jan", "Feb", "Mar", "Apr", "May", "June", "July", "Aug", "Sept", "Oct", "Nov"]

# Length of avg_monthly_precip
precip_len = len(avg_monthly_precip) 
print(precip_len)

# Length of months
months_len = len(months)
print(months_len)
# %%
# Check whether both type and length of avg_monthly_precip and months match
if type(avg_monthly_precip) is type(months) and precip_len == months_len:
    print("Objects are of the same type and have the same length.")
else:
    print("Objects are not of the same type or do not have same length.")
# %%
# Set x equal to 0 and y equal to 10
x = 0
y = 10

# Check whether either is equal to zero
if x == 0 or y == 0:
    print("Either x or y is equal to 0.")
    x += 1
    y += 1
    print("x is now", x, "and y is now", y)

else:
    print("Neither x nor y is equal to 0.")
# %%
# Check match for either type and length of avg_monthly_precip and months
if type(avg_monthly_precip) is type(months) or precip_len == months_len:
    print("Objects have either the same type or length.")
else:
    print("Objects either do not have the same type or same length.")
# %%
list_of_values = [1, 2, 3, 4, 5]
for avalue in list_of_values:
    print(avalue)
# %%
for avalue in list_of_values:
    print("the current value is:", avalue)
# %%
for avalue in list_of_values:
    print("the current value is:", avalue+1)
# %%
num_list = [12, 5, 136, 47]
for i in num_list:
    i += 10
    print(i)
# %%
num_list = [12, 5, 136, 47]
for x in num_list:
    x += 10
    print("The value of the variable 'x' is:", x)
# %%
num_list = [12, 5, 136, 47]
for banana in num_list:
    banana += 10
    print("The value of the variable 'banana' is:", banana)
# %%
files = ["months.txt", "avg-monthly-precip.txt"]
for fname in files:
    print("The value of the variable 'fname' is:", fname)
# %%
# Create list of abbreviated month names
months = ["Jan", "Feb", "Mar", "Apr", "May", "June",
          "July", "Aug", "Sept", "Oct", "Nov", "Dec"]

# Create list of average monthly precip (inches) in Boulder, CO
avg_monthly_precip = [0.70,  0.75, 1.85, 2.93, 3.05, 2.02,
                      1.93, 1.62, 1.84, 1.31, 1.39, 0.84]

# List of list names
lists = [months, avg_monthly_precip]

# For each item in list, print value
for dlist in lists:
    print("The value of the variable 'dlist' is:", dlist)
# %%
# For each list in lists, print the length
for dlist in lists:
    print("The length of the variable 'dlist' is:", len(dlist))
# %%
# For each list in lists, print the value at last index
for dlist in lists:
    print(dlist[-1])
# %%
# For each list in lists, print attribute shape
for dlist in lists:
    print(dlist.shape) # will not nork b/c lists do not have sape, numpy array has shape
# %%
