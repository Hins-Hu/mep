
import utils

# Server address
url = "https://valhalla1.openstreetmap.de/isochrone"


# Parameters

isochrones = [10, 20, 30, 40]

modes = ['tranit', 'multimodal', 'ride-sharing']


... 



# Get the isochrones
polygon = utils.get_isochrones()


