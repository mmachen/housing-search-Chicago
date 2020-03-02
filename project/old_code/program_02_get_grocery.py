
import extra_programs as helper
import pandas as pd 

def get_grocery_features(redfinHome_LatLon, groceryList):
    """
    ##################################################################
    ###    This code gathers information about a location
    ###    using ARCGIS API and distance functions.
    ###    _________________________________________________________
    ###    INPUT:    redfinHome_LatLon - List of latitude / longitude
    ###              groceryList - Pandas DataFrame of grocery stores 
    ###    OUTPUT:   Dictionary
    ###################################################################
    """
    x1 = redfinHome_LatLon[0]
    y1 = redfinHome_LatLon[1]
    tempDistance = []
    for store in range(groceryList.shape[0]):
        x2 = groceryList.LATITUDE[store]
        y2 = groceryList.LONGITUDE[store]
        d = helper.distanceGPS(x1,y1,x2,y2)
        tempDistance.append({"NAMES":groceryList.NAME[store],
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

    return( ({  "GROCERY_CLOSEST" : closestStore['NAMES'].values[0],
                "GROCERY_CLOSEST_DST" : closestStore['DISTANCE'].values[0],
                "GROCERY_WALK_NUM": len(closeSubset),
                "GROCERY_WALK": ', '.join(closeSubset),
                "GROCERY_DRIVE_NUM": len(fartherSubset),
                "GROCERY_DRIVE": ', '.join(fartherSubset)
                        }) )


def get_liquor_features(redfinHome_LatLon, beerTobaccoList):
    """
    ##################################################################
    ###    This code gathers information about a location
    ###    using ARCGIS API and distance functions.
    ###    _________________________________________________________
    ###    INPUT:    redfinHome_LatLon - List of latitude / longitude
    ###              beerTobaccoList - Pandas DataFrame of liquor stores 
    ###    OUTPUT:   Dictionary
    ###################################################################
    """
    x1 = redfinHome_LatLon[0]
    y1 = redfinHome_LatLon[1]
    tempDistance = []
    for store in range(beerTobaccoList.shape[0]):
        x2 = beerTobaccoList.LATITUDE[store]
        y2 = beerTobaccoList.LONGITUDE[store]
        d = helper.distanceGPS(x1,y1,x2,y2)
        tempDistance.append({"NAMES":beerTobaccoList.NAME[store],
                                "DISTANCE":d })
    tempDistance = pd.DataFrame(tempDistance)
    # Closest store 
    closestStore = tempDistance[tempDistance['DISTANCE'] == min(tempDistance['DISTANCE'])]
    # List stores within 0.5 miles of home 
    closeSubset = tempDistance[tempDistance['DISTANCE'] <= 0.5]
    closeSubset = closeSubset['NAMES'].unique().tolist()
    return( ({  "LIQUOR_CLOSEST_DST" : closestStore['DISTANCE'].values[0],
                "LIQUOR_WALK_NUM": len(closeSubset)
                        }) )
