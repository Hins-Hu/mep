import requests
import osmnx as ox
import geopandas as gpd
import numpy as np


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

    

def mep_computation(O_tj, N_star, N, f, isochrones, e, c, alpha = -0.5, beta = -0.08, sigma = -0.5):  
    
    """_summary_

    Args:
        O_tj (np.ndarray): O_tj[t][j] =  # of opportunities of type j in the polygon within t time  
        N_star (int): A factor. The total number of benchmark opportunities across multiple cities (for example, the number of meal opportunities)
        N (np.ndarray): N[j] = the total # of opportunities of activity j
        f (np.ndarray): f[j] = the frequency that people access opportunities of activity j
        isochrones (list): A list of isochrones (e.g., [10, 20, 30, 40])
        e (float): The energy intensity (kWh per passenger-mile)
        c (float): The cost (dollar per passenger-mile)
        alpha (float, optional): weighing factors. Defaults to -0.5.
        beta (float, optional): weighing factors. Defaults to -0.08.
        sigma (float, optional): weighing factors. Defaults to -0.5.
    """
    
    O_t = O_tj @ (f / N) * (N_star * sum(f))
    
    M_t = np.repeat(alpha * e, len(isochrones)) + beta * isochrones + np.repeat(sigma * c, len(isochrones))
    
    np.insert(O_t, 0, 0)
    mep = 0
    for ind, o1, o2 in enumerate(zip(O_t[:-1], O_t[1:])):
        mep += (o2 - o1) * np.exp(M_t[ind])
        
    return mep
        
    
    