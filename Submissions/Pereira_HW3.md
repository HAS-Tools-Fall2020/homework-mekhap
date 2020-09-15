# Homework 3 Markdown
*Mekha Pereira*
*09/13/2020*

---------
# Grade

3/3 - Great job! I like your approach

---
## Assignment Questions

*Question 1.* Describe the variables flow, year, month, and day. What type of objects are they, what are they composed of, and how long are they?

* flow is a list containing float variables which reports the observed average daily flow in cfs
* year is a list containing int variables which reports the year the flow was observed
* month is a list containing int variables which reports the month the flow was observed
* day is a list containing int variables which reports the day the flow was observed
* all lists are 11578 elements long, indexed from 0 to 11577

*Question 2.* How many times was the daily flow greater than your prediction in the month of September (express your answer in terms of the total number of times and as a percentage)?

My forecast made 8/31 for the first two weeks of September was 300 cfs. This was simply based on the 2019 average daily flow over the entire 16 week period of interedst (rounded).

Over the period 1/1/1989-9/12/2020, flow exceeded 300 cfs 79 times out of 942, or approximately 8.4% of the time.

*Question 3.* How would your answer to the previous question change if you considered only daily flows in or before 2000? Same question for the flows in or after the year 2010? (again report total number of times and percentage)

Over the period 1/1/1989-12/31/2000, flow exceeded 300 cfs 49 times out of 360, or approximately 13.6% of the time.

Over the period 1/1/2010-9/12/2020, flow exceeded 300 cfs 12 times out of 312, or approximately 3.8% of the time.

*Question 4.* How does the daily flow generally change from the first half of September to the second?

Considering September data from 1989-2019 because 2020 is not a complete September month:

September 1-15:
* Min =  48.6
* Max =  1280.0
* Average =  182.2
* Standard Dev = 172.2

September 15-30:
* Min =  51.2  
* Max =  5590.0
* Average =  169.9
* Standard Dev = 372.0

The range of min to max flow increases from the first half of the month to the second, but the average flow is lower in the second half of the month than the first. The higher standard deviation indicates the second half of September is more likely to see extreme flood events.

-------

## Justification for Forecast

For the one week and two week forecast, I looked at the statistics for the most recent week of data through 09/12/2020, and plotted the flows for the past two weeks of data. I made a guess based on the increasing trend over the past few days.

For the long term forecast, I wrote for-loops to isolate each of the 16 weeks of data for a given year, and printed the weekly average. The year variable could be changed, so I ran this code repeatedly changing the year from 1989-2019, looking for the low flow years since we know this has been a bad monsoon season. The weekly averages for 2019 seemed lowest, except for week 15 and 16 which saw a large flood event. I used the weekly 2019 average values for my forecast, and repeated the week 14 average for weeks 15 and 16.
