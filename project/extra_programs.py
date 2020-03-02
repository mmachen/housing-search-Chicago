from math import sin, cos, sqrt, atan2, radians

def distanceGPS(lat1,lon1,lat2,lon2):
    """
    ##################################################################
    ###     This code calculates the distance (miles) between two points 
    ###     __________________________________________________________
    ###     INPUT:      lat1 - Latitude (degrees) of first object
    ###                 lon1 - Longitude (degrees) of first object
    ###                 lat2 - Latitude (degrees) of second object
    ###                 lon2 - Longitude (degrees) of second object
    ###     OUTPUT:     distance
    ##################################################################
    """
    # approximate radius of earth in km
    R = 6373.0
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return(R * c * 0.62137)
