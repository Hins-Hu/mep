
import utils
import numpy as np
import sys
from concurrent.futures import ThreadPoolExecutor



city = 'Chattanooga'
state = 'TN'

# Set the categories of activities
"""
Category 1: Religious facility/Schools/Day care
Category 2: Health care
Category 3: Retails
Category 4: Sports & entertainment
Category 5: Food & restaurant
"""
#* Need to mannually input all relevant activities according to OSM features
C1 = ['[amenity=college]', '[amenity=driving_school]', '[amenity=kindergarten]', '[amenity=language_school]', '[amenity=music_school]',
      '[amenity=school]', '[amenity=research_institute]', '[amenity=university]', '[amenity=place_of_worship]']

C2 = ['[healthcare]', '[amenity=baby_hatch]', '[amenity=clinic]', '[amenity=dentist]', '[amenity=doctors]', '[amenity=hospital]',
      '[amenity=nursing_home]', '[amenity=pharmacy]', '[amenity=veterinary]', '[amenity=social_facility]']

C3 = ['[shop]']

C4 = ['[leisure]', '[sport]', '[tourism]', '[amenity=arts_centre]', '[amenity=casino]', '[amenity=cinema]', '[amenity=community_centre]', '[amenity=conference_centre]',
      '[amenity=events_venue]', '[amenity=exhibition_centre]', '[amenity=fountain]', '[amenity=gambling]', '[amenity=music_venue]',
      '[amenity=nightclub]', '[amenity=planetarium]', '[amenity=studio]', '[amenity=theatre]', '[amenity=social_centre]', '[amenity=public_bookcase]']

C5 = ['[amenity=bar]', '[amenity=biergarten]', '[amenity=cafe]', '[amenity=fast_food]', '[amenity=food_court]', '[amenity=ice_cream]', '[amenity=pub]',
      '[amenity=restaurant]']
activities = [C1, C2, C3, C4, C5]


# Count the total number of opportunities of different activities in Chattanooga
N = np.zeros(len(activities))
for j, a in enumerate(activities):
    places = utils.get_places_city_OSM(city = city, tags = a)
    N[j] = len(places.nodes)

# Set the total number of benchmark opportunities
N_star = N[-1]
    
# The trip frequencies
freq = [0.031, 0.015, 0.195, 0.084, 0.067]

# The travel mode
modes = ['multimodal']

# The energy coefficient
e = 0.65

# The cost coefficient
c = 1.05

# Travel time are in minutes
isochrones = [5, 10, 15, 20]




# Valhalla API
url_valhalla = "https://valhalla1.openstreetmap.de/isochrone"

# TIGERweb API
url_TIGERweb = "https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/tigerWMS_Census2010/MapServer/18/query"

# Overpass API
#* We use overpy, a python wrapper of the overpass API

# Census API
#* We use cenpy, a python wrapper of the census API




blocks = utils.get_census_blocks(city + ', ' + state)
block_geoids = blocks['GEOID']



# Initialize the array of opportunities
O_itj = np.zeros((len(blocks), len(isochrones), len(activities)))
mep = np.zeros(len(blocks))


# Define the executable function for multithreading
def compute_one_block(i):
    
    geoid = block_geoids[i]
    
    # Monitor the progress
    print("Now at i = ", i)
    sys.stdout.flush()
    
    centroid_lat, centroid_lon = utils.get_census_block_centroid(geoid)
    loc_list = [{'lat': centroid_lat, 'lon': centroid_lon}]

    for t, interval in enumerate(isochrones):
        
        polygon = utils.get_isochrones(loc_list, modes[0], interval)
        
        if polygon != None:
            for j, a in enumerate(activities):
                places = utils.get_places_polygon_OSM(polygon, a)
                O_itj[i][t][j] = len(places.node_ids)
    
    # Compute the MEP metric
    mep[i] = utils.mep_computation(O_itj[i, :, :], N_star, N, freq, isochrones, e, c)    
               
               
# Enable multithreading
with ThreadPoolExecutor(max_workers = 12) as executor:
    for i, _ in enumerate(block_geoids):
        executor.submit(compute_one_block, i)
        
#  wait for all tasks to complete before the main thread continues
executor.shutdown()


# Append the computed mep metric to the blocks dataframe
blocks['MEP'] = mep

# Output data
blocks.to_file("chatt_census_blocks.geojson", driver='GeoJSON')

# Generate the plot
utils.visualization(blocks, 'MEP')



