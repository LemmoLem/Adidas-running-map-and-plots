"""
if u are generating map with pop up then dataframe created needs to be with weather method
"""

import load_data
import gpsData
import savePlots
import make_index_page

# this code creates the map and a html page with plots
# both saved to this folder at foliumMap.hmtl and index.html
df = load_data.create_df_with_weather()
gpsData.make_map_with_pop_up(df)
savePlots.make_plots(df)
make_index_page.generate_html()
