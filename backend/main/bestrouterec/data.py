# Python 3 program to calculate Distance Between Two Points on Earth 
from math import radians, cos, sin, asin, sqrt
import pandas as pd
from geopy.geocoders.nominatim import Nominatim
from faker import Faker
import random
import time
from pathlib import Path
import csv
import math
from geopy.extra.rate_limiter import RateLimiter
from random import randint
import datetime

faker = Faker()
Address = []
Latitude = []
Longitude = []
Distance = []
departure_longitude = []
arrival_longitude = []
departure_latitude = []
arrival_latitude = []
departure_points = []
arrival_points = []
departure_timestamp = []
arrival_timestamp = []
price = []


def dataset_taxi_preprocessing():
    text = Path("./data_files/scrapped_data.csv").read_text(encoding="UTF-8")
    text = text.replace("\ufeff", '"')
    text = text.replace("id", 'id""')
    text = text.replace(',"\n"', '\n')
    text = text.replace('""', '"')
    out = Path("./data_files/data_taxi.csv").write_text("".join(text), encoding="UTF-8")

    df = pd.read_csv("./data_files/data_taxi.csv", error_bad_lines=False, warn_bad_lines=True, encoding="UTF-8",engine='python')
    locator = Nominatim(user_agent="myGeocoder")

    # 1 - conveneint function to delay between geocoding calls
    geocode = RateLimiter(locator.geocode, min_delay_seconds=1)
    # 2- - create location column
    df['location'] = df['Full_Address'].apply(geocode)
    # 3 - create longitude, laatitude and altitude from location column (returns tuple)
    df['point'] = df['location'].apply(lambda loc: tuple(loc.point) if loc else '')
    # 4 - split point column into latitude, longitude and altitude columns
    df[['latitude', 'longitude', 'altitude']] = pd.DataFrame(df['point'].tolist(), index=df.index)


    df = df.drop(['Website', 'Plus_Code', 'Rating', 'Reviews', 'URL' ], axis=1)

    df = df.dropna()

    for i in range (len(df)-1):
        for k in range (len(df)-1-i):
            departure_longitude.append(radians(Longitude[k]))
            departure_latitude.append(radians(Latitude[k]))
            departure_points.append(df['Name'][k])

        for j in range(i+1,len(df)):
            arrival_longitude.append(radians(Longitude[j]))
            arrival_latitude.append(radians(Latitude[j]))
            arrival_points.append(df['Name'][j])

        departure_lon = radians(departure_longitude[i])
        arrival_lon = radians(arrival_longitude[i])
        departure_lat = radians(departure_latitude[i])
        arrival_lat = radians(arrival_latitude[i])
            
        dlon = arrival_lon - departure_lon  
        dlat = arrival_lat - departure_lat 
        a = math.sin(dlat/2)**2 + math.cos(departure_lat)*math.cos(arrival_lat)*math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        # Radius of earth in kilometers. Use 3956 for miles 
        r = 6373
        d = c * r
        Distance.append(d)
        price.append(max(1.5 * (2 + (0.20/80) * float(Distance[i]) * 1000),7.5)) 
        # calculate the result 
        departure_time = datetime.datetime(year=randint(2019,2020),month=randint(1,12),day=randint(1,30),hour=randint(00,23),minute=randint(00,59))
        arrival_time = departure_timestamp + 2*datetime.datetime(minute=d)
        departure_timestamp.append(departure_time)
        arrival_timestamp.append(arrival_time)

    # intialise data of lists. 
    data = {'departure_point':departure_points, 'arrival_point':arrival_points, 'Distance': Distance, 'departure_timestamp':departure_timestamp, 'arrival_timestamp':arrival_timestamp, 'price':price} 
    
    # Create DataFrame 
    df = pd.DataFrame(data) 
    df['Mode_transport'] = ['Petit Taxi']*len(df)










