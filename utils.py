import requests
import numpy as np
import cenpy
import matplotlib.pyplot as plt
import geopandas as gp
import overpy


def get_census_block_centroid(geoid):
    
    url = 'https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/tigerWMS_Census2010/MapServer/18/query'
    params = {
        'f': 'json',
        'where': f"GEOID='{geoid}'",
        'outFields': 'CENTLAT,CENTLON'
    }

    response = requests.get(url, params=params)
    data = response.json()
    
    

    # Extract centroid coordinates from the response
    centroid_lat = data['features'][0]['attributes']['CENTLAT']
    centroid_lon = data['features'][0]['attributes']['CENTLON']

    return centroid_lat, centroid_lon



def get_places_OSM(polygon, tags = ["[amenity=restaurant]"]):
    
    # Convert the nested-list polygon to a one-line string format
    polygon_str = ""
    for ind, (lon, lat) in enumerate(polygon):
        if ind != 0:
            polygon_str += " "
        polygon_str += str(lat)
        polygon_str += " "
        polygon_str += str(lon)

    # Construct a one-line argument for the overpass api
    arg_polygon = f"node(poly: '{polygon_str}')"
    arg_tag =  ''.join(tags)
    arg_end = "out;"
    arg = arg_polygon + arg_tag + ";" + arg_end
    
    overpass_api = overpy.Overpass()
    result = overpass_api.query(arg)
    
    return result
    

def get_isochrones(loc_list, mode = "bus", time = 15):
    
    
    url_local = "http://0.0.0.0:8002/isochrone"
    
    json_input = {"locations": loc_list,"costing":mode,"contours":[{"time":time,"color":"ff0000"}]}

    result = requests.get(url_local, json = json_input)

    try:
        data = result.json()
    except requests.exceptions.JSONDecodeError:
        print("An error is caught! Print the result from requests.get().")
        print(result)
        return None
        

    polygon = data['features'][0]['geometry']['coordinates']

    return polygon


def get_census_blocks(place = 'Chattanooga, TN'):
    
    return  cenpy.products.Decennial2010().from_place(place, level='block') 


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
        
        
def visualization(blocks, metric):
    
    f, ax = plt.subplots(1, 1, figsize = (20, 20))
    blocks.plot(metric, ax = ax, cmap = 'viridis')
    f.savefig('./plot.png', dpi = 300)
    
    
    
    