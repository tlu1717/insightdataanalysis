# Insight Data Engineering Coding Challenge 

author: Tiffany Lu
environment: python3
library: sys

## Problem
(Copied from https://github.com/InsightDataScience/h1b_statistics)
A newspaper editor was researching immigration data trends on H1B(H-1B, H-1B1, E-3) visa application processing over the past years, trying to identify the occupations and states with the most number of approved H1B visas. She has found statistics available from the US Department of Labor and its Office of Foreign Labor Certification Performance Data. But while there are ready-made reports for 2018 and 2017, the site doesn’t have them for past years.

As a data engineer, you are asked to create a mechanism to analyze past years data, specificially calculate two metrics: Top 10 Occupations and Top 10 States for certified visa applications.

Your code should be modular and reusable for future. If the newspaper gets data for the year 2019 (with the assumption that the necessary data to calculate the metrics are available) and puts it in the input directory, running the run.sh script should produce the results in the output folder without needing to change the code.


## Approach
I split the data cleaning and processing into 3 parts: extracting, getting-occupations and getting-states. 

										extracting
									/       		 \
						   get_occupations  		get_states
						         | 						|
				top_10_occupations.txt  			top_10_states.txt


### Extracting Data - read_csv()
This is the read_csv(path) function in parsedata.py. It gets the csv data line by line and split them up by the ';' delimiter. It also filters for only the applications that are certified. It outputs a list of lists where each internal list represents a row of a table. The input data, or the csv file, must contain the column that represents the application status. If there is not such column, the function will return -1. 

### Getting Occupations - get_occupations()
The get_occupations() function gets the top 10 frequent soc titles in the certified application data (returned from read_csv). The input data must contains a column or attribute that is the soc-title (this is implemented as keyword searching). If the input data did not have a soc-title related column, the function will return -1. The top 10 frequent soc titles will not include empty strings, although the total number of certified application do include entries with empty strings as soc titles. 
### Getting States - get_states()
The get_states() function is similar to get_occupations() as the only difference is that it looks at the work_state column to get the 10 most frequent states. The input data must contains a column or attribute that is the work state (this is implemented as keyword searching). If the input data did not have a work state related column, the function will return -1. The top 10 frequent work states will not include empty strings, although the total number of certified application do include entries with empty strings as work states. If the data has multiple work states, the function will only account for the 1st work states recorded. 

### Wrapper - top_10_jobs()
This is the big wrapper function that will output the top states and occupations for a single csv file. It callsthe read_csv(), get_occupations(), and get_states() functions. 

### Notes
The get_occupations() and get_states() functions are so similar that I can combine them both into one single function. However, since different data have different formats and different column titles, I write individual functions for getting the occupations and getting the states for easier error handling and debugging in the future. I am going to assume that there might be some data without a 'status' column or a 'workstate' column, or a 'soc-title' column. For example, I am currently assuming that there will only be one 'work state' related column in the data, and the name will always contain the keyword 'work' and 'state'. But if the data did not have any such column or the name of such column does not contain the keywords, there will be an error.

## Run instructions
`cd <name of directory>`



