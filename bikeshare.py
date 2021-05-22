import time
import pandas as pd
import numpy as np

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

    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ''
    while True:
        city = input('Please specify a city you would like data from: Chicago, New York City, or Washington: ').lower()
        if city in ('chicago', 'new york city', 'washington'):
            break
        else:
            print('Perhaps there is a typo. Please try again')

    # TO DO: get user input for month (all, january, february, ... , june)
    month = ''
    while True:
        month = input('Please enter month you\'d like to filter on between January to June, or select all: ').lower()
        if month in ('all','january','february','march','april','may','june'):
            break
        else:
            print('Perhaps there is a typo. Please try again')

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = ''
    while True:
        day = input('Please enter day you\'d like to filter on between Monday to Sunday, or select all: ').lower()
        if day in ('all','monday','tuesday','wednesday','thursday','friday','saturday','sunday'):
            break
        else:
            print('Perhaps there is a typo. Please try again')

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
    # read the appropriate csv file for city
    df = pd.read_csv(CITY_DATA[city])

    # convert to appropriate month and day format
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    common_month_int = df['month'].mode()[0]
    months_list = ['January', 'February', 'March', 'April', 'May', 'June']
    common_month = months_list[common_month_int-1]
    print('Most common month: {}'.format(common_month))

    # TO DO: display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('Most common day: {}'.format(common_day))

    # TO DO: display the most common start hour
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print('Most common hour: {}'.format(common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('Most common start station: {}'.format(common_start_station))

    # TO DO: display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('Most common end station: {}'.format(common_end_station))

    # TO DO: display most frequent combination of start station and end station trip
    df['Combination'] = df['Start Station'] + ' to ' + df['End Station']
    common_combination = df['Combination'].mode()[0]
    count_c = df[df['Combination'] == common_combination].count()[0]
    print('Most common combination of stations: {} (count: {})'.format(common_combination,count_c))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_time_sec = df['Trip Duration'].sum()
    total_time = pd.to_timedelta(total_time_sec, unit = 's')
    print('Total travel time is: {} seconds'.format(total_time))

    # TO DO: display mean travel time
    total_mean_sec = df['Trip Duration'].mean()
    total_mean = pd.to_timedelta(total_mean_sec, unit = 's')
    print('Mean travel time is: {} seconds'.format(total_mean))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_type = df['User Type'].value_counts()
    print('Types of users: \n{}'.format(user_type))

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        gender_count = df['Gender'].value_counts(dropna=False)
        print('Gender breakdown:\n{}'.format(gender_count))
    else:
        print('No gender data to display.')

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_birth = df['Birth Year'].min()
        most_recent_birth = df['Birth Year'].max()
        most_common_birth = df['Birth Year'].mode()[0]
        print('Earliest birth year is: {} \nMost recent birth year is: {} \nCommon birth year is: {}'.format(earliest_birth, most_recent_birth, most_common_birth))
    else:
        print('No birth year data to display.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # Display individual raw data 5 at a time
        # https://pandas.pydata.org/pandas-docs/stable/user_guide/options.html for display max columns
        raw_data = input('Would you like to see individual trip data? Yes or no: ')
        if raw_data.lower() == 'yes':
            row_total = len(df.index)
            print(row_total)
            i = 0
            while True:
                pd.set_option('display.max_columns', None)
                if i+5 > row_total:
                    diff = row_total - i
                    print(df.iloc[i:(i+diff),:])
                    break
                else:
                    print(df.iloc[i:(i+5),:])
                    i += 5
                raw_data = input('Continue? Yes or no: ')
                if raw_data.lower() != 'yes':
                    break

        # Restart option
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
