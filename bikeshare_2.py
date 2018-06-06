import time
import pandas as pd
import numpy as np
CITY="'washington'"
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTH_LIST = ['january', 'february', 'march', 'april', 'may', 'june','all']
DOW_LIST = ['sunday','monday','tuesday','wednesday','thursday','friday','saturday','all']
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("="*80)
    print('Hello! Let\'s explore some US bikeshare data!')
    print("="*80)
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = input(" Enter the name of the city:(out of chicago/new york city/washington): ").lower()
            #Now it should accept both "ChicAgo" and "Chicago" input
            if not city:
                raise ValueError("empty string")
            if city in CITY_DATA.keys(): # matching with out CITY_DATA list for validation
                print("City name is matched :)")
                break
            else:
                print("Your entered city name not in list!!!.....please write again\n")
        except ValueError:
            print("City name is invalid")
        except KeyboardError:
            print("Keyboard Error")

    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = input("Enter the name of the month (only first 6 months in full words {ex. january/february/march/april/may/june/all}): ").lower()
            if not month:
                raise ValueError("empty string")
            if month in MONTH_LIST: # matching with our MONTH_LIST for validation
                print("Month name is matched :)")
                break
            else:
                print("Your entered month name not in list!!!.....please write again\n")
        except ValueError:
            print("month name is invalid")
        except KeyboardError:
            print("Keyboard Error")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = input("Enter the name of Day of the week (in full words{ex. sunday/monday/tuesday/wednesday/thursday/friday/saturday/all}): ").lower()
            if not day:
                raise ValueError("empty string")
            if day in DOW_LIST: # matching with out DOW_LIST list for validation
                print("Day name is matched :)")
                break
            else:
                print("Your entered day name is invalid!!!.....please write again\n")
        except ValueError:
            print("day is invalid")
        except KeyboardError:
            print("Keyboard Error")

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
    #load data to df dataframe
    df = pd.read_csv(CITY_DATA[city])
    #convert the Start Time column to datatime
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    #extract month and day of week,also create new columns
    df["month"] = df["Start Time"].dt.month
    df["day_of_week"] = df["Start Time"].dt.weekday_name

    #filter by month if applicable
    if month != "all":
        #use the index of the months list to get it's int ValueError
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1
        #filter by months to create the new DataFrame
        df=df[df["month"]==month]
    #filter by day of week if applicable
    if day != "all":
        #filter by day of week to create the new DataFrame
        df = df[df["day_of_week"]==day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print("="*80)
    print('\nCalculating The Most Frequent Times of Travel...\n')
    print("="*80)
    start_time = time.time()

    # display the most common month
    common_month = df["month"].mode()[0] # or df["month"].value_count().idxmax()
    print("\n")
    print("Popular month is: ",common_month)


    # display the most common day of week
    common_day_of_week = df["day_of_week"].mode()[0]
    print("\n")
    print("Popular Day of Week is: ",common_day_of_week)

    # display the most common start hour
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    df["hour"] =df["Start Time"].dt.hour
    common_hour = df["hour"].mode()[0]
    print("\n")
    print("Popular Start hour is: ",common_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print("="*80)
    print('\nCalculating The Most Popular Stations and Trip...\n')
    print("="*80)
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df["Start Station"].value_counts().idxmax()
    print("\n")
    print("most commonly used start station:: ",common_start_station)


    # display most commonly used end station
    common_end_station = df["End Station"].value_counts().idxmax()
    print("\n")
    print("most commonly used End station:: ",common_end_station)

    # display most frequent combination of start station and end station trip
    print("most frequebt trip:: \n",df[["Start Station","End Station"]].mode())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def time_conversion(sec):
    """ Converts seconds into -->  Days : Hour : Minutes : Seconds"""
    day = sec//(24*3600)
    sec = sec %(24*3600)
    hour = sec //3600
    sec%=3600
    minute = sec //60
    sec%=60
    seconds = sec
    return ("Days : Hour : Minutes : Seconds -> %d : %d : %d : %d"%(day,hour,minute,seconds))


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print("="*80)
    print('\nCalculating Trip Duration...\n')
    print("="*80)
    start_time = time.time()

    # display total travel time
    total_travel_time = df["Trip Duration"].sum()
    print("Total travel time is : ",time_conversion(total_travel_time)) # calling time_conversion() to convert the seconds into days:hour:min:sec

    # display mean travel time
    mean_travel_time = df["Trip Duration"].mean()
    print("Mean travel time is : ",time_conversion(mean_travel_time)) # calling time_conversion() to convert the seconds into days:hour:min:sec

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print("="*80)
    print('\nCalculating User Stats...\n')
    print("="*80)
    start_time = time.time()

    # Display counts of user types
    print("COUNT OF USER TYPE:\n")
    print(df["User Type"].value_counts())

    if CITY!="washington":
        # Display counts of gender
        print("COUNT OF GENDER:\n")
        """ here we could have NaN in various rows First we remove those rows"""
        df.dropna(axis=0)
        print(df["Gender"].value_counts())


        # Display earliest, most recent, and most common year of birth

        #calculation of earliest( i.e., minimum value)
        asc_order = df["Birth Year"].sort_values(ascending=True)#first sort (asc)
        print("earliest DOB is {}".format(int(asc_order.iloc[0])))# then choose first value

        #calculation of most recent(i.e., maximum value)
        desc_order = df["Birth Year"].sort_values(ascending=False)#first sort (desc)
        print("recent DOB is {}".format(int(desc_order.iloc[0])))# then choose first value

        #calculation of most common year of birth
        print("Most common year of birth is {}".format(int(df["Birth Year"].mode()[0])))

    else:
        print("There is no data related to Gender and Birth Year in this file beacuse of absence of gender and birth column ")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def correlation(x,y):
    """

    "correlation assuming x and y are independent"

    This function computes the correlation between the two input variable
    either a NumPy array or a pandas

    correlation = average of (x in standard units) times (y in standard units)
    """
    x_std = (x-x.mean())/x.std(ddof=0)
    y_std = (y-y.mean())/y.std(ddof=0)
    return (x_std*y_std).mean()


def find_correlation(df):
    """Displays statistics of correlation"""
    print("="*80)
    print('\nCalculating Correlation...\n')
    print("="*80)

    Trip_Duration = df["Trip Duration"]
    hour = df["hour"]
    print("correlation b/w Trip_Duration and hour is: ",correlation(Trip_Duration,hour))


def main():
    while True:
        city, month, day = get_filters()
        global CITY
        CITY=city
        #df=load_data("new york city", 'february', 'all')
        #print(df)
        df = load_data(city, month, day)
        print("-"*60)

        #showing some statixtical analysis
        print("Various statistical analysis:")
        print(df.head(4))
        print(df.columns)
        print(df.info())
        print(df.describe())
        print("-"*60)

        #appliyng various functions
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        find_correlation(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
