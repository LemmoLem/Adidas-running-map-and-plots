"""
this script contains two functions
one adds pop ups with formatted string to each run so that when using the map
you can click on a run to find out all the info about the run
also code for making map without this
"""

import gpxpy
import ezgpx
import folium
from datetime import timedelta

def make_map_with_pop_up(df):
    gpx_file = open('adidas data/Sport-sessions/GPS-data/'+ df['GPS_heads'].iloc[-1], 'r')
    gpx = gpxpy.parse(gpx_file)
    val  =  gpx.tracks[0].segments[0].points[0]
    data = [val.latitude,val.longitude]
    gpx_file.close()
    m = folium.Map(data, zoom_start=4)
        
    for index, row in df.iterrows():
        formatted_date = row['run_dates'].strftime("%d/%m/%Y %H:%M:%S")
        # round it as seconds
        duration = timedelta(seconds = round(row['durations']*3600))
        
        info_parts = [
            f"Date: {formatted_date}",
            f"Sport: {row['sport_type']}<br>",
            f"Distance: {str(row['distances'])}(km) Duration: {str(duration)}<br>",
            f"Pace: {str(round(row['paces'], 3))}(mins/km) Speed: {str(row['speed'])}(km/h)<br>",
            f"Elevation gain: {str(row['elevation_gain'])}(m) Elevation loss: {str(row['elevation_loss'])}(m)<br>",
            f"Calories: {str(row['calories'])}(kcal) Dehydration: {str(row['dehydration'])}(ml)<br>",
            f"Temperature: {str(row['temp'])}(°C) Humidity: {str(row['rhum'])}(%)<br>",
            f"Weather: {row['coco']} Wind speed: {str(row['wspd'])}(km/h)<br>",
            f"Surface: {row['surface']} Feeling: {row['feeling']} Notes: {row['notes']}<br>",
            "Segments:"
        ]
        
        for segment in row['segments']:
            rounded_segment = timedelta(seconds=round(segment['duration'] / 1000))
            segment_info = f"<br>{segment['distance']} {str(rounded_segment)}"
            info_parts.append(segment_info)
        
        df.at[index, 'info'] = " ".join(info_parts)
    
    
    for index, row in df.iterrows():
        gpx = ezgpx.GPX('adidas data/Sport-sessions/GPS-data/'+ df.at[index,'GPS_heads'])
        gpx.simplify()
        route_info = gpx.to_dataframe()[['lat','lon']]    
        polyline = folium.PolyLine(
            locations=route_info,
            color="#FF0000",
            weight=0.9,
            popup= folium.Popup(df.at[index,'info'],max_width=1000)
        )
        polyline.add_to(m)

    map_path = "foliumMap.html"
    m.save(map_path)
    with open(map_path, 'a') as f:
        f.write('\n<script src="hover_effect.js"></script>\n')
        
def make_map_without_pop_up(df):
    gpx_file = open('adidas data/Sport-sessions/GPS-data/'+ df['GPS_heads'].iloc[-1], 'r')
    gpx = gpxpy.parse(gpx_file)
    val  =  gpx.tracks[0].segments[0].points[0]
    data = [val.latitude,val.longitude]
    gpx_file.close()
    m = folium.Map(data, zoom_start=4)
    for index, row in df.iterrows():
        gpx = ezgpx.GPX('adidas data/Sport-sessions/GPS-data/'+ df.at[index,'GPS_heads'])
        gpx.simplify()
        route_info = gpx.to_dataframe()[['lat','lon']]    
        polyline = folium.PolyLine(
            locations=route_info,
            color="#FF0000",
            weight=0.9,
        )
        polyline.add_to(m)       
        
    map_path = "foliumMap.html"
    m.save(map_path)    
    with open(map_path, 'a') as f:
        f.write('\n<script src="hover_effect.js"></script>\n')