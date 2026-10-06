import sys

"""
Create a program which will provide answers to the questions posed in the assignment description.
We've provided a function which will parse the NYT covid database file (named "us-counties.csv"); 
however, its correct implementation will be up to you. DO NOT MODIFY THIS FUNCTION.
Your code needs to be successful as well as sufficiently commented/documented to receive full credit.
"""


def parse_nyt_data(file_path=''):
    """
    Parse the NYT covid database and return a list of tuples. Each tuple describes one entry in the source data set.
    Date: the day on which the record was taken in YYYY-MM-DD format
    County: the county name within the State
    State: the US state for the entry
    Cases: the cumulative number of COVID-19 cases reported in that locality
    Deaths: the cumulative number of COVID-19 death in the locality

    :param file_path: Path to data file
    :return: A List of tuples containing (date,county, state, fips, cases, deaths) information

    ____________________ DO NOT MODIFY THIS FUNCTION ___________________
    """
    # data point list
    data=[]

    # open the NYT file path
    try:
        fin = open(file_path)
    except FileNotFoundError:
        print('File ', file_path, ' not found. Exiting!')
        sys.exit(-1)

    # get rid of the headers
    fin.readline()

    # while not done parsing file
    done = False

    # loop and read file
    while not done:
        line = fin.readline()

        if line == '':
            done = True
            continue

        # format is date,county,state,fips,cases,deaths
        (date,county, state, fips, cases, deaths) = line.rstrip().split(",")

        # clean up the data to remove empty entries
        if cases=='':
            cases=0
        if deaths=='':
            deaths=0

        # convert elements into ints
        try:
            entry = (date,county,state, fips, int(cases), int(deaths))
        except ValueError:
            print('Invalid parse of ', entry)

        # place entries as tuple into list
        data.append(entry)


    return data

### YOUR CODE HERE ###
# Obtain the COVID-19 data from the NYT dataset
covid_data = parse_nyt_data('data/covid/us-counties.csv')

#----------------Question 1----------------------
# Find first positive COVID-19 case in Harrisonburg
first_case_harrisonburg = None
for entry in covid_data:
    # Unpack values stored in each tuple
    date, county, state, fips, cases, deaths = entry
    # Check if this entry corresponds to Harrisonburg city in Virginia with positive cases
    if county == 'Harrisonburg city' and state == 'Virginia' and cases > 0:
        first_case_harrisonburg = date
        break

print('First positive COVID-19 case in Harrisonburg:', first_case_harrisonburg)

# Find first positive COVID-19 case in Rockingham County
first_case_rockingham = None
for entry in covid_data:
    date, county, state, fips, cases, deaths = entry
    # Stop searching once the first positive case is found
    if county == 'Rockingham' and state == 'Virginia' and cases > 0:
        first_case_rockingham = date
        break

print('First positive COVID-19 case in Rockingham County:', first_case_rockingham)

#----------------Question 2----------------------
#Find date of Greatest number of new COVID-19 cases in Harrisonburg
greatest_new_cases_harrisonburg = 0
previous_cases_harrisonburg = 0
date_of_greatest_new_cases_harrisonburg = None
for entry in covid_data:
    date, county, state, fips, cases, deaths = entry
    if county == 'Harrisonburg city' and state == 'Virginia':
        # Calculate new cases for this entry
        new_cases = cases - previous_cases_harrisonburg
        # Update the greatest number of new cases if this entry has more than the current maximum
        if new_cases > greatest_new_cases_harrisonburg:
            greatest_new_cases_harrisonburg = new_cases
            date_of_greatest_new_cases_harrisonburg = date
            # Store today's cases as the previous cases for the next iteration
        previous_cases_harrisonburg = cases

print('Date of greatest number of new COVID-19 cases in Harrisonburg:', date_of_greatest_new_cases_harrisonburg)

#Find date of Greatest number of new COVID-19 cases in Rockingham County
greatest_new_cases_rockingham = 0
previous_cases_rockingham = 0
date_of_greatest_new_cases_rockingham = None
for entry in covid_data:
    date, county, state, fips, cases, deaths = entry
    if county == 'Rockingham' and state == 'Virginia':
        # Calculate new cases for this entry
        new_cases = cases - previous_cases_rockingham
        # Update the greatest number of new cases if this entry has more than the current maximum
        if new_cases > greatest_new_cases_rockingham:
            greatest_new_cases_rockingham = new_cases
            date_of_greatest_new_cases_rockingham = date

        previous_cases_rockingham = cases

print('Date of greatest number of new COVID-19 cases in Rockingham County:', date_of_greatest_new_cases_rockingham)

#----------------Question 3----------------------
#Find worst seven-day period of new COVID-19 cases in Harrisonburg
worst_seven_day_cases_harrisonburg = 0
previous_cases_harrisonburg = 0
#Variables store the start and end dates of the worst seven-day period
start_date_of_worst_seven_day_cases_harrisonburg = None
end_date_of_worst_seven_day_cases_harrisonburg = None
# List to store the new cases for the current seven-day period
seven_day_cases_harrisonburg = []
for entry in covid_data:
    date, county, state, fips, cases, deaths = entry
    if county == 'Harrisonburg city' and state == 'Virginia':
        # Calculate new cases for this entry
        new_cases = cases - previous_cases_harrisonburg
        # Add the new cases for this date to the seven-day list
        seven_day_cases_harrisonburg.append((date, new_cases))
        # Remove the oldest entry if the list exceeds seven days
        if len(seven_day_cases_harrisonburg) > 7:
            seven_day_cases_harrisonburg.pop(0)

        # Check if we have a full seven-day period to evaluate
        if len(seven_day_cases_harrisonburg) == 7:
            # Add the daily new cases for the current seven-day period
            total_seven_day_cases = sum(c for d, c in seven_day_cases_harrisonburg)
            # Update the worst seven-day period if the current total is greater than the previous worst
            if total_seven_day_cases > worst_seven_day_cases_harrisonburg:
                worst_seven_day_cases_harrisonburg = total_seven_day_cases
                start_date_of_worst_seven_day_cases_harrisonburg = seven_day_cases_harrisonburg[0][0]
                end_date_of_worst_seven_day_cases_harrisonburg = seven_day_cases_harrisonburg[-1][0]
        # Save today's cases as the previous cases for the next iteration
        previous_cases_harrisonburg = cases

print('Worst seven-day period of new COVID-19 cases in Harrisonburg starts on:', 
    start_date_of_worst_seven_day_cases_harrisonburg,
    'to',
    end_date_of_worst_seven_day_cases_harrisonburg)


#Find worst seven-day period of new COVID-19 cases in Rockingham County
worst_seven_day_cases_rockingham = 0
previous_cases_rockingham = 0
start_date_of_worst_seven_day_cases_rockingham = None
end_date_of_worst_seven_day_cases_rockingham = None
#Store the most recent seven days of new cases for Rockingham County
seven_day_cases_rockingham = []
for entry in covid_data:
    date, county, state, fips, cases, deaths = entry
    if county == 'Rockingham' and state == 'Virginia':
        # Calculate new cases for this entry
        new_cases = cases - previous_cases_rockingham
        # Add the new cases for this date to the seven-day list
        seven_day_cases_rockingham.append((date, new_cases))
        # Remove the oldest entry if the list exceeds seven days
        if len(seven_day_cases_rockingham) > 7:
            seven_day_cases_rockingham.pop(0)

        # Check if we have a full seven-day period to evaluate
        if len(seven_day_cases_rockingham) == 7:
            # Add the daily new cases for the current seven-day period
            total_seven_day_cases = sum(c for d, c in seven_day_cases_rockingham)
            # Update the worst seven-day period if the current total is greater than the previous worst
            if total_seven_day_cases > worst_seven_day_cases_rockingham:
                worst_seven_day_cases_rockingham = total_seven_day_cases
                start_date_of_worst_seven_day_cases_rockingham = seven_day_cases_rockingham[0][0]
                end_date_of_worst_seven_day_cases_rockingham = seven_day_cases_rockingham[-1][0]
        previous_cases_rockingham = cases

print('Worst seven-day period of new COVID-19 cases in Rockingham County starts on:', 
    start_date_of_worst_seven_day_cases_rockingham,
    'to',
    end_date_of_worst_seven_day_cases_rockingham)
