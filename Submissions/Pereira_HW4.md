# Homework 3 Markdown
*Mekha Pereira*
*09/20/2020*

---------
## Justification for Forecast

*Question 1.* Include discussion of the quantitative analysis that lead to your prediction. This can include any analysis you complete but must include at least two histograms and some quantitative discussion of flow quantiles that helped you make your decision.

First I just created a line plot showing the September 2020 daily flows (9/1/20 - 9/19-20). In the past few days, there has been a downward trend in daily flow with Saturday's flow around 55 cfs.

Next I calculated the mean of last week's flow (9/13-9/19) which was 56.2 cfs. Considering historical September data through 2019, flow in September has exceeded this value 97.4% of the time.

Next, for the 1 week forecast period of Sept 20-26, I created a histogram of 1989-2019 data for this week. I only plotted the low end of the distribution (flows up to 100 cfs) because we know that so far, this has been a low flow year. Based on this distribution, we can see that this year's September flow is on the lowest end of observed flows for this week in September. I then calculated the quantiles to show the minimum, 10%, 50%, and 90% quantiles. The results show that historically, 10% of the data for the week of interest is below 80.14 cfs, which is still larger than observed September 2020 flow. The observed flow for the past week of September has been below 2.5% of the data. I recalculated the quantiles to show the minimum, 2.5%, 5%, and 10% quantiles. This showed 2.5% of the data is below 67.6 cfs.

I did the same calculations for the 2 week forecast period of Sept 27 - Oct 3. Results are shown below.

|date range      |0% (min)|10%    |50%     |90%    |
|:--------------:|:------:|:-----:|:------:|:-----:|
|Sept 20 -Sept 26|51.2    |80.14  |110     |223.8  |
|Sept 27 - Oct 3 |71.3    |81.06  |107     |197    |

|date range      |0% (min)|2.5%   |5%      |10%    |
|:--------------:|:------:|:-----:|:------:|:-----:|
|Sept 20 -Sept 26|51.2    |67.6   |72.44   |80.14  |
|Sept 27 - Oct 3 |71.3    |75.7   |78.16   |81.06  |

Because observed September 2020 flow has been even less than the 2.5% quantile, I chose the minimum overserved flow value for the one week forecast. For the two week forecast, I predicted slightly less than the 1 week forecast based on the recent trend seen in the initial line graph.

## Other Assignment Questions

*Question 2.* Describe the variable flow_data:

* flow_data is a numpy array
* it is composed of floats
* it is a 2-dimensional array with 11585 columns, 4 rows, and its total size is 46340 elements

*Question 3.* How many times was the daily flow greater than your prediction in the month of September (express your answer in terms of the total number of times and as a percentage)??????

My forecast made 9/7, I predicted 55 cfs for average weekly flow.

Over the period 1/1/1989-9/20/2020, flow exceeded 55 cfs 919 times out of 949, or approximately 96.8% of the time.

*Question 4.* How would your answer to the previous question change if you considered only daily flows in or before 2000? Same question for the flows in or after the year 2010? (again report total number of times and percentage)

Over the period 1/1/1989-12/31/2000, flow exceeded 55 cfs 360 times out of 360, or 100% of the time.

Over the period 1/1/2010-9/12/2020, flow exceeded 55 cfs 301 times out of 319, or approximately 94.4% of the time.

*Question 5.* How does the daily flow generally change from the first half of September to the second?

Considering September data from 1989-2019 because 2020 is not a complete September month:

* Mean 1st half:  182.1982795698925
* Mean 2nd half:  169.8541935483871
* Median 1st half:  137.0
* Median 2nd half:  111.0
* Std Dev 1st half:  172.15874231702526
* Std Dev 2nd half:  371.9750870786179

On average, the flow decreases from 182 cfs to 170 cfs, but the much higher standard deviation in the second half of the month (372 cfs compared to 172 cfs) indicates the second half of September is more likely to see extreme flood events.
