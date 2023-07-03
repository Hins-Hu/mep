
import utils
import osmnx as ox
import time
from cenpy import products


# Bounding box for Chattanooga
min_lon = -85.45
max_lon = -85.07
min_lat = 34.99
max_lat = 35.19

# Server address
url = "https://valhalla1.openstreetmap.de/isochrone"


# Parameters

isochrones = [10, 20, 30, 40]

modes = ['tranit', 'multimodal', 'ride-sharing']



# centroids = utils.generate_square_centroids(bbox = [min_lon, max_lon, min_lat, max_lat], square_size = 0.1)


# for c in centroids:
#     p = utils.get_isochrones([c])
#     time.sleep(1)


