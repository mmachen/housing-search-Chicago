##################################################################
###    This code Zillow's "zestimate" per house by using Zillow's
###    housing data API. 
###    _________________________________________________________
###    INPUT:    Redfin Raw Source Data
###              Zillow API key (string)
###    OUTPUT:   Saved File 
###################################################################

import pandas as pd
from decimal import * 
from pyzillow.pyzillow import ZillowWrapper, GetDeepSearchResults, GetUpdatedPropertyDetails, ZillowError

# Read data from CSV files
csv1_path = "output/commute_grocery_data.csv"

# Read in RedFin data
prop_df = pd.read_csv(csv1_path)
n = prop_df.shape[0]
print(n) 

# Initialize Zillow API (limit of 1000 calls per day) 
csvK_path = "delete/input2.txt"
file = open(csvK_path,"r") 
API = file.read()
file.close()

zillow_data = ZillowWrapper(API)

for home in range(n): 
#home = 0
    print("Percentage Complete: " + str(round((home+1)/n*100,2)) + "%")
    address = ",".join([prop_df.ADDRESS[home],prop_df.CITY[home],prop_df.STATE[home]])
    zipcode = prop_df.ZIP[home] 
    
    try:
        deep_search_response = zillow_data.get_deep_search_results(address,zipcode)
        result = GetDeepSearchResults(deep_search_response)

        prop_df.at[home,'ZILLOW_ID'] = result.zillow_id
        prop_df.at[home,'ZILLOW_URL'] = result.home_detail_link 
        prop_df.at[home,'LAST_TAX_YEAR'] = result.tax_year
        if str(result.tax_value) != "None":
            prop_df.at[home,'LAST_TAX_ASSESSMENT'] = float(result.tax_value)/10
        prop_df.at[home,'ESTIMATED_TAX'] = prop_df.PRICE[home]*0.02117 # Based on Average Tax Rate for Cook County 
        #print(prop_df.LAST_TAX_ASSESSMENT[home]) 
        #if str(result.tax_value) != "None":
        #    _temp = round(float(result.tax_value)/10)*0.02117
        #    print("_temp is " + str(_temp))
        #    prop_df.at[home,'ESTIMATED_TAX'] = _temp # Based on Average Tax Rate for Cook County 
        prop_df.at[home,'LAST_SOLD_DATE'] = result.last_sold_date
        prop_df.at[home,'LAST_SOLD_PRICE'] = result.last_sold_price
        prop_df.at[home,'ZESTIMATE'] = result.zestimate_amount 
        prop_df.at[home,'ZESTIMATE_LAST_UPDATED'] = result.zestimate_last_updated 
        prop_df.at[home,'ZESTIMATE_VALUE_CHANGE'] = result.zestimate_value_change 
        prop_df.at[home,'ZESTIMATE_RANGE_HIGH'] = result.zestimate_valuation_range_high
        prop_df.at[home,'ZESTIMATE_RANGE_LOW'] = result.zestimate_valuationRange_low
    except ZillowError:
        print("ERROR") 

# Write the new cleaned dataset to directory
csv2_path = "output/commute_grocery_zillow_data.csv"
prop_df.to_csv(csv2_path,index=False)

