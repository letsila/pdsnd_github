import time
import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    """

    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington).
    city = input(
        "Which city data do you like to display, Chicago, New York City or Washington? \n").lower()
    while (city != 'chicago' and city != 'new york city' and city != 'washington'):
        city = input(
            "Which city do you like to display, Chicago, New York City or Washington? \n").lower()

    # get user input for month (all, january, february, ... , j
    month = input(
        "Which month to display? January, February, March, April, May, June, or all?\n").lower()
    while (month != 'all' and month != 'january' and month != 'february' and month != 'march' and month != 'april' and month != 'may' and month != 'june'):
        month = input(
            'Which month to display? January, February, March, April, May, June, or all? \n').lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Which day of the week?(Monday, ... or all) \n').lower()
    while (day != 'all' and day != 'monday' and day != 'tuesday' and day != 'wednesday' and day != 'thursday' and day != 'friday' and day != 'saturday' and day != 'sunday'):
        day = input('Which day of the week?(Monday, ... or all)  \n').lower()

    print('-'*40)
    return city, month, day


def convert_to_datetime(dataframe, column):
    """
    Convert data in one column into datetime type

    """
    dataframe[column] = pd.to_datetime(dataframe[column])


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    """
    df = pd.read_csv(CITY_DATA[city])

    # convert the start time to date time
    convert_to_datetime(df, 'Start Time')

    # extract month, day of week and hour into their respective column
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        df = df[df['month'] == month]

    # filter by day of week
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    most_common_month = df['month'].mode()[0]
    print('Most common Month: ', most_common_month)

    # Display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print('\n Most common Day of week: ', most_common_day)

    # Display the most common start hour
    most_common_start_hour = df['hour'].mode()[0]
    print('\n Most common Start Hour: ', most_common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print('The most commonly used start station: ', most_common_start_station)

    # Display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print('\n The most commonly used end station: ', most_common_end_station)

    # Display most frequent combination of start station and end station trip
    most_common_combination = df.groupby(
        ['Start Station', 'End Station']).size().idxmax()
    print('\n The most frequent combination of start station and end station trip: ',
          most_common_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # convert the Start Time  and End column to datetime
    convert_to_datetime(df, 'Start Time')
    convert_to_datetime(df, 'End Time')

    # Create a column Travel Time
    df['Travel Time'] = df['End Time'] - df['Start Time']

    # Display total travel time
    sum_travel = df['Travel Time'].sum()
    print("The total travel time: ", sum_travel)

    # Display mean travel time
    mean_travel = df['Travel Time'].mean()
    print("\nThe mean travel time is: ", mean_travel)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("User types count: \n", user_types)

    # Display counts of gender for New York City and Chicago
    if city != 'washington':
        gender = df['Gender'].value_counts()
        print("\nThis is the count of each gender: \n", gender)

        # Display earliest, most recent, and most common year of birth
        popular_year = df['Birth Year'].mode()[0]
        print("\nThe most common year of birth is:", popular_year)
        print("\nThe earliest year of birth is:", df['Birth Year'].min())
        print("\nThe most recent year of birth is:", df['Birth Year'].max())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    """
    Display raw data upon request by the user

    """
    answer = input("Want to see raw data? (yes or no)\n").lower()
    if answer == 'yes':
        start_index = 0
        end_index = 6
        data = df.iloc[start_index:end_index]
        print(data)
        new_answer = input("Want to see more 5 lines of raw data?\n").lower()
        while new_answer != 'no':
            start_index += 5
            end_index += 5
            new_data = df.iloc[start_index:end_index]
            print(new_data)
            new_answer = input("Want to see more 5 lines of raw data?\n").lower()


def main():

    # infinite loop in order to make our cli app interactive 
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_data(df)

        restart = input('\nWould you like to restart? yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()

