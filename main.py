
import utils
import numpy as np
import sys
from concurrent.futures import ThreadPoolExecutor





# Parameters
isochrones = [5, 10, 15, 20]
modes = ['multimodal']
city = 'Chattanooga, TN'



activities = [['[Healthcare]','[amenity=restaurant]']]

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
block_geoids = blocks['GEOID']

# Initialize the array of opportunities
O_itj = np.zeros((len(blocks), len(isochrones), len(activities)))



# Define the executable function for multithreading
def compute_one_block(i):
    
    geoid = block_geoids[i]
    
    # Monitor the progress
    # print("Now at i = ", i)
    sys.stdout.flush()
    
    centroid_lat, centroid_lon = utils.get_census_block_centroid(geoid)
    loc_list = [{'lat': centroid_lat, 'lon': centroid_lon}]

    for t, interval in enumerate(isochrones):
        
        polygon = utils.get_isochrones(loc_list, modes[0], interval)
        
        if polygon != None:
            for j, a in enumerate(activities):
                places = utils.get_places_OSM(polygon, a)
                if t == 0:
                    O_itj[i][t][j] = len(places.nodes)
                else:
                    O_itj[i][t][j] = len(places.nodes) - O_itj[i][t-1][j]        
               
               
# Enable multithreading
with ThreadPoolExecutor(max_workers = 12) as executor:
    for i, _ in enumerate(block_geoids):
        executor.submit(compute_one_block, i)
        
#  wait for all tasks to complete before the main thread continues
executor.shutdown()


# Compute the MEP metric
# TODO: Use the correct formula once the debugging is done
blocks['Quant'] = np.sum(O_itj, axis = (1, 2))


# Generate the plot
utils.visualization(blocks, 'Quant')



