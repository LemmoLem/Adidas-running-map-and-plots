"""
this script has various functions for different plots
these aim to try analyse progress that have made with running 
and to try find any interesting things with the data
like impact of weather
"""


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as dates
from datetime import datetime, timedelta
import pandas as pd


def make_plots(df):
    scatter_plot_distance_paces_date(df)
    scatter_plot_paces_date(df)
    scatter_plot_distance_date(df)
    cum_distance(df)
    boxplots_distance_pace_weather(df)
    pace_temperature(df)
    distance_month(df)
    scatter_distance_pace(df)
    heatmap_hour_day(df)
    boxplot_pace_year(df)
    histo_paces_distance(df)
    cum_elevation_gain_loss(df)
    cum_time(df)
    day_pie(df)
    best_seg_times(df)
    yearly_cum_distance(df)
    
def scatter_plot_distance_paces_date(df):
    # scatter plot pace against distance with date along bottom
    fig, ax1 = plt.subplots(figsize=(15,10))
    ax2 = ax1.twinx()
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Distances (km)')
    ax2.set_ylabel('Paces (m/km)')
    ax1.scatter(df['run_dates'], df['distances'], color='red', label="Distance")
    ax2.scatter(df['run_dates'], df['paces'], color='blue', label="Pace")
    title = 'Paces and distances'
    plt.title(title)
    scatter, labels = ax1.get_legend_handles_labels()
    scatter2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(scatter + scatter2, labels + labels2)
    plt.tight_layout()
    plt.savefig(title+'.png')
    plt.show()
    
    
def scatter_plot_paces_date(df):    
    # scatter paces and plot trend line
    plt.figure(figsize=(15,10))
    plt.scatter(df['run_dates'], df['paces'])
    title = "Paces"
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Pace (m/km)")
    dateNum = dates.date2num(df['run_dates'])
    trend = np.polyfit(dateNum, df['paces'].astype('float'), 1)
    fit = np.poly1d(trend)
    plt.plot(dateNum, fit(dateNum), color='red')
    plt.tight_layout()
    plt.savefig(title+'.png')
    plt.show()
    
def scatter_plot_distance_date(df):    
    # scatter distances and plot trend line
    plt.figure(figsize=(15,10))
    plt.scatter(df['run_dates'], df['distances'])
    title = "Distances"
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Distance (km)")
    dateNum = dates.date2num(df['run_dates'])
    trend = np.polyfit(dateNum, df['distances'].astype('float'), 1)
    fit = np.poly1d(trend)
    plt.plot(dateNum, fit(dateNum), color='red')
    plt.tight_layout()
    plt.savefig(title+'.png')
    plt.show()
    
def cum_distance(df):
    # cumaltive distance - drawstyle is set to post
    cum_distance = np.cumsum(df['distances'])
    plt.figure(figsize=(15,10))
    plt.plot(df['run_dates'], cum_distance, drawstyle='steps-post')
    title = "Cumulative distance"
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Distance (km)")
    plt.tight_layout()
    plt.savefig(title+'.png')
    plt.show()
    
        
    
    # cumulative distance plot per year
    # method used is a bit of a work around
    # years are counted and new dates are made with same year
    # this allows plotting of each year to overlap
    
def yearly_cum_distance(df):    
    year_counts = {}
    new_dates = []
    for x in df['run_dates']:
        new_dates.append(datetime(2020,x.month,x.day))
        if x.year not in year_counts:
            year_counts[x.year] = 0
        year_counts[x.year] += 1
    
    fig = plt.figure(figsize=(15,10))    
    ax = fig.add_subplot(111)
    title = "Cumulative distances"
    plt.title(title)
    prev = 0
    for x in year_counts:
        # a dummy run is added to the start of the year 
        # and to the end of the year if its not the current year
        # this means the line plotted accounts for whole year
        n_dates = [datetime(2020,1,1)]
        n_dates.extend(new_dates[prev:prev+year_counts[x]])
        n_distance = [0]
        n_distance.extend(df['distances'][prev:prev+year_counts[x]]) 
        if x != datetime.now().year:
            n_distance.append(0)
            n_dates.append(datetime(2020,12,31))
        plt.plot(n_dates,np.cumsum(n_distance), label=str(x)+": "+str(year_counts[x])+" runs", drawstyle='steps-post')
        prev += year_counts[x]
    plt.xlabel("Date")
    plt.ylabel("Distance (km)")
    ax.xaxis.set_major_formatter(dates.DateFormatter('%b')) 
    ax.set_xticks([datetime(2020, month, 1) for month in range(1, 13)])
    plt.legend()
    plt.tight_layout()
    plt.savefig(title+'.png')
    plt.show()
    
def best_seg_times(df):    
    # plot for best segment times per year
    year_counts = {}
    new_dates = []
    for x in df['run_dates']:
        new_dates.append(datetime(2020,x.month,x.day))
        if x.year not in year_counts:
            year_counts[x.year] = 0
        year_counts[x.year] += 1
    
    
    fig = plt.figure(figsize=(15,10))    
    ax = fig.add_subplot(111)
    title = "Best segment times"
    plt.title(title)
    color_map = {'1km': 'red', '5km': 'blue', '10km': 'green', 'half_marathon': 'orange', 'marathon': 'purple', '1mi':'pink','3mi':'gray'}
    prev = 0
    zero = datetime(2020,1,1)
    fastest = {}
    for year in year_counts:   
        fastest_segments = {}
        fastest[year] = {}
        for index in range(prev, prev + year_counts[year]):
            for segment in df['segments'][index]:
                distance = segment['distance']
                duration = segment['duration']
                run_date = df.at[index, 'run_dates']                
                if distance not in fastest_segments:
                    fastest_segments[distance] = duration
                    fastest[year][distance] = [run_date,duration]
                elif fastest_segments[distance] > duration:
                    fastest_segments[distance] = duration
                    fastest[year][distance] = [run_date,duration]
        for distance, duration in fastest_segments.items():
            duration_timedelta = timedelta(0,duration/1000)
            time = zero + duration_timedelta
            zero_num = dates.date2num(zero)
            time = dates.date2num(time)-zero_num 
            
            plt.scatter(datetime(year,1,1), time, color=color_map.get(distance, 'black'), label=distance)
        prev += year_counts[year]
    ax.yaxis_date()
    ax.yaxis.set_major_formatter(dates.DateFormatter('%H:%M')) 
    ax.xaxis_date()
    ax.xaxis.set_major_formatter(dates.DateFormatter('%Y')) 
    # makes sure the x axis shows only the year 
    ax.set_xticks([datetime(year, 1, 1) for year in year_counts])
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys())
    plt.tight_layout()
    plt.savefig(title+'.png')
    plt.show()
    
    
    # usinf fastest dictionary created from above, plots a table with each year and distance
    # with the date of the run and the time taken for that segment
    distances = []
    seen = set()
    for year_data in fastest.values():
        for distance in year_data:
            if distance not in seen:
                seen.add(distance)
                distances.append(distance)
    years = sorted(fastest.keys())
    table_data = []
    for distance in distances:
        row = [distance]
        for year in years:
            if distance in fastest[year]:
                date, duration_ms = fastest[year][distance]
                duration_td = timedelta(seconds= round(duration_ms /1000))
                row.append(f"{date.strftime('%Y-%m-%d')} ({duration_td})")
            else:
                row.append("N/A")
        table_data.append(row)
    
    fig, ax = plt.subplots(figsize=(9,6))    
    ax.axis('off')
    table = ax.table(cellText=table_data, colLabels=["Distance"] + years, loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1.5,3)
    title = 'Fastest segment table'
    plt.title(title)
    plt.tight_layout()
    #fig.canvas.draw()
    plt.savefig(title+'.png')
    plt.show()
    
def day_pie(df):
    # piechart for runs by day of the week
    days = [0 for x in range(7)]
    for x in df['run_dates']:
        days[x.weekday()] += 1
    plt.figure(figsize=(15, 10))    
    mylabels = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    total = sum(days)
    # means number of days rather than percentage is shown
    plt.pie(days, labels=mylabels,autopct=lambda p: '{:.0f}'.format(p * total / 100))
    plt.savefig('piechart.png')
    plt.show() 
    
def cum_time(df):
    # total time
    cum_time = np.cumsum(df['durations'])
    plt.figure(figsize=(15,10))
    plt.plot(df['run_dates'], cum_time, drawstyle='steps-post')
    title = "Cumulative time"
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Duration (h)")
    plt.tight_layout()
    plt.savefig(title+'.png')
    plt.show()
    
def cum_elevation_gain_loss(df):
    # total elevation
    cum_gain = np.cumsum(df['elevation_gain'])
    cum_loss = np.cumsum(df['elevation_loss'])
    plt.figure(figsize=(15,10))
    plt.plot(df['run_dates'], cum_gain, label ='Elevation Gain', drawstyle='steps-post')
    plt.plot(df['run_dates'], cum_loss, label = 'Elevation Loss', drawstyle='steps-post')
    title = "Cumulative elevation gain and loss"
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Distance (m)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(title+'.png')
    plt.show()
    
    
def histo_paces_distance(df):
    # histogram of paces and distances together
    plt.figure(figsize=(15, 10))
    # paces
    plt.subplot(1, 2, 1)
    plt.hist(df['paces'], bins=20, color='blue', edgecolor='black')
    plt.xlabel('Pace (m/km)')
    plt.ylabel('Frequency')
    plt.title('Distribution of Paces')
    
    # distances
    plt.subplot(1, 2, 2)
    plt.hist(df['distances'], bins=20, color='red', edgecolor='black')
    plt.xlabel('Distance (km)')
    plt.ylabel('Frequency')
    plt.title('Distribution of Distances')
    
    plt.tight_layout()
    title = "Pace and distance histogram"
    plt.tight_layout()
    plt.savefig(title+'.png')
    plt.show()
    
def boxplot_pace_year(df):
    # boxplot of paces by year
    years = df['run_dates'].apply(lambda x: x.year).unique()
    box_data = []
    # add to box data paces for each year
    for year in years:
        yearly_paces = df[df['run_dates'].apply(lambda x: x.year) == year]['paces']
        box_data.append(yearly_paces)
    plt.figure(figsize=(15, 10))
    plt.boxplot(box_data, labels=years)
    plt.xlabel('Year')
    plt.ylabel('Pace (m/km)')
    title = 'Pace Distribution by Year'
    plt.title(title)
    plt.tight_layout()
    plt.savefig(title+'.png')
    plt.show()
    
def heatmap_hour_day(df):
    # plots heatmap of run by time of day for each day of the week
    df['run_dates'] = pd.to_datetime(df['run_dates'])
    df['weekday'] = df['run_dates'].dt.dayofweek
    df['hour'] = df['run_dates'].dt.hour
    heatmap_data = df.groupby(['weekday', 'hour']).size().unstack()
    # group the runs by day of the week and hour and counts them with size and unstack formats into below
    # creates this table with my data
    """
    hour      8    9    10   11   12    13    14   15   16   17   20
    weekday                                                         
    0        NaN  NaN  1.0  3.0  6.0   7.0   1.0  8.0  2.0  1.0  NaN
    1        NaN  NaN  1.0  NaN  4.0   5.0   5.0  6.0  6.0  1.0  NaN
    2        NaN  1.0  1.0  2.0  5.0   5.0   7.0  7.0  2.0  NaN  1.0
    3        NaN  NaN  NaN  2.0  4.0   4.0   5.0  6.0  5.0  1.0  NaN
    4        NaN  NaN  NaN  1.0  1.0   8.0   6.0  8.0  3.0  NaN  NaN
    5        1.0  NaN  1.0  2.0  NaN   5.0   6.0  5.0  1.0  NaN  NaN
    6        1.0  NaN  NaN  5.0  4.0  11.0  10.0  3.0  1.0  NaN  NaN
    """
    plt.figure(figsize=(15, 10))
    plt.imshow(heatmap_data, cmap='viridis', aspect='auto')
    plt.colorbar(label='Frequency')
    plt.xlabel('Hour of Day')
    plt.ylabel('Day of Week')
    title = 'Frequency of Runs by Day of Week and Hour of Day'
    plt.title(title)
    # xticks for each hour
    plt.xticks(np.arange(len(heatmap_data.columns)), heatmap_data.columns)
    plt.yticks(np.arange(len(heatmap_data.index)), ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
    plt.grid(False)
    plt.tight_layout()
    plt.savefig(title+'.png')
    plt.show()
    
def scatter_distance_pace(df):
    # scatter distances against pace
    plt.figure(figsize=(15, 10))
    plt.scatter(df['distances'], df['paces'])
    plt.xlabel('Distance (km)')
    plt.ylabel('Pace (m/km)')
    title = 'Relationship between Pace and Distance'
    plt.title(title)
    plt.tight_layout()
    plt.savefig(title+'.png')
    plt.show()
    
def distance_month(df):
    # show distance for each month ever
    df['month'] = df['run_dates'].dt.month
    df['year'] = df['run_dates'].dt.year
    monthly_distance = df.groupby(['year', 'month'])['distances'].sum()
    monthly_labels = [f"{year}-{month:02d}" for year, month in monthly_distance.index]
    plt.figure(figsize=(15, 10))
    plt.plot(monthly_labels, monthly_distance.values, marker='o')
    plt.xlabel('Month')
    plt.ylabel('Total Distance (km)')
    title = 'Monthly Total Distance'
    plt.title(title)
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(title+'.png')
    plt.show()
    
    
def pace_temperature(df):
    # scatter pace against temperature
    plt.figure(figsize=(15,10))
    plt.scatter(df['paces'], df['temp'])
    title = "Pace against temperature"
    plt.title(title)
    plt.xlabel("Pace (m/km)")
    plt.ylabel("Temperature (°C)")
    plt.tight_layout()
    plt.savefig(title+'.png')
    plt.show()
    
def boxplots_distance_pace_weather(df):    
    # remove runs where there is not a condition code (coco)
    filtered_df = df.dropna(subset=['coco'])    
    # plot paces by weather condition
    filtered_df.boxplot(column='paces', by='coco', figsize=(15, 10))
    plt.xlabel('Weather Condition')
    plt.ylabel('Pace (m/km)')
    title = 'Box Plot of Pace by Weather Condition'
    plt.title(title)
    plt.suptitle('')
    plt.grid(False)
    plt.xticks(rotation=45)  
    plt.tight_layout()
    plt.savefig(title+'.png')
    plt.show()
    
    # plot distances by weather condition
    filtered_df.boxplot(column='distances', by='coco', figsize=(15, 10))
    plt.xlabel('Weather Condition')
    plt.ylabel('Distance (m)')
    title = 'Box Plot of Distance by Weather Condition'
    plt.title(title)
    plt.suptitle('')
    plt.grid(False)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(title+'.png')
    plt.show()