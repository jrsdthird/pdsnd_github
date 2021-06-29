import pandas as pd
import time
import numpy as np

# load the files
city_data = {
    'chicago':'chicago.csv',
    'new_york':'new_york_city.csv',
    'washington':'washington.csv'
}

# why don't you just _tell_ me the city you want to view?
def input_city():
    print('\nDo you want to explore bikeshare data? You got it. \n\nTell me what city: ')
    print('Chicago = 1 \nNew York City = 2 \nWashington DC = 3')
    city = input('Your choice: ')
    city = city.lower()

    # input error handling
    while True:
        if city == '1' or city == 'chicago':
            print("\nChicago, gotcha.")
            return 'chicago'
        if city == '2' or city == 'new york city':
            print("\nNYC, nice.")
            return 'new_york'
        elif city == '3' or city == 'washington dc':
            print("\nWashington, aye.")
            return 'washington'
        else:
            print('\nHmm. That doesn\'t look right. Let\'s try again. \nType the name of the city or 1, 2, 3: ')
            city = input('Your choice: ')
            city = city.lower()
    return city

# why don't you just _tell_ me the filters you want to use?
def input_time():
    print('\nTo filter the data by month, type \"month\". \nTo filter the data by day of the week, type \"day\". \nTo apply no filter, type, \"nada\". ')
    time_filter = input('\nYour choice: ')
    time_filter = time_filter.lower()

    while True:
        if time_filter == "month":
            print('\nMonths. Sounds good. Continuing.')
            return 'month'
        if time_filter == "day":
            print('\nDays. Sounds good. Continuing.')
            return 'day_of_week'
        elif time_filter == "nada":
            print('\nNo filters? No problem.')
            return 'no_filter'
        time_filter = input('\nThat doesn\'t look right. \nTo filter the data by month, type \"month\". \nTo filter the data by day of the week, type \"day\". \nTo apply no filter, type, \"nada\". ')

# which month do you want to review?
def input_month(m):
    if m == 'month':
        month = input('\nType which month you want (January through June only): \n').lower()
        while month.strip().lower() not in ['january', 'february', 'march', 'april', 'may', 'june']:
            month = input('\nType which month you want (January - June only): \n').lower()
        return month.strip().lower()
    else:
        return 'no_month_filter'

# why don't you just _tell_ me the day you want to review?
def day_info(d):
    if d == 'day_of_week':
        day = input('\nWhich day? \"Mon\", \"Tue\", \"Wed\", \"Thur\", \"Fri\", \"Sat\", \"Sun\": ')
        while day.lower().strip() not in ['mon', 'tue', 'wed', 'thur', 'fri', 'sat', 'sun']:
            day = input('\nWhich day? \"Mon\", \"Tue\", \"Wed\", \"Thur\", \"Fri\", \"Sat\", \"Sun\": ')
        return day.lower().strip()
    else:
        return 'none'

# grab the requested city's data
def load_data(city):
    df = pd.read_csv(city_data[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['month'] = df['Start Time'].dt.month
    df['day_of_month'] = df['Start Time'].dt.day
    return df

# apply the selected filters
def time_filters(df, time_filter, month, week_day):
    if time_filter == 'month':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]
    if time_filter == 'day_of_week':
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        for d in days:
            if week_day.capitalize() in d:
                day_of_week = d
        df = df[df['day_of_week'] == day_of_week]
    return df

'''
#1 Popular times of travel (i.e., occurs most often in the start time)
most common month
most common day of week
most common hour of day
'''
# calculate stats for #1
def month_freq(df):
    m = df.month.mode()[0]
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    popular_month = months[m - 1].capitalize()
    result = '\nThe most common month for travel is: ' + popular_month
    return result

def day_freq(df):
    calc = df['day_of_week'].value_counts().reset_index()['index'][0]
    result = '\nThe most common day of the week for travel is: ' + calc
    return result

def hour_freq(df):
    df['hour'] = df['Start Time'].dt.hour
    calc = str(df.hour.mode()[0])
    result = '\nThe most common hour of the week for travel is: ' + calc
    return result



'''
#2 Popular stations and trip
most common start station
most common end station
most common trip from start to end (i.e., most frequent combination of start station and end station)
'''
# calculate stats for #2
def popular_stations(df):
    start_station = df['Start Station'].value_counts(dropna=False).reset_index()['index'][0]
    end_station = df['End Station'].value_counts(dropna=False).reset_index()['index'][0]
    result = '\nThe most common starting station is: ' + start_station + '\nThe most common end station is: ' + end_station
    return result

def common_trip(df):
    calc = df[['Start Station', 'End Station']].groupby(['Start Station', 'End Station']).size().nlargest(1)
    #calc = str(df.head(1))
    result = '\nThe most common start-to-end trip is: \n' + str(calc)
    return result


'''
#3 Trip duration
total travel time
average travel time
'''
def trip_duration(df):
    # sum of seconds / seconds in a day
    total_time = int(np.sum(df['Trip Duration']) / 86400)
    # avg seconds per trip
    avg_time = int(np.mean(df['Trip Duration']))
    print('\nTotal travel time is ' + str(total_time) + ' day(s)')
    print('Average travel time is ' + str(avg_time) + ' second(s)')
    return ''

'''
#4 User info
counts of each user type
counts of each gender (only available for NYC and Chicago)
earliest, most recent, most common year of birth (only available for NYC and Chicago)
'''
def user_counts(df):
    try:
        result = df['User Type'].value_counts()
        return result
    except:
        print('\nNo data for the selected filter')

def gender_counts(df):
    try:
        result = df['Gender'].value_counts()
        return result
    except:
        print('\nNo data for the selected filter.')

def birth_data(df):
    try:
        earliest = np.min(df['Birth Year'])
        print('\nThe earliest birth year is: ' + str(int(earliest)))

        most_recent = np.max(df['Birth Year'])
        print('The most recent birth year is: ' + str(int(most_recent)))

        most_common = df['Birth Year'].mode()[0]
        print('The most common birth year is: ' + str(int(most_common)))

        return ''
    except:
        print('\nNo data for the selected filter.')

'''
Raw data is displayed upon request by the user in this manner: Script should prompt the user if they want to see 5 lines of raw data, display that data if the answer is 'yes', and continue these prompts and displays until the user says 'no'.
'''
def raw_data(df):
    row_index = 0
    prompt = input('\nDo you want to see 5 lines of raw data? \nType \"Yes\" or \"No\": ').lower()

    while True:
        if prompt == 'no':
            return
        if prompt == 'yes':
            print(df[row_index: row_index + 5])
            row_index = row_index + 5
        prompt = input('\nDo you want to see 5 lines of raw data? \nType \"Yes\" or \"No\": ').lower()


# calculating processing times
def process(f, df):
    start_time = time.time()
    stat_to_compute = f(df)
    print(stat_to_compute)
    print('This result took %s seconds to calculate.' % (time.time() - start_time))
    print('------')


# get the party started
def main():
    city = input_city()
    time_filter = input_time()
    month = input_month(time_filter)
    day = day_info(time_filter)
    df = load_data(city)
    df = time_filters(df, time_filter, month, day)
    raw_data(df)

    # calculate the outputs
    run_functions = [month_freq, day_freq, hour_freq, popular_stations, common_trip, trip_duration, user_counts, gender_counts, birth_data]
    for x in run_functions:
        process(x, df)

    # ask if user wants to go again
    start_over = input('\nDo you want to try again? Type \"Yes\" or \"No\": ').lower()
    if start_over != 'yes' and start_over != 'no':
        start_over = input('\nDo you want to try again? Type \"Yes\" or \"No\": ').lower()
    elif start_over == 'yes':
        main()
    else:
        print('\nThanks for riding!\n')


if __name__ == '__main__':
    main()
