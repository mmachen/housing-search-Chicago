
import googlemaps
import extra_programs as helper 
import pandas as pd 

def get_places_from_google_api(search, API_key, location_address):
    """
    ##################################################################
    ###    This code generates public places near a location
    ###    using Google's Places API.
    ###    _________________________________________________________
    ###    INPUT:    search - keyword (string) 
    ###              API_key - Google API (string)
    ###              location_address - Location (list of Lat, Lon) 
    ###    OUTPUT:   Dictionary
    ###################################################################
    """
    # Load GoogleMaps API 
    gmaps = googlemaps.Client(key=API_key)  # Up to 40,000 calls per month

    search_results = gmaps.places_nearby(location=location_address,keyword=search,rank_by="distance")['results'] 

    if len(search_results) != 0: 
        x1 = location_address[0]
        y1 = location_address[1]

        tempDistance = []
        for place in range(len(search_results)):
            x2 = search_results[place]['geometry']['location']['lat'] 
            y2 = search_results[place]['geometry']['location']['lng'] 
            d = helper.distanceGPS(x1,y1,x2,y2)
            tempDistance.append({"NAMES":search_results[place]['name'],
                                    "DISTANCE":d })
        tempDistance = pd.DataFrame(tempDistance)

        # Closest store 
        closestStore = tempDistance[tempDistance['DISTANCE'] == min(tempDistance['DISTANCE'])]
        # List stores within 0.5 miles of home 
        closeSubset = tempDistance[tempDistance['DISTANCE'] <= 0.5]
        closeSubset = closeSubset['NAMES'].unique().tolist()
        # List stores within 2 miles of home
        fartherSubset = tempDistance[tempDistance['DISTANCE'] <= 2]
        fartherSubset = fartherSubset['NAMES'].unique().tolist()

        return( ({  "CLOSEST" : closestStore['NAMES'].values[0],
                    "CLOSEST_DST" : closestStore['DISTANCE'].values[0],
                    "WALK_NUM": len(closeSubset),
                    "WALK": ', '.join(closeSubset),
                    "DRIVE_NUM": len(fartherSubset),
                    "DRIVE": ', '.join(fartherSubset)
                            }) )
    else: 
        return( ({  "CLOSEST" : "",
                "CLOSEST_DST" : float('nan'),
                "WALK_NUM": float('nan'),
                "WALK": "",
                "DRIVE_NUM": float('nan'),
                "DRIVE": ""
                        }) )
                        
