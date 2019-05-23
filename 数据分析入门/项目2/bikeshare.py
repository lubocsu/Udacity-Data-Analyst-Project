import time
import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply
                      no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no
                   day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington).
    # HINT: Use a while loop to handle invalid inputs
    city = ''
    month = ''
    day = ''
    filter_opt = ''
    while True:
        try:
            input_city = input(
                "\nWould you like to see data for Chicago, New york city or "
                "Washington?\n").lower()
            if input_city in ['chicago', 'new york city', 'washington']:
                city = input_city
                break
        except KeyboardInterrupt:
            print('\nNo input taken\n')
        finally:
            print('\nAttempted Input\n')
    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        try:
            input_filter = input(
                '\nWould you like to filter the data by month ,day,'
                'both or not at all？Type \'none\' for no time filter.\n').lower()
            if input_filter == 'none':
                day = 'all'
                month = 'all'
                filter_opt = 'none'
                break
            elif input_filter == 'both':
                filter_opt = 'both'
                while True:
                    try:
                        input_month = input(
                            '\nWhich month? January, February, March, April, '
                            'May or June?\n').lower()
                        if input_month in ['january', 'february', 'march',
                                           'april', 'may', 'june']:
                            month = input_month
                            while True:
                                try:
                                    input_day = input(
                                        '\nWhich day? Monday, Tuesday, Wednesday,'
                                        ' Thursday, Friday, Saturday or Sunday?\n').lower()
                                    if input_day in ['monday', 'tuesday',
                                                     'wednesday', 'thursday',
                                                     'friday', 'saturday',
                                                     'sunday']:
                                        day = input_day
                                        break
                                except KeyboardInterrupt:
                                    print('\nNo input taken\n')
                                finally:
                                    print('\nAttempted Input\n')
                            break
                    except KeyboardInterrupt:
                        print('\nNo input taken\n')
                    finally:
                        print('\nAttempted Input\n')
                break
            elif input_filter == 'month':
                filter_opt = 'month'
                while True:
                    try:
                        input_month = input(
                            '\nWhich month? January, February, March, April, '
                            'May or June?\n').lower()
                        if input_month in ['january', 'february', 'march',
                                           'april', 'may', 'june']:
                            month = input_month
                            day = 'all'
                            break
                    except KeyboardInterrupt:
                        print('\nNo input taken\n')
                    finally:
                        print('\nAttempted Input\n')
                break
            elif input_filter == 'day':
                filter_opt = 'day'
# TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
                while True:
                    try:
                        input_day = input(
                            '\nWhich day? Monday, Tuesday, Wednesday, Thursday,'
                            'Friday, Saturday or Sunday?\n').lower()
                        if input_day in ['monday', 'tuesday', 'wednesday',
                                         'thursday', 'friday', 'saturday',
                                         'sunday']:
                            day = input_day
                            month = 'all'
                            break
                    except KeyboardInterrupt:
                        print('\nNo input taken\n')
                    finally:
                        print('\nAttempted Input\n')
                break
        except KeyboardInterrupt:
            print('\nNo input taken\n')
        finally:
            print('\nAttempted Input\n')

    print('-' * 40)
    return city, month, day, filter_opt


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day
    if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply
                     no month filter
        (str) day - name of the day of week to filter by, or "all" to apply
                    no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.DataFrame(pd.read_csv(CITY_DATA[city]))
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['Month'] = df['Start Time'].dt.month
    df['Day_of_week'] = df['Start Time'].dt.weekday_name
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['Month'] == month]
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['Day_of_week'] == day.title()]
    return df


def time_stats(df, filter_opt):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    df_month = df[['Month', 'Start Time']].groupby('Month')[
        'Start Time'].size().reset_index(name='Count')\
        .sort_values(['Count'], ascending=False)
    common_month_list = df_month[df_month['Count'] == df_month['Count'].max()][['Month', 'Count']].values.tolist()
    if common_month_list:
        for item in common_month_list:
            print('\nMost common month : {}, Count : {}, Filter: {}.'
                  .format(item[0], item[1], filter_opt))
    else:
        print('\nNo Most common month data to share.')
    # TO DO: display the most common day of week
    df_day = df[['Day_of_week', 'Start Time']].groupby('Day_of_week')[
        'Start Time'].size().reset_index(name='Count')\
        .sort_values(['Count'], ascending=False)
    common_day_list = df_day[df_day['Count'] == df_day['Count'].max()][['Day_of_week', 'Count']].values.tolist()
    if common_day_list:
        for item in common_day_list:
            print('\nMost common day : {}, Count : {}, Filter: {}.'
                  .format(item[0], item[1], filter_opt))
    else:
        print('\nNo Most common day data to share.')

    # TO DO: display the most common start hour
    df['Start Hour'] = df['Start Time'].dt.hour
    df_hour = df[['Start Hour', 'Start Time']].groupby('Start Hour')[
        'Start Time'].size().reset_index(name='Count')\
        .sort_values(['Count'], ascending=False)
    common_hour_list = df_hour[df_hour['Count'] == df_hour['Count'].max()][['Start Hour', 'Count']].values.tolist()
    if common_hour_list:
        for item in common_hour_list:
            print('\nMost common hour : {}, Count : {}, Filter: {}.'
                  .format(item[0], item[1], filter_opt))
    else:
        print('\nNo Most common hour data to share.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df, filter_opt):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    df_start = df[['Start Station', 'Start Time']].groupby('Start Station')[
        'Start Time'].size().reset_index(name='Count')\
        .sort_values(['Count'], ascending=False)
    common_start_list = df_start[df_start['Count'] == df_start['Count'].max()][['Start Station', 'Count']].values.tolist()
    if common_start_list:
        for item in common_start_list:
            print('\nMost commonly used start station '
                  ': {}, Count : {}, Filter: {}.'
                  .format(item[0], item[1], filter_opt))
    else:
        print('\nNO Most commonly used start station data to share.')

    # TO DO: display most commonly used end station
    df_end = df[['End Station', 'Start Time']].groupby('End Station')[
        'Start Time'].size().reset_index(name='Count')\
        .sort_values(['Count'], ascending=False)
    common_end_list = df_end[df_end['Count'] == df_end['Count'].max()][['End Station', 'Count']].values.tolist()
    if common_end_list:
        for item in common_end_list:
            print('\nMost commonly used end station '
                  ': {}, Count : {}, Filter: {}.'
                  .format(item[0], item[1], filter_opt))
    else:
        print('\nNO Most commonly used end station data to share.')

    # TO DO: display most frequent combination of start station
    # and end station trip
    df_start_end = df[['Start Station', 'End Station', 'Start Time']].groupby(
        ['Start Station', 'End Station'])['Start Time'].size().sort_values(
        ascending=False).reset_index(name='Count')
    start_end_list = df_start_end[df_start_end['Count'] ==
                                  df_start_end['Count'].max()][['Start Station', 'End Station', 'Count']].values.tolist()
    if start_end_list:
        for item in start_end_list:
            print('\nMost frequent combination of start station and end station :')
            print('\nStart Station :{}, End Station :{}, Count : {}, '
                  'Filter: {}.'
                  .format(item[0], item[1], item[2], filter_opt))
    else:
        print('\nNO Most frequent start and end station data to share.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df, filter_opt):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    df = df.fillna(0)
    total_duration = df['Trip Duration'].sum()
    count = df.shape[0]
    print('\nTotal duration : {} ,Count : {} , Filter : {} .'
          .format(total_duration, count, filter_opt))
    # TO DO: display mean travel time
    average_duration = df['Trip Duration'].mean()
    print('\nAvg duration : {} ,Count : {} , Filter : {} .'
          .format(average_duration, count, filter_opt))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df, filter_opt):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types

    df_user_counts = df[['User Type', 'Start Time']].groupby('User Type')['Start Time'].size().reset_index(name='Count').sort_values(['Count'], ascending=False)
    user_counts_list = df_user_counts.values.tolist()
    if user_counts_list:
        for item in user_counts_list:
            print('\nUser Type :{}, Count :{}, Filter : {} .'
                  .format(item[0], item[1], filter_opt))
    else:
        print('\nNO user type counts data to share.')

    # TO DO: Display counts of gender
    if 'Gender' in df:
        df_gender_counts= df[['Gender', 'Start Time']].groupby('Gender')[
            'Start Time'].size().reset_index(name='Count').sort_values(['Count'], ascending=False)
        gender_counts_list = df_gender_counts.values.tolist()
        if gender_counts_list:
            for item in gender_counts_list:
                print('\nGender Type :{}, Count :{}, Filter : {} .'
                      .format(item[0], item[1], filter_opt))
        else:
            print('\nNO user gender counts data to share.')
    else:
        print('\nNO user gender counts data to share.')

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        if False in df['Birth Year'].isnull().values.tolist():
            earliest_year = df['Birth Year'].min()
            recent_year = df['Birth Year'].max()
            common_year = df['Birth Year'].mode().iloc[0]
            print('\nEarliest birth year : {} , Most recent birth year : {} , '
                  'Most common birth year : {} .'
                  .format(earliest_year, recent_year, common_year))
        else:
            print('\nNo birth year data to share .')
    else:
        print('\nNo birth year data to share .')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def main():
    while True:
        city, month, day, filter_opt = get_filters()
        df = load_data(city, month, day)

        time_stats(df, filter_opt)
        station_stats(df, filter_opt)
        trip_duration_stats(df, filter_opt)
        user_stats(df, filter_opt)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
