import pandas as pd 
from arcgis.gis import GIS
from arcgis.geocoding import geocode

def get_data_from_arcGIS_api(zipcodes, keywords):
    """
    ##################################################################
    ###    This code generates public addresses 
    ###    using ARCGIS's API.
    ###    _________________________________________________________
    ###    INPUT:    array of zipcodes (numpy.ndarray) 
    ###              list of keyword to search by (list of strings)
    ###    OUTPUT:   Pandas DataFrame
    ###################################################################
    """
    # Number of zipcodes 
    n = len(zipcodes)

    # Initialize List and GIS service
    listedList = []
    gis = GIS()
    # Loop through all zip codes in Cook County and save unique items with geocode
    for id in range(n):
        yourZip = geocode(str(zipcodes[id]))[0]
        for word in range(len(keywords)):
            searchedItem = geocode(keywords[word], yourZip['extent'], max_locations=1000)
            for item2 in range(len(searchedItem)):
                listedList.append({"ADDRESS": searchedItem[item2]['attributes']['Place_addr'],
                                    "PHONE": searchedItem[item2]['attributes']['Phone'],
                                    "POSTAL": searchedItem[item2]['attributes']['Postal'],
                                    "LONGITUDE": searchedItem[item2]['location']['x'],
                                    "LATITUDE": searchedItem[item2]['location']['y']})
    listedList = pd.DataFrame(listedList)
    # Find if there are duplicates (by ADDRESS)
    dup_index = listedList.duplicated(["ADDRESS"])
    prop_dup = listedList[dup_index]
    listedList.drop_duplicates(subset=['ADDRESS'],inplace=True)
    return(listedList) 