
import utils
import time
import numpy as np


# Parameters
isochrones = [5, 10, 15, 20]
modes = ['bus']
city = 'Chattanooga, TN'
activities = [['[sport]'], ['[Healthcare]']]

N_star = ...
freqencies = []




# Valhalla API
url_valhalla = "https://valhalla1.openstreetmap.de/isochrone"

# TIGERweb API
url_TIGERweb = "https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/tigerWMS_Census2010/MapServer/18/query"

# Overpass API
#* We use overpy, a python wrapper of the overpass API

# Census API
#* We use cenpy, a python wrapper of the census API





blocks = utils.get_census_blocks(city)
block_geoids = blocks['GEOID'][:3]

# Initialize the array of opportunities
O_itj = np.zeros((len(blocks), len(isochrones), len(activities)))

# Initialize the time tracker
s_time = time.time()

#TODO: Need to be changed when valhalla local server is built
for i, geoid in enumerate(block_geoids):
    
    centroid_lat, centroid_lon = utils.get_census_block_centroid(geoid)
    loc_list = [{'lat': centroid_lat, 'lon': centroid_lon}]

    for t, interval in enumerate(isochrones):
        
        # Time tracker due to the demo Valhalla server
        t_time = time.time()
        time.sleep(max(0, 1 - t_time + s_time))
        s_time = time.time()
        
        
        polygon = utils.get_isochrones(loc_list, modes[0], interval)
        
        for j, a in enumerate(activities):

            places = utils.get_places_OSM(polygon, a)
            if t == 0:
                O_itj[i][t][j] = len(places.nodes)
            else:
                O_itj[i][t][j] = len(places.nodes) - O_itj[i][t-1][j]
        
# Compute the MEP metric
# TODO: Use the correct formula once the debugging is done
blocks['Quant'] = np.sum(O_itj, axis = (1, 2))


# Generate the plot
utils.visualization(blocks, 'Quant')



