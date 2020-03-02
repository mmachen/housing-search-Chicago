from pyzillow.pyzillow import ZillowWrapper, GetDeepSearchResults, GetUpdatedPropertyDetails, ZillowError

def get_data_from_zillow_api(address, zipcode, API_key):
    """
    ##################################################################
    ###    This code generates public transportation to a location
    ###    using Google's Directions API.
    ###    _________________________________________________________
    ###    INPUT:    address - Redfin Raw Source Data "Address, City, State"
    ###              zipcode - Redfin Raw Source Data "Zipcode" 
    ###              API_key - Google API (string)
    ###    OUTPUT:   PyZillow class 
    ###################################################################
    """
    # Load Zillow API 
    zillow_data = ZillowWrapper(API_key)

    try:
        deep_search_response = zillow_data.get_deep_search_results(address,zipcode)
        result = GetDeepSearchResults(deep_search_response)
    except: 
        result = None
    return(result) 
