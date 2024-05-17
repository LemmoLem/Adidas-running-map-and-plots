"""
this script goes thru all the adidas running data and pairs it with the gps data
and then produces a dataframe with all the relevant data from the adidas files
the gps data is used in this script for getting weather data
meteostat is used as the weather data stored in adidas running was missing alot of values
"""


import os
import json
from datetime import datetime, timedelta
import pandas as pd
from meteostat import Point, Hourly
import gpxpy

directory_gps = 'adidas data/Sport-sessions/GPS-data/'
directory_json = 'adidas data/Sport-sessions/'
def create_df_with_weather():
    df = create_df_without_weather()
    # get historical weather data
    # use time plus first coordinate point
    # loop thru gps heads in this df
    # add column for weather, humidity, etc, all the stats that can be useful
    for index, row in df.iterrows():
        f = open(directory_gps+ row['GPS_heads'],'r')
        gpx = gpxpy.parse(f)
        val = gpx.tracks[0].segments[0].points[0]
        # to get data weather of start of run add an hour to the time as need a range to make a point with meteostar
        data = Hourly(Point(val.latitude,val.longitude), df.at[index, 'run_dates'], df.at[index, 'run_dates']+ timedelta(hours=1)).fetch()
        if not data.empty:
            for col in data.columns:
                df.at[index, col] = data[col].values[0]
        f.close()
    
    for col in df.columns:
        print(col, df.at[0,col])
    
    coco_labels = {
        1: 'Clear',
        2:	'Fair',
        3:	'Cloudy',
        4:	'Overcast',
        5:	'Fog',
        6:	'Freezing Fog',
        7:	'Light Rain',
        8:	'Rain',
        9:	'Heavy Rain',
        10:	'Freezing Rain',
        11: 'Heavy Freezing Rain',
        12:	'Sleet',
        13:	'Heavy Sleet',
        14:	'Light Snowfall',
        15:	'Snowfall',
        16:	'Heavy Snowfall',
        17:	'Rain Shower',
        18:	'Heavy Rain Shower',
        19:	'Sleet Shower',
        20:	'Heavy Sleet Shower',
        21:	'Snow Shower',
        22:	'Heavy Snow Shower',
        23:	'Lightning',
        24:	'Hail',
        25:	'Thunderstorm',
        26:	'Heavy Thunderstorm',
        27:	'Storm'
    }

    df['coco'] = df['coco'].map(coco_labels)

    
    return df


def create_df_without_weather():

    
    # saves file heads for which there is both session file and gps file
    gps_heads = []
    adidas_heads = []
    for filename in os.listdir(directory_json):
        if filename.endswith(".json"):
            my_file, ending = os.path.splitext(filename)
            file_with_path = directory_gps + my_file + '.gpx'
            if os.path.isfile(file_with_path):
                adidas_heads.append(filename)
                gps_heads.append(my_file+'.gpx')
    
    # main dataframe 
    df = pd.DataFrame({'Adidas_heads': adidas_heads, 'GPS_heads': gps_heads})
    
    def get_sport_type_by_id(sport_id):
        for sport in sport_types:
            if sport[0] == sport_id:
                return sport[1]
        return "Sport not found"
    
    sport_types = [
      [1, 'Running'],
      [62, 'Speed Skiing'],
      [2, 'Nordic Walking'],
      [63, 'PushUps'],
      [3, 'Cycling'],
      [64, 'SitUps'],
      [4, 'Mountain Biking'],
      [65, 'PullUps'],
      [5, 'Other'],
      [66, 'Squats'],
      [6, 'Inline Skating'],
      [7, 'Hiking'],
      [68, 'Baseball'],
      [8, 'Cross-country skiing'],
      [69, 'Crossfit'],
      [9, 'Skiing'],
      [70, 'Dancing'],
      [10, 'Snowboarding'],
      [71, 'Ice Hockey'],
      [11, 'Motorbike'],
      [72, 'Skateboarding'],
      [13, 'Snowshoeing'],
      [73, 'Zumba'],
      [14, 'Treadmill'],
      [74, 'Gymnastics'],
      [15, 'Ergometer'],
      [75, 'Rugby'],
      [16, 'Elliptical'],
      [76, 'Standup Paddling'],
      [17, 'Rowing'],
      [77, 'Sixpack'],
      [18, 'Swimming'],
      [78, 'Butt Training'],
      [19, 'Walking'],
      [80, 'Leg Training'],
      [20, 'Riding'],
      [81, 'Results Workout'],
      [21, 'Golfing'],
      [82, 'Trail Running'],
      [22, 'Race Cycling'],
      [84, 'Plogging'],
      [23, 'Tennis'],
      [85, 'Wheelchair'],
      [24, 'Badminton'],
      [86, 'E Biking'],
      [25, 'Squash'],
      [87, 'Scootering'],
      [26, 'Yoga'],
      [88, 'Rowing Machine'],
      [27, 'Aerobics'],
      [89, 'Stair Climbing'],
      [28, 'Martial Arts'],
      [90, 'Jumping Rope'],
      [29, 'Sailing'],
      [91, 'Trampoline'],
      [30, 'Windsurfing'],
      [92, 'Bodyweight Training'],
      [31, 'Pilates'],
      [93, 'Tabata'],
      [32, 'Rock Climbing'],
      [94, 'Callisthenics'],
      [33, 'Frisbee'],
      [95, 'Suspension Training'],
      [34, 'Strength Training'],
      [96, 'Powerlifting'],
      [35, 'Volleyball'],
      [97, 'Olympic Weightlifting'],
      [36, 'Handbike'],
      [98, 'Stretching'],
      [37, 'Cross Skating'],
      [99, 'Mediation'],
      [38, 'Soccer'],
      [100, 'Bouldering'],
      [42, 'Surfing'],
      [101, 'Via Ferrata'],
      [43, 'Kitesurfing'],
      [102, 'Pade'],
      [44, 'Kayaking'],
      [103, 'Pole Dancing'],
      [45, 'Basketball'],
      [104, 'Boxing'],
      [46, 'Spinning'],
      [105, 'Cricket']
    ]
    df['segments'] = None
    
    for index, row in df.iterrows():
        f = open(directory_json + row['Adidas_heads'],'r')
        data = json.load(f)
        metrics = data['features']
        date = str(row['Adidas_heads'])[:19]
        dateObj = datetime.strptime(date, '%Y-%m-%d_%H-%M-%S')
        df.at[index, 'run_dates'] = dateObj 
        for x in metrics:
            if x['type'] == 'track_metrics':
                # unit conversions - m/s to km/m 
                speed = float(x['attributes']['average_speed'])*3.6
                df.at[index, 'speed'] = round(speed,3)
                df.at[index, 'paces'] = float(x['attributes']['average_pace']) * 1000 / 60
                df.at[index, 'distances'] = float(x['attributes']['distance']) / 1000
                df.at[index,'elevation_gain'] = x['attributes']['elevation_gain']
                df.at[index, 'elevation_loss'] = x['attributes']['elevation_loss']
                if 'surface' in x['attributes']:
                    df.at[index,'surface'] = x['attributes']['surface']
            if x['type'] == 'fastest_segments':
                df.at[index, 'segments'] = x['attributes']['segments']
        # duration is in millisseconds
        df.at[index, 'durations'] = float(data['duration']) / 3600000
        df.at[index,'calories'] = data['calories']
        df.at[index,'sport_id'] = int(data['sport_type_id'])
        sport_id = int(data['sport_type_id'])
        df.at[index,'sport_type'] = get_sport_type_by_id(sport_id)
        df.at[index,'dehydration'] = data['dehydration_volume']
        if 'notes' in data:
            df.at[index,'notes'] = data['notes']
        if 'subjective_feeling' in data:
            df.at[index,'feeling'] = data['subjective_feeling']
        f.close()
      
    df['run_dates'] = pd.to_datetime(df['run_dates'])
    return df