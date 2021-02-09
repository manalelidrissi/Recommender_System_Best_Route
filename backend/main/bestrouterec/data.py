# Python 3 program to calculate Distance Between Two Points on Earth 
from math import radians, cos, sin, asin, sqrt
import pandas as pd
from geopy.geocoders.nominatim import Nominatim
from faker import Faker
import random
import re
import time
from pathlib import Path
import csv
import math
from geopy.extra.rate_limiter import RateLimiter
from random import randint
import datetime
import pandas as pd
import random
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from bestrouterec.document import Trip, Event
from bestrouterec.repository import Repository
from surprise import Dataset, Reader
import os
import logging

faker = Faker()
sia = SentimentIntensityAnalyzer()

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
Price = []
Trips=[]

logger = logging.getLogger(os.path.basename(__file__))

#White Taxi, Bus and Tram data not available on aps

def taxi_dataset_tranform():

    text = Path("./data_files/scrapped_data.csv").read_text(encoding="UTF-8")
    text = text.replace("\ufeff", '"')
    text = text.replace("id", 'id""')
    text = text.replace(',"\n"', '\n')
    text = text.replace('""', '"')
    out = Path("./data_files/data_taxi.csv").write_text("".join(text), encoding="UTF-8")


#TODO : optimize the running time of the code below
#TODO: refactor the code

distance = []
departure_datetime = []
arrival_datetime = []

logger = logging.getLogger(os.path.basename(__file__))

def prepare_trips_dataset(file : str , mode_transport: str):



    df=pd.read_csv(file)
    address_to_coordinates(df)
    df=df.dropna()
    
    df['departure_lon']=df['longitude_f'].apply(lambda x: radians(x))
    df['arrival_lon']=df['longitude_t'].apply(lambda x: radians(x))
    df['departure_lat']=df['latitude_f'].apply(lambda x: radians(x))
    df['arrival_lat']=df['latitude_t'].apply(lambda x: radians(x))

    departure_lon=list(df['departure_lon'])
    departure_lat=list(df['departure_lat'])
    arrival_lon=list(df['arrival_lon'])
    arrival_lat=list(df['arrival_lat'])


    for i in range(len(df)):
        dlon = arrival_lon[i] - departure_lon[i] 
        dlat = arrival_lat[i] - departure_lat[i] 
        a = math.sin(dlat/2)**2 + math.cos(departure_lat[i])*math.cos(arrival_lat[i])*math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        r = 6373
        d = c * r
        distance.append(d)

        if mode_transport=='petit_taxi':
            df = df.drop(['Website', 'Plus_Code', 'Rating', 'Reviews', 'URL' ], axis=1)
            df['price']=[max(1.5 * (2 + (0.20/80) * float(d) * 1000),7.5)]*len(df) 
            departure_time = datetime.datetime(year=randint(2019,2020),month=randint(1,12),day=randint(1,30),hour=randint(00,23),minute=randint(00,59))
            arrival_time = departure_timestamp + 2*datetime.datetime(minute=d)
        elif mode_transport=='ctm':
            df.drop(['location_from','location_to','point_from','point_to','altitude_from','altitude_to', 'Unnamed: 0'], axis=1)
            df['price']=df['price'].apply(lambda x: x[:-2].replace(',','.'))
            departure_time = datetime.datetime(year=randint(2019,2020),month=randint(1,12),day=randint(1,30),hour=randint(00,23),minute=randint(00,59))
            arrival_time = departure_timestamp + datetime.datetime(hour=d/80)
        elif mode_transport=='oncf':
            df.drop(['location_from','location_to','point_from','point_to','altitude_from','altitude_to', 'Unnamed: 0'], axis=1)
            df['price']=df['price'].apply(lambda x: x[:-2].replace(',','.'))
            departure_time = datetime.datetime(year=randint(2019,2020),month=randint(1,12),day=randint(1,30),hour=randint(00,23),minute=randint(00,59))
            arrival_time = departure_timestamp + datetime.datetime(hour=d/100) 
        elif mode_transport=='cov':
            df.drop(['location_from','location_to','point_from','point_to','altitude_from','altitude_to', 'Unnamed: 0'], axis=1)
            df['price']=df['price'].apply(lambda x: x[:-2].replace(',','.'))
            departure_time = datetime.datetime(year=randint(2019,2020),month=randint(1,12),day=randint(1,30),hour=randint(00,23),minute=randint(00,59))
            arrival_time = departure_timestamp + datetime.datetime(hour=d/90)

        departure_datetime.append(departure_time)
        arrival_datetime.append(arrival_time)  

    data = {'distance' : distance, 'departure_point' : list(df['from']),'arrival_point' : list(df['to']),'departure_timestamp' : departure_datetime, 'arrival_timestamp' : arrival_datetime, 'mode_transport' : [mode_transport]*len(df)}
    df = pd.DataFrame(data)
    
    df.to_csv(f"data_files/{mode_transport}.csv")


prepare_trips_dataset(files=[], mode_transports =[])

def address_to_coordinates(df):

    locator = Nominatim(user_agent="myGeocoder")

    # 1 - conveneint function to delay between geocoding calls
    geocode = RateLimiter(locator.geocode, min_delay_seconds=1)
    # 2- - create location column
    df['location'] = df['Full_Address'].apply(geocode)
    # 3 - create longitude, laatitude and altitude from location column (returns tuple)
    df['point'] = df['location'].apply(lambda loc: tuple(loc.point) if loc else '')
    # 4 - split point column into latitude, longitude and altitude columns
    df[['latitude', 'longitude', 'altitude']] = pd.DataFrame(df['point'].tolist(), index=df.index)

#Code to analyse sentiment of the user
def clean_comment(comment):
    user_handles = re.findall(r'@[A-Za-z0-9]+', comment) #search @mentions
    hashtags = re.findall(r'#[A-Za-z0-9]+', comment) #search #hashtags
    links = re.findall(r' http?:\/\/\S+', comment) #search the hyperlink
    
    cleaned_comment = re.sub(r'@[A-Za-z0-9]+','', comment) #remove @mentions
    cleaned_comment = re.sub(r'#[A-Za-z0-9]+', '', cleaned_comment) #remove #hashtags
    cleaned_comment = re.sub(r' http?:\/\/\S+', '', cleaned_comment) #remove the hyperlink
        
    return cleaned_comment.strip(), user_handles, hashtags, links

#df is a dataframe that initially contains original comments
def clean_all_comments(df):
    df['cleaned_tweet'] = df['original_tweet'].apply(lambda x: clean_comment(x)[0])
    return df

def nnp(score):
    if score >= -1 and score < -0.2:
        return "negative"
    elif score >= -0.2 and score <= 0.2:
        return "neutral"
    elif score > 0.2 and score <= 1.0:
        return "positive"

def calculate_sentiment(df):
    scores = []
    for sentence in df['cleaned_tweet']:
        score = sia.polarity_scores(sentence)
        scores.append(score)
    df = pd.DataFrame(scores)
    df['sentiment'] = list(df['compound'].apply(nnp))
    return df

def final_dataset():
    df_taxi = prepare_trips_dataset(file='data_files/taxi_trips.csv', mode_transport='petit_taxi')
    df_oncf = prepare_trips_dataset(file='data_files/oncf_trips.csv', mode_transport='oncf')
    df_ctm = prepare_trips_dataset(file='data_files/ctm_trips.csv', mode_transport='ctm')
    df_cov = prepare_trips_dataset(file='data_files/cov_trips.csv', mode_transport='cov')
    df = pd.concat([df_taxi,df_oncf,df_ctm,df_cov])
    df['trip_id'] = range(len(df))
    df = df.reindex_axis(['trip_id', 'distance','departure_point', 'arrival_point','departure_timestamp', 'arrival_timestamp', 'transport'], axis=1)
    df.to_csv('data_files/trips.csv')


import numpy as np
users_ids=[]

def dataset_Event(passengers_count : int):
    df = pd.read_csv('data_files/trips.csv')
    Trafic = []
    df['Flow'] = np.random.randint(10,50)/df['Distance']
    for index,row in df.iterrows():
        if row['Flow']> df['Flow'].mean():
            Trafic.append(1)
        else:
            Trafic.append(0)
    df['Trafic'] = Trafic
    accident = []
    for index,row in df.iterrows():
        if row['Trafic'] == 1:
            accident.append(1)
        elif row['Trafic'] == 0 and row['Distance'] >= df['Distance'].mean():
            accident.append(1)
        else:
            accident.append(0)
    df['Accident'] = accident
    security = []
    for index,row in df.iterrows():
        if row['Trafic'] == 1 and row['time'] >= datetime(hour=6,minute=0,second=0) and row['time'] < datetime(hour=21,minute=0,second=0):
            security.append(2)
        elif row['Trafic'] == 0 and row['time'] >= datetime(hour=6,minute=0,second=0) and row['time'] < datetime(hour=21,minute=0,second=0):
            security.append(1)
        elif row['Trafic'] == 1 and row['time'] < datetime(hour=6,minute=0,second=0) and row['time'] >= datetime(hour=21,minute=0,second=0):
            security.append(1)
        else:
            security.append(0)

    df['Security'] = security
    df['route_rating'] = 2*(1 - df['Accident']) + df['Security'] + df['Trafic']
    df_ctm['route_rating'] = 3.1
    df_oncf['route_rating'] = 3.7

    df['rating_mood'] = np.random.choice(range(1,6))
    df['rating'] = (df['route_rating'] + df['rating_mood']) /2

    ratings = list(df['rating'])
    users_id=range(passengers_count)
    trips_id = list(df['trips_ids'])

    data = {"user_id" : users_id, "trip_id" : trips_id, "rating" : ratings} 

    df=pd.DataFrame(data)
    
    return df

def training_dataset(passengers_count : int):

    data = dataset_Event(passengers_count)
    data = Dataset.load_from_df(data, Reader(rating_scale=(1, 5)))
    data = data.build_full_trainset()

    return data

#convert csv to sqlalchemy database
trips=list()
events=list()

def csv_to_db():

    logger.info("convert the trips csv to a sqlalchemy database")

    df = pd.read_csv('data_files/trips.csv')
    trips_list = df.values.tolist()
    for elt in trips_list:
        trip = Trip(trip_id=elt[0], distance=elt[1], departure_point=elt[2], arrival_point=elt[3], departure_timestamp=elt[4], arrival_timestamp=elt[5], transport=elt[6])
        trips.append(trip)

    Repository.add_many(trips)

    logger.info("convert the events csv to a sqlalchemy database")

    df = pd.read_csv('data_files/events.csv') 
    events_list = df.values.tolist()
    for elt in events_list:
        event = Event(trip_id=elt[0], distance=elt[1], departure_point=elt[2], arrival_point=elt[3], departure_timestamp=elt[4], arrival_timestamp=elt[5], transport=elt[6])
        events.append(event)

    Repository.add_many(events)


csv_to_db()