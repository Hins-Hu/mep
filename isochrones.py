import requests


url = "https://valhalla1.openstreetmap.de/isochrone"

json_input = {"locations":[{"lat":40.744014,"lon":-73.990508}],"costing":"pedestrian","contours":[{"time":15.0,"color":"ff0000"}]}


result = requests.get(url, json = json_input)
data = result.json()


polygon = data['features'][0]['geometry']['coordinates']
print(polygon)

