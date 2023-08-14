import time
import pandas as pd
import numpy as np
import sys

# Ensure data files are saved within same folder or update to include file paths
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # List of valid cities, months, and days
    cities = ['chicago', 'new york city', 'washington']
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    # Get user input for city (chicago, new york city, washington) and validate input
    while True:
        city = input("Which city would you like to analyze? (chicago, new york city, washington): ").lower()
        if city in cities:
            break
        else:
            print("Invalid input. Please select a valid city.")

    # Get user input for month (all, january, february, ... , june) and validate input
    while True:
        month = input("Which month would you like to filter by? (all, january, february, ... , june): ").lower()
        if month in months:
            break
        else:
            print("Invalid input. Please select a valid month.")

    # Get user input for day of week (all, monday, tuesday, ... sunday) and validate input
    while True:
        day = input("Which day of the week would you like to filter by? (all, monday, tuesday, ... sunday): ").lower()
        if day in days:
            break
        else:
            print("Invalid input. Please select a valid day.")


    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
# Load the data for the specified city
    df =pd.read_csv(CITY_DATA[city])
    
    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # Extract month and day of the week from Start Time and create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()
    
    # Filter by month if applicable
    if month != 'all':
        # Use the index of the month to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]
    
    # Filter by day of the week if applicable
    if day != 'all':
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    common_month = df['month'].mode()[0]
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    print(f"The most common month of travel is: {months[common_month - 1].title()}")

    # Display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print(f"The most common day of the week for travel is: {common_day.title()}")

    # Display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print(f"The most common hour of the day for travel is: {common_hour}:00")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print(f"The most commonly used start station is: {common_start_station}")

    # Display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print(f"The most commonly used end station is: {common_end_station}")

    # Display most frequent combination of start station and end station trip
    df['Start End Combo'] = df['Start Station'] + " to " + df['End Station']
    common_start_end_combo = df['Start End Combo'].mode()[0]
    print(f"The most frequent combination of start and end station trip is: {common_start_end_combo}")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print(f"Total travel time is: {total_travel_time} seconds")

    # Display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print(f"Average travel time is: {mean_travel_time:.2f} seconds")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("Counts of user types:")
    print(user_types)
    
    # Check for the Gender column in the DataFrame before displaying counts of gender
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print("Counts of gender:")
        print(gender_counts)
       
    # Check for the Birth Year column in the DataFrame before displaying statistics on birth year
    if 'Birth Year' in df.columns:
        earliest_birth_year = df['Birth Year'].min()
        most_recent_birth_year = df['Birth Year'].max()
        most_common_birth_year = df['Birth Year'].mode()[0]
        print(f"Earliest year of birth: {int(earliest_birth_year)}")
        print(f"Most recent year of birth: {int(most_recent_birth_year)}")
        print(f"Most common year of birth: {int(most_common_birth_year)}")
        print()


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """Displays chunks of raw data based on user input."""
    
    start_idx = 0
    chunk_size = 5
    
    # Prompt the user if they want to see raw data
    see_data = input("\nWould you like to see the raw data? Enter yes or no.\n")
    
    while see_data.lower() == 'yes':
        # Display next chunk of raw data
        print(df.iloc[start_idx : start_idx + chunk_size])
        
        start_idx += chunk_size
        
        # Ask user if they want to continue seeing more data
        see_data = input("\nWould you like to see 5 more rows of the raw data? Enter yes or no.\n")
        
        # If the user has seen all the data, break out of the loop
        if start_idx >= len(df):
            print("\nYou've seen all the data!")
            break

import sys

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        while True:
            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() == 'yes':
                break
            elif restart.lower() == 'no':
                print("Exiting the program.")
                sys.exit()
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")

if __name__ == "__main__":
    main()

