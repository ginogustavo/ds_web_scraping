#Practice of operation between arrays
#Functions for extran hours and min from militar hours and utils method for
#diff between scheduled and actual departure of flights

import numpy as np
import pandas as pd

def string_explosion(string):
    if (len(string)>0):
        print(string, end ="")
        string = string[1:]
        string_explosion(string)
#string_explosion("hi")

def replace(a, b):
    a=a[:len(a)-1]
    for i in b:
        a.append(i)
    print(a)

def bowl_cost():
    B = np.array([
        [4,4,4],
        [1,0,3],
        [0,4,2],
        [0,0,12]
    ])
    A = np.array([
        [0, 3, 2, 0],
        [2, 2, 2, 2],
        [0, 0, 0, 10]
    ])
    x = [40,100,120]

    inv = np.linalg.inv(A @ B)
    return inv @ x

print(bowl_cost())

def bowl_cost2():
    v = np.array([11.25  ,  0.625 , -0.4375])
    B = np.array([
        [4,4,4],
        [1,0,3],
        [0,4,2],
        [0,0,12]
    ])
    A = np.array([
        [0, 3, 2, 0],
        [2, 2, 2, 2],
        [0, 0, 0, 10]
    ])
    return A @ B @ v
print(bowl_cost2())

def extract_hours(time):
    time = time.where(time<=2359.0)
    time = time.where(pd.isna(time),time//100)
    return time
def extract_mins(time):
    time = time.where(time<=2359.0)
    time = time.where(pd.isna(time),time%100)
    return time

#data = pd.Series([1270.0,np.nan, 245.0, 2400.0])
#print(extract_hours(data))
#print(extract_mins(data))

def convert_to_minofday(time):
    hours = extract_hours(time)
    mins = extract_mins(time)
    mins = mins + hours*60
    return mins

sched = pd.Series([1202, 1310, 0000, 110, 2053], dtype='float64')
actual = pd.Series([1203, 1315, 1259, 100, 0000], dtype='float64')

scheduled = convert_to_minofday(sched)
actual =  convert_to_minofday(actual)

print(actual-scheduled)
