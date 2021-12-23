import time
import pandas as pd
import numpy as np


def get_filters():
    '''Receives input filters values from users and returns said filters in the appropriate variables.'''

    # use input_match function to get the required city, month, and day filters
    city = input_match('\nPlease enter the city for which you would like to see the Bikeshare data...', cities)
    month = input_match('If required, please enter a month filter for the data (January - June) or type \'all\' for no filter...', months)
    day = input_match('If required, please enter a day filter for the data (Monday - Sunday) or type \'all\' for no filter...', days)
    print('-'*40)
    return city, month, day
    
    
def load_data(city, month, day):
    '''Based on filter arguements, load/return Bikeshare data into a dataframe.'''

    # load data file with corresponding city into a dataframe
    df = pd.read_csv(city_data[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    # use the index of the months list to get the corresponding int when applicable
    if month != 'All':
        # use of plus 1 will adjust index of months to int equivalent (ie. moving 0 to 1)
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[(df['month'] == month)]
    # use the index of the day of week to get the corresponding int when applicable
    if day != 'All':
        day = days.index(day)
        # filter by day of week to create the new dataframe
        df = df[(df['day_of_week'] == day)]
    return df


def time_stats(df):
    '''Displays statistics on the most frequent times of travel.'''

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # create column for hour with info. taken from start time
    df['hour'] = df['Start Time'].dt.hour
    # display the most common month
    popular_month = df['month'].mode()[0]
    print('The most frequent month for travel is:', months[popular_month - 1].title())
    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('The most frequent day for travel is:', days[popular_day].title())
    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    popular_hour = str(popular_hour)
    # adjusting display format of adding a '0' infront of all times with only 1 digit - add a leading '0'
    if len(popular_hour) == 1:
        popular_hour = '0' + popular_hour
    print('The most frequent hour for travel is: {}:00'.format(popular_hour))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    start_time = time.time()
    # create new column for station pairings (from where they began their trip and where it ended)
    df['station pairings'] = df['Start Station']+'  >>>>>  '+df['End Station']
    print('\nCalculating The Most Popular Stations and Trip...\n')
    # displays the most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('The most commonly used start station is:', popular_start_station.title())
    # displays the most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('The most commonly used end station is:', popular_end_station.title())
    # displays the most frequent combination of start station and end station trip
    popular_station_pairings = df['station pairings'].mode()[0]
    print('The most popular start and end station pairing is:', popular_station_pairings.title())
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    # transforming duration to datetime object
    df['Trip Duration'] = pd.to_datetime(df['Trip Duration']*1000000000)-pd.to_datetime(0)
    # displays the total travel time
    total_trv_time = df['Trip Duration'].sum().round('s')
    print('The total trip duration (of all users combined) is:', total_trv_time)
    # displays the mean travel time
    avg_trv_time = df['Trip Duration'].mean().round('s')
    print('The average trip duration per user is:', avg_trv_time)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics for Bikeshare users."""
       
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    # Display counts of different user types
    user_types = df['User Type'].value_counts()
    print('The following is a breakdown of users by type: \n')
    print(user_types)
    # Display counts of gender - first checking whether column exits (may not always)
    if 'Gender' in df:
        user_genders = df['Gender'].value_counts()
        print('\nThe following is a breakdown of the users by gender: \n')
        print(user_genders)
    else:
        print('\nNo rider information by gender is available.')
    # Display earliest, most recent, and most common year of birth f:- first checking whether column exits (may not always)
    if 'Birth Year' in df:
        user_max_age = df['Birth Year'].max()
        user_min_age = df['Birth Year'].min()
        user_mode_age = df['Birth Year'].mode()[0]
        print('\nThe following are some statistics for the year from when the riders were born: \n')
        print('The earliest year born is:', int(user_min_age))
        print('The most recent year born is:', int(user_max_age))
        print('The most common year born is:', int(user_mode_age))
    else:
        print('\nNo rider information about the year when riders were born is available.')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def print_raw(city):
    """Prints out the raw (orignal) data for the requested city file - 5 rows at a time."""

    df = pd.read_csv(city_data[city])
    for i in range(0, len(df), 5):
        print('\n')
        print(df.iloc[i:i+5])
        end_output = input('\nPlease press \'enter\' to advance to the next 5 lines of output or type \'exit\' to leave the raw data display: ')
        if end_output.lower() == 'exit':
            #print('\nYou have ended the raw data display.')
            break

def input_match(question, list):
    """Requests user input and checks it against a list - if in the list returns the imput."""
    
    while True:
        x = input(question+'\n'+'('+', '.join(list)+'): ').title()
        if x in list:
            return x
        print('There appears to be a problem with the input. Please try again.')


def main():
    while True:
        city, month, day = get_filters()
        # setting up display variables for whether filters are being applied of not for the city selected
        if month == 'all':
            month_f = 'None'
        else:
            month_f = month
        if day == 'all':
            day_f = 'None'
        else:
            day_f = day
        print('\nShowing results for: {}\nMonth filter: {}\nDay filter: {}\n{}'.format(city.title(), month_f.title(), day_f.title(), '-'*40))
        try:
            df = load_data(city, month, day)
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
        except Exception as e:
            # setting up error messages and the frame appearance of the error message
            err = ''
            frame = '*'*71
            mini_frame = '*'*16
            print('\n\n\n     An error has occurred......\n     <Error {} has occured>\n\n\n'.format(e))
            print('{}\nSorry, there appears to be a problem with loading the data.\nIt may be that not all the required columns are in the data file,\nor it may be that the file requested is coroupt.\nPlease contact your system administrator for assistance.  Thank you.\n{}\n{}   THE APPLICATION WILL SHUTDOWN NOW   {}\n{}'.format(frame, frame, mini_frame, mini_frame, frame))
        else:
            raw = input('Would you like to see the raw data from which the above statistics were derived?\nType \'yes\' to see the raw data or just hit enter to end the application: ')
            if raw.lower() == 'yes':
                print_raw(city)
        print('\nYou have reached the end of the application.\n')
        restart = input('Would you like to restart the Rideshare statistics application? Enter \'yes\' to continue or hit enter to exit: ')
        if restart.lower() != 'yes':
            print('\nYou have chosen to exit the system.  Thank you for using the Rideshare information app.')
            break

city_data = { 'Chicago': 'chicago.csv',
              'New York': 'new_york_city.csv',
              'Washington': 'washington.csv' }
cities = ['Chicago', 'New York', 'Washington']
months = ['January', 'February', 'March', 'April', 'May', 'June', 'All']
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'All']
if __name__ == "__main__":
	main()
