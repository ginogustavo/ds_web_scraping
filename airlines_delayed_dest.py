## delayed_destinations from airlpors iformation
import numpy as np
import pandas as pd

flights = pd.read_csv("flights.dat", dtype={'sched_dep_time': 'f8', 'sched_arr_time': 'f8'})
# show the first few rows, by default 5
flights.head()
airports_cols = [
    'openflights_id',
    'name',
    'city',
    'country',
    'iata',
    'icao',
    'latitude',
    'longitude',
    'altitude',
    'tz',
    'dst',
    'tz_olson',
    'type',
    'airport_dsource'
]

airports = pd.read_csv("airports.dat", names=airports_cols)
airports.head(3)

def extract_hours(time):
    time = time.where(time<=2359.0)
    time = time.where(pd.isna(time),time//100)
    return time

def extract_mins(time):
    time = time.where(time<=2359.0)
    time = time.where(pd.isna(time),time%100)
    return time

def convert_to_minofday(time):
    hours = extract_hours(time)
    mins = extract_mins(time)
    mins = mins + hours*60
    return mins

def calc_time_diff(x, y):
    scheduled = convert_to_minofday(x)
    actual =  convert_to_minofday(y)
    return actual-scheduled

delay = calc_time_diff(flights['sched_dep_time'],flights['actual_dep_time'])
delayed15 = flights.loc[delay>=15]


delayed_airports = delayed15[(delayed15['origin']=='SFO') | (delayed15['origin']=='OAK')]
delayed_airports = pd.merge(delayed_airports, airports, left_on='destination', right_on='iata')

delayed_destinations = delayed_airports.drop_duplicates(subset='name', keep='first')
delayed_destinations = delayed_destinations.sort_values("name", axis = 0, ascending = True)

print(delayed_destinations["name"])
