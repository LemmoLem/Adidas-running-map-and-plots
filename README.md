# Adidas-running-map-and-plots
This project allows users to visualize their running data from Adidas Running on a map and create various plots. Users can see all their runs displayed on an interactive map, providing a comprehensive view of their running history.

# Features
Interactive Map: View all your runs on a map using Folium.

Data Plots: Generate plots to analyze your running data.
# Prerequisites
To use this project, you need to have the following installed:
* Python 3.x
* Folium
* ezGPX
* gpxpy
* Meteostat
* matplotlib

You can install the required Python packages using pip

# Usage
This project requires you to export your adidas runnig data. This takes a few days to be exported and you recieve an email when its done.
https://help.runtastic.com/hc/en-us/articles/360000953365-Export-Account-Data

Unzip the data into a new folder where you download this program called "adidas data"
Alternatively you can copy the "sport sessions" folder in the data to a folder called "adidas data" as this is the only data used in the program

Run the main script to process the data and generate the map and plots.
Open the generated HTML file to view your interactive map.

The map shows every run which has gps data associated with it. You can change the method of the map creation to not include pop up about each run if so desired.

There is a javascript file which highlights the run you hover over and changes colour when clicked on.

Note: due to the way polylines are added to the map and the way the map works by being tiles, the runs only show on the starting tiles (so don't go all the way east or west and loop round, as the runs wont be shown there)
# Example
I have not shared a generated map (instead this screenshot) as running data contains locations which are private, the file created can be relatively for a webpage, with my 200 runs on a map the map size was 1.7mb
![map](https://github.com/LemmoLem/Adidas-running-map-and-plots/assets/124703792/63dd8b3a-1839-4507-b7b8-35f0c5e6f28e)
The plots are generated with matplotlib and are shown in ide as well. The images are saved to the same folder as where you run this program
![image](https://github.com/LemmoLem/Adidas-running-map-and-plots/assets/124703792/f5551754-73a5-4697-a21b-611d49992676)
