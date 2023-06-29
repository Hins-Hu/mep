import requests
import osmnx as ox
import geopandas as gpd


def get_isochrones(loc_list):

    url = "https://valhalla1.openstreetmap.de/isochrone"
    json_input = {"locations": loc_list,"costing":"pedestrian","contours":[{"time":15.0,"color":"ff0000"}]}

    result = requests.get(url, json = json_input)
    data = result.json()

    polygon = data['features'][0]['geometry']['coordinates']

    return polygon



def generate_square_centroids(bbox, square_size = 0.01):
    

    min_lon, max_lon, min_lat, max_lat = bbox
    
    lon_range = max_lon - min_lon
    lat_range = max_lat - min_lat
    num_squares_lon = round(lon_range / square_size)
    num_squares_lat = round(lat_range / square_size)

    # Calculate the centroid coordinates of each square
    centroids = []
    for i in range(num_squares_lon):
        for j in range(num_squares_lat):
            
            square_min_lon = min_lon + i * square_size
            square_min_lat = min_lat + j * square_size

            centroid_lon = square_min_lon + (square_size / 2)
            centroid_lat = square_min_lat + (square_size / 2)
            
            centroids.append({"lat": centroid_lat, "lon": centroid_lon})         
        
    return centroids

    



