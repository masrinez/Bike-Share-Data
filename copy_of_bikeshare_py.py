# -*- coding: utf-8 -*-
"""Copy of bikeshare.py

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1r7LtqKUD7P5Q8JsgMJlbYXQzF2JDxiko

#**Bike Share Data**

Over the past decade, bicycle-sharing systems have been growing in number and popularity in cities across the world. Bicycle-sharing systems allow users to rent bicycles on a very short-term basis for a price. This allows people to borrow a bike from point A and return it at point B, though they can also return it to the same location if they'd like to just go for a ride. Regardless, each bike can serve several users per day.

Thanks to the rise in information technologies, it is easy for a user of the system to access a dock within the system to unlock or return bicycles. These technologies also provide a wealth of data that can be used to explore how these bike-sharing systems are used.

In this project, I used data provided by https://motivateco.com/, a bike share system provider for many major cities in the United States, to uncover bike share usage patterns. I compared the system usage between three large cities: Chicago, New York City, and Washington, DC.


**The Datasets**

Randomly selected data for the first six months of 2017 are provided for all three cities. All three of the data files contain the same core six (6) columns:

Start Time (e.g., 2017-01-01 00:07:57)
End Time (e.g., 2017-01-01 00:20:53)
Trip Duration (in seconds - e.g., 776)
Start Station (e.g., Broadway & Barry Ave)
End Station (e.g., Sedgwick St & North Ave)
User Type (Subscriber or Customer)
The Chicago and New York City files also have the following two columns:

Gender
Birth Year

In this project, I'll write codes to provide the following information:


**1 Popular times of travel (i.e., occurs most often in the start time)**

most common month
most common day of week
most common hour of day

**2 Popular stations and trip**

most common start station
most common end station
most common trip from start to end (i.e., most frequent combination of start station and end station)

**3 Trip duration**

total travel time
average travel time

**4 User info**

counts of each user type
counts of each gender (only available for NYC and Chicago)
earliest, most recent, most common year of birth (only available for NYC and Chicago)

** An Interactive Experience **

The bikeshare.py is set up as a script that takes in raw input to create an interactive experience in the terminal that answers questions about the dataset. The experience is interactive because depending on a user's input, the answers to the questions will change! There are four questions that will change the answers:

1) Would you like to see data for Chicago, New York, or Washington?

2) Would you like to filter the data by month, day, or not at all?

3) (If they chose month) Which month - January, February, March, April, May, or June?

4) (If they chose day) Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?

The answers to the questions above will determine the city and timeframe on which I'll perform my data analysis. After filtering the dataset, users will see the statistical result of the data, and choose to start again or exit.

My code would handle unexpected input well without failing. I will anticipate raw input errors like using improper upper or lower case, typos, or users misunderstanding what I am expecting.

My script also prompt the user whether they would like to see the raw data. If the user answers 'yes,' then the script would print 5 rows of the data at a time, then ask the user if they would like to see 5 more rows of the data. The script would continue prompting and printing the next 5 rows at a time until the user chooses 'no,' they do not want any more raw data to be displayed.


##**DATA ANALYSIS**

NB: The provided dataset won't be undergoing data wrangling as the clean version of the dtaset was downloaded for this project
"""

# Uploading the downloaded zip file from my local drive unto my workspace

from google.colab import files

local_file_path = "C:\\Users\\2227021\\Downloads\\all-project-files.zip"

uploaded = files.upload()

# Unzipping the file to work on

!unzip all-project-files.zip

# Importing necessary libraries

import time
import pandas as pd
import numpy as np

# Define data file paths and dictionary for city names

CITY_DATA = {
    'chicago' : 'chicago.csv',
    'new york' : 'new_york_city.csv',
    'washington' : 'washington.csv'
}

# Define months and days for filtering

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']

DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():

    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        str (city), str (month), str (day): City name, month, and day of the week for analysis
    """
    print("\nWelcome to the Bike Share Data Analysis tool!\n")

    # Get user input for city

    while True:

        city = input("Would you like to see data for Chicago, New York, or Washington? ").lower()

        if city in CITY_DATA:

            break

        else:

            print("Invalid input. Please choose a valid city.")

    # Get user input for time filter

    while True:

        time_filter = input("Would you like to filter the data by month, day, or not at all? ").lower()

        if time_filter in ['month', 'day', 'none']:

            break

        else:

            print("Invalid input. Please choose 'month', 'day', or 'none'.")

    month = 'all'

    day = 'all'

    if time_filter == 'month':

        while True:

            month = input("Which month - January, February, March, April, May, or June? ").lower()

            if month in MONTHS:

                break

            else:

                print("Invalid month. Please choose a valid month.")

    elif time_filter == 'day':

        while True:

            day = input("Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday? ").lower()

            if day in DAYS:

                break

            else:

                print("Invalid day of the week. Please choose a valid day.")

    print('-' * 40)

    return city, month, day

# Load data

def load_data(city, month, day):

    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of the week to filter by, or "all" to apply no day filter

    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """

# Load data file into a dataframe

    try:
        df = pd.read_csv(CITY_DATA[city])

    except FileNotFoundError:

        print("File not found. Please make sure the data file exists.")

        return None
# Convert the start time column to datetime

    df['Start Time'] = pd.to_datetime(df['Start Time'])

# extract month and day of week from start time to create new columns

    df['Month'] = df['Start Time'].dt.month

    df['Day of Week'] = df['Start Time'].dt.strftime('%A')

    df['Hour'] = df['Start Time'].dt.hour

# filter by month if applicable

    if month != 'all':

        # Use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']

        month_num = months.index(month) + 1

        # Filter by month to create the new dataframe

        df = df[df['Month'] == month_num]

    # filter by day of week if applicable

    if day != 'all':

        # filter by day of week to create the new dataframe

        df = df[df['Day of Week'] == day.title()]

    return df

# Time statistics

def time_stats(df):

    """
    Displays statistics on the most frequent times of travel.
    """
    print("\nCalculating the most frequent times of travel...\n")

    # Display the most common month

    common_month = df['Month'].mode()[0]

    print("Most common month:", MONTHS[common_month - 1].title())

    # Display the most common day of the week

    common_day = df['Day of Week'].mode()[0]

    print("Most common day of the week:", common_day)

    # Display the most common start hour

    common_hour = df['Hour'].mode()[0]

    print("Most common start hour:", common_hour)

# station statistics

def station_stats(df):

    """
    Displays statistics on the most popular stations and trips.
    """

    print("\nCalculating the most popular stations and trips...\n")

    # Display the most common start station

    common_start_station = df['Start Station'].mode()[0]

    print("Most common start station:", common_start_station)

    # Display the most common end station

    common_end_station = df['End Station'].mode()[0]

    print("Most common end station:", common_end_station)

    # Display the most common trip from start to end

    df['Trip'] = df['Start Station'] + ' to ' + df['End Station']

    common_trip = df['Trip'].mode()[0]

    print("Most common trip:", common_trip)

# Trip duration statistics

def trip_duration_stats(df):

    """
    Displays statistics on trip duration.
    """

    print("\nCalculating trip duration statistics...\n")

    # Display total travel time

    total_travel_time = df['Trip Duration'].sum()

    print("Total travel time (seconds):", total_travel_time)

    # Display average travel time

    average_travel_time = df['Trip Duration'].mean()

    print("Average travel time (seconds):", average_travel_time)

# User statistics

def user_stats(df, city):

    """
    Displays statistics on user types, gender, and birth year (if available).
    """

    print("\nCalculating user statistics...\n")

    # Display counts of each user type

    user_types = df['User Type'].value_counts()

    print("Counts of each user type:")

    for user_type, count in user_types.items():

        print(f"{user_type}: {count}")

    # Check if gender and birth year columns exist in the dataframe

    if 'Gender' in df.columns and 'Birth Year' in df.columns:

        # Display counts of each gender

        genders = df['Gender'].value_counts()

        print("\nCounts of each gender:")

        for gender, count in genders.items():

            print(f"{gender}: {count}")

        # Display earliest, most recent, and most common birth year

        earliest_birth_year = int(df['Birth Year'].min())

        most_recent_birth_year = int(df['Birth Year'].max())

        common_birth_year = int(df['Birth Year'].mode()[0])

        print("\nBirth year statistics:")

        print("Earliest birth year:", earliest_birth_year)

        print("Most recent birth year:", most_recent_birth_year)

        print("Most common birth year:", common_birth_year)

    else:

        print("\nGender and birth year data not available for", city.title())

# display raw data

def display_raw_data(df):

    """
    Displays 5 lines of raw data upon user request.
    """

    raw_data_display = input("Would you like to see 5 lines of raw data? Enter 'yes' or 'no': ").lower()

    if raw_data_display == 'yes':

        i = 0

        while i < len(df):

            print(df.iloc[i:i+5])

            i += 5

            raw_data_display = input("Would you like to see the next 5 lines of raw data? Enter 'yes' or 'no': ").lower()

            if raw_data_display != 'yes':

                break

# main function

def main():

    while True:

        city, month, day = get_filters()

        df = load_data(city, month, day)

        if df is not None:

            time_stats(df)

            station_stats(df)

            trip_duration_stats(df)

            user_stats(df, city)

            display_raw_data(df)

        restart = input("\nWould you like to restart? Enter 'yes' or 'no': ").lower()

        if restart != 'yes':

            print("Goodbye!")

            break

if __name__ == "__main__":

    main()

from google.colab
import files

uploaded = files.upload()
