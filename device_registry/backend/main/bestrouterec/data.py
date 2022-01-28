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
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from bestrouterec.document import Trip
from bestrouterec.repository import Repository

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

#White Taxi, Bus and Tram data not available on aps

def taxi_dataset_tranform():

    text = Path("./data_files/scrapped_data.csv").read_text(encoding="UTF-8")
    text = text.replace("\ufeff", '"')
    text = text.replace("id", 'id""')
    text = text.replace(',"\n"', '\n')
    text = text.replace('""', '"')
    out = Path("./data_files/data_taxi.csv").write_text("".join(text), encoding="UTF-8")

    # df = pd.read_csv("./data_files/data_taxi.csv", error_bad_lines=False, warn_bad_lines=True, encoding="UTF-8",engine='python')
    # locator = Nominatim(user_agent="myGeocoder")

    # # 1 - conveneint function to delay between geocoding calls
    # geocode = RateLimiter(locator.geocode, min_delay_seconds=1)
    # # 2- - create location column
    # df['location'] = df['Full_Address'].apply(geocode)
    # # 3 - create longitude, laatitude and altitude from location column (returns tuple)
    # df['point'] = df['location'].apply(lambda loc: tuple(loc.point) if loc else '')
    # # 4 - split point column into latitude, longitude and altitude columns
    # df[['latitude', 'longitude', 'altitude']] = pd.DataFrame(df['point'].tolist(), index=df.index)


    # df = df.drop(['Website', 'Plus_Code', 'Rating', 'Reviews', 'URL' ], axis=1)

#TODO : optimize the running time of the code below
#TODO: refactor the code

def prepare_trips_dataset(files : List[str], mode_transports : List[str]):


    for file, mode in zip(files,mode_transports):

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

        Trips=[]

        for i in range(len(df)):
            dlon = arrival_lon[i] - departure_lon[i] 
            dlat = arrival_lat[i] - departure_lat[i] 
            a = math.sin(dlat/2)**2 + math.cos(departure_lat[i])*math.cos(arrival_lat[i])*math.sin(dlon/2)**2
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            r = 6373
            d = c * r

            if mode=='petit_taxi':
                df = df.drop(['Website', 'Plus_Code', 'Rating', 'Reviews', 'URL' ], axis=1)
                df['Mode_transport'] = [mode]*len(df)
                price=max(1.5 * (2 + (0.20/80) * float(d) * 1000),7.5) 
                departure_time = datetime.datetime(year=randint(2019,2020),month=randint(1,12),day=randint(1,30),hour=randint(00,23),minute=randint(00,59))
                arrival_time = departure_timestamp + 2*datetime.datetime(minute=d)
            if mode=='ctm':
                df.drop(['location_from','location_to','point_from','point_to','altitude_from','altitude_to', 'Unnamed: 0'], axis=1)
                df['Mode_transport'] = [mode]*len(df)
                df['price']=df['price'].apply(lambda x: x[:-2].replace(',','.'))
                departure_time = datetime.datetime(year=randint(2019,2020),month=randint(1,12),day=randint(1,30),hour=randint(00,23),minute=randint(00,59))
                arrival_time = departure_timestamp + datetime.datetime(hour=d/80)
            if mode=='oncf':
                df.drop(['location_from','location_to','point_from','point_to','altitude_from','altitude_to', 'Unnamed: 0'], axis=1)
                df['Mode_transport'] = [mode]*len(df)
                df['price']=df['price'].apply(lambda x: x[:-2].replace(',','.'))
                departure_time = datetime.datetime(year=randint(2019,2020),month=randint(1,12),day=randint(1,30),hour=randint(00,23),minute=randint(00,59))
                arrival_time = departure_timestamp + datetime.datetime(hour=d/100) 
            if mode=='cov':
                df.drop(['location_from','location_to','point_from','point_to','altitude_from','altitude_to', 'Unnamed: 0'], axis=1)
                df['Mode_transport'] = [mode]*len(df)
                df['price']=df['price'].apply(lambda x: x[:-2].replace(',','.'))
                departure_time = datetime.datetime(year=randint(2019,2020),month=randint(1,12),day=randint(1,30),hour=randint(00,23),minute=randint(00,59))
                arrival_time = departure_timestamp + datetime.datetime(hour=d/90)  
            departure_point=list(df['from'])[i]
            arrival_point=list(df['to'])[i]               

            trip=Trip(distance=d,departure_point=departure_point,arrival_point=arrival_point,departure_timestamp=departure_time,arrival_timestamp=arrival_time)
            Trips.append(trip)
        
        Repository.add_many(objs=Trips)




#generate

# def prepare_dataset(files):

#     for file_name in files:
#         df = pd.read_csv(file_name)
    
#         distance=list(df['distance'])

#         for i in range(len(df)):

#             departure_time = datetime.datetime(year=randint(2019,2020),month=randint(1,12),day=randint(1,30),hour=randint(00,23),minute=randint(00,59))
#             arrival_time = departure_timestamp + 2*datetime.datetime(minute=distance[i])
#             departure_timestamp.append(departure_time)
#             arrival_timestamp.append(arrival_time)

#         # intialise data of lists. 
#         data = {'departure_point':departure_points, 'arrival_point':arrival_points, 'Distance': Distance, 'departure_timestamp':departure_timestamp, 'arrival_timestamp':arrival_timestamp, 'price':price} 
    
#         # Create DataFrame 
#         df = pd.DataFrame(data) 
#         df['Mode_transport'] = ['Petit Taxi']*len(df)
#         dataframe = pd.concat[df]

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
    df2 = pd.DataFrame(scores)
    df['sentiment'] = list(df2['compound'].apply(nnp))
    return df


