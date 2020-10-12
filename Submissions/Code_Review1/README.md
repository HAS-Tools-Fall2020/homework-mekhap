# Code Review Assignment, Week 7
###### Code author: Mekha (modified code from Laura)
###### Code reviewer: Patrick

---
#### INSTRUCTIONS

*Step 1.* Once data for Saturday 10/20/2020 is available, download the daily discharge data for our USGS gage [here.](https://waterdata.usgs.gov/nwis/dv/?site_no=09506000&agency_cd=USGS) Choose *Tab-separated* as the Output Format, enter *1989-01-01* for the Begin Date, and *10-10-2020* for the End Date, then click GO. Once the data loads, right click on the page and Save as a text file with the filename *streamflow_week7.txt* in the folder named *data*, which is located within the *homework-mekhap* folder.

*Step 2.* Check that *streamflow_week7.txt* is in the correct format. In previous weeks when we save the tab separated table to a text file, the first line of data (USGS	09506000	1989-01-01	207	A) is on line 31. When I tried saving data to a text file on Friday as test, there was an extra line space in the text file for some reason and the first line of data was on line 32 (which broke my code and took me longer than it should have to figure out...). So as a check, please open *streamflow_week7.txt* in Atom and make sure the first line of data is on line 31. If it is not, delete some of the line spaces in the top section to make sure the data starts on line 31, and save the file. You can open *streamflow_week6.txt* for an example of what the format should look like.

*Step 3.* Open and run the *Pereira_HW7.py* script. The script is broken into several blocks, and you will need to click Run on each one, in order.
* First the script will generate a 1 week and 2 week forecast using an autoregression (AR) model. Enter these forecast values in the space below, but do not use these values as the final values to submit for the forecast competition.
* Next the code will generate a 1 week and 2 week forecast based on average flows over the past two weeks. Enter these forecast values in the space below, and use these values as the final values to submit for the forecast competition.
* Next the code will generate four plots to visualize the AR model. These are optional to run.

*Step 4.* Update week 7 entries in the *pereira.csv* file in the *forecast_entries* folder with the 1 week and 2 week forecast generated in the final part of the script (based on the averages over the past two weeks of flow data). Push to Github. (You can leave the long term forecast blank)

*Step 5.* Review my code following the code review rubric in the *Starter_Codes* folder, and provide feedback to the three questions in the space below. I'm new to coding and appreciate the feedback, so thank you!!

---
#### FORECAST VALUES FROM CODE

* 1 week forecast based on AR model: 85.85
* 2 week forecast based on AR model: 106.59


* 1 week forecast based on last week's average flow: 61.86
* 2 week forecast based on last two weeks' average flow: 59.57

---
#### CODE REVIEW

1. Is the script easy to read and understand?
The script is very easy to read! You could change a couple of things though, like your function doesn't need to be named model3_... especially if you change the name of your model. Also if you are going to label by steps, make sure you account for when you remove numbers so that the count stays consistent (I got confused when there wasn't a step 5). Also if you are going to do something like line 118-121, I would say don't make it its own cell since it doesn't have any code to run.   3

2. Does the code follow PEP8 style consistently?
Yes, but make sure to move your functions to the top of your script by your initial imports!   3

3. Is the code written succinctly and efficiently?
The code was written well, I can tell that you went back and removed anything unnecessary.   3
