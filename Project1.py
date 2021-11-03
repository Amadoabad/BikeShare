import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTH_DATA = {
    1:'Jan',
    2:'Feb',
    3:'Mar',
    4:'Apr',
    5:'May',
    6:'Jun'
}

DAY_DATA = {
    0:"Mon",
    1:"Tue",
    2:"Wed",
    3:"Thu",
    4:"Fri",
    5:"Sat",
    6:"Sun"
}

def get_key(dictionary ,value):
    """
    Get the key of the dictionary if you have the value
    """
    for key, value in dictionary.items():
        if dictionary.get(key)==value:
            return key

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Enter the city you'd like to analyze. from (chicago, new york city, washington)\n").lower().strip()
        if city in CITY_DATA.keys():
            city = CITY_DATA[city]
            break
        print("Enter a valid city please!")
   
    
    # get user input for month (None, 1, 2, ... , 6)
    while True:
        month = input("Enter the month you'd like to filter by. Like Jan for January OR None for no filtering\n").title().strip()
        if month in MONTH_DATA.values():
            month = get_key(MONTH_DATA,month)
            break
        elif month == 'None':
            month = None
            break
        print("Enter a valid month please!")
    
    
    # get user input for day of week (None, 0, 1, 2, ...)
    while True:
        day = input("Enter the day you'd like to filter by. like Mon for Monday OR None for no filtering\n").title().strip()
        if day in DAY_DATA.values():
            day = get_key(DAY_DATA,day)
            break
        elif day == 'None':
            day = None
            break
        print("Enter a valid day please!")
    
    print('-'*40)
    
    return city, month, day

def load_data(city, r_month, r_day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    print("-"*40)
    print("Wait while preparing the data for you ^^")
    print("-"*40)
    # Loading city data
    file = '../Data/'+city
    df = pd.read_csv(file)
    
    # getting a month column
    #df["Start Time"] = pd.to_datetime(df["Start Time"])
    df["Month"] = pd.DatetimeIndex(df["Start Time"]).month
    
    # getting a day column
    df["Day"] = pd.DatetimeIndex(df["Start Time"]).weekday
    
    # getting an hour column
    df["Hour"] = pd.DatetimeIndex(df["Start Time"]).hour    
    
    # Filtering by month
    global month_filter
    month_filter = False
    if r_month != None :
        df= df[df['Month'] == r_month]
        month_filter = True
        
    # Filtering by day
    global day_filter
    day_filter = False
    if r_day != None :
        df= df[df['Day'] == r_day]
        day_filter = True
    return df



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('-'*40)
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month_filter == False :
        most_common_month = df['Month'].mode()[0]
        common_month = MONTH_DATA.get(most_common_month)
        print(f"The most common month is: {common_month}")
    
    # display the most common day of week
    if day_filter == False:
        most_common_day = df['Day'].mode()[0]
        common_day = DAY_DATA.get(most_common_day)
        print(f"The most common day is: {common_day}")

    # display the most common start hour
    most_common_hour = df['Hour'].mode()[0]
    print(f"The most common hour is: {most_common_hour}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('-'*40)
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df["Start Station"].mode()[0]
    print(f"The most common start station is: {most_common_start_station}")
    
    # display most commonly used end station
    most_common_end_station = df["End Station"].mode()[0]
    print(f"The most common end station is: {most_common_end_station}")

    # display most frequent combination of start station and end station trip
    comb_series = df['Start Station']+' to '+df['End Station']
    most_frequent_combination = comb_series.mode()[0]
    print(f"The most frequent combination starts from {most_frequent_combination}")
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('-'*40)
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print(f"The total travel time is: {total_travel_time/3600:.2f} Hours!")

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print(f"The mean travel time is: {mean_travel_time/3600:.2f} Hours!")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
   
    print('-'*40)
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count_of_user_types = df["User Type"].value_counts().to_dict()
    for i,k in count_of_user_types.items():
        print(f"The user type {i} appeared {k} times!")
    
    
    # Display counts of gender
    if 'Gender' in df.columns :
        count_of_gender = df["Gender"].value_counts().to_dict()
        for i,k in count_of_gender.items():
            print(f"Gender {i} appeared {k} times!")
    else:
        print("This database doesn't have gender information.")
    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns :
        earliest = df['Birth Year'].min()
        recent = df['Birth Year'].max()
        common = df['Birth Year'].mode()[0]
        print(f"The earliest year of birth is {earliest}!\nWhile the most recent is {recent}.\nBut the most common is {common}")
    else:
        print("This database doesn't have age information.")
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def show_5_rows(df):
    df.drop(columns=['Month', 'Hour', 'Day'], inplace = True)
    print("-"*40)
    k=0
    n=5
    while True:
        show = input("Would you like me to show you 5 rows from the database? yes or no.\n").strip().lower()
        if show != "yes":
            break
        print(df[k:n])
        n +=5
        k +=5
    
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_5_rows(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

