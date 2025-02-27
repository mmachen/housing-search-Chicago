

import pandas as pd 
import program_00_get_commute as commute
import program_01_zillow as zillow 
import program_02_crime as crime 
import program_03_googleSearch as search
import program_04_affordableHousing as afford

if __name__ == '__main__':

    # Work Address
    work = "111 E Pearson St, Chicago, IL"    

    # Read in RedFin data (new)
    csv1_path = "data_sets/RedFin_raw_data.csv"
    raw_df = pd.read_csv(csv1_path)
    raw_df.columns = ["SALE_TYPE","SOLD_DATE","PROPERTY_TYPE","ADDRESS","CITY","STATE","ZIP","PRICE","BEDS","BATHS","LOCATION","SQFT","LOT_SIZE","YEAR","DAY_ON_MARKET","PRICE_PER_SQFT","HOA","STATUS","NEXT_OPEN_S","NEXT_OPEN_E","URL","SOURCE","MLS","FAVORITE","INTERESTED","LATITUDE","LONGITUDE"]
    raw_df = raw_df[~pd.isnull(raw_df["ADDRESS"])]
    raw_df = raw_df[~pd.isnull(raw_df["CITY"])]

    # Read in Output data (old) 
    csv2_path = "output/final_data.csv"
    try:
        out_df = pd.read_csv(csv2_path) 

        # Read in Training Data 
        csv_training = "output/training.csv" 
        train = pd.read_csv(csv_training) 
        # Find Updated Homes
        updated_homes = pd.merge(train["MLS"],out_df,on="MLS",how="inner") 
        target = updated_homes["MLS"].tolist()
        # Get Old Homes Not Updated
        old_training = train[~train["MLS"].isin(target)]
        # Get New Homes to be Added
        new_homes = out_df[~out_df["MLS"].isin(target)]
        # Concatenate 
        update = old_training.append(updated_homes,sort=True).append(new_homes,sort=True)
        update.index = range(len(update))
        # Write Training to File
        output_file_train = "output/training.csv"
        update.to_csv(output_file_train, index=False)

        prop_df = pd.merge(out_df[ out_df.columns.difference(raw_df.columns).tolist() + ["MLS"]  ],raw_df,on="MLS",how="right")
    except: 
        prop_df = raw_df

    n = prop_df.shape[0]

    # Merge Socio-Economic Values
    csvEco_path = "data_sets/socioeconomic_indicators.csv"
    eco_df = pd.read_csv(csvEco_path)
    prop_df = pd.merge(prop_df[prop_df.columns.difference(eco_df.columns).tolist()],eco_df,left_on="LOCATION",right_on="COMMUNITY AREA NAME",how="left")

    # Merge LanguagesSpoken Values
    csvLanguage = "data_sets/languages_spoken.csv"
    lang_df = pd.read_csv(csvLanguage)
    prop_df = pd.merge(prop_df[prop_df.columns.difference(lang_df.columns).tolist()],lang_df,left_on="LOCATION",right_on="Community Area Name",how="left")

    # Initialize Google API
    csvK_path = "delete/input.txt"
    file = open(csvK_path, "r")
    API_google = file.read()
    file.close()

    # Initialize Zillow API (limit of 1000 calls per day) 
    csvK_path = "delete/input2.txt"
    file = open(csvK_path,"r") 
    API_zillow = file.read()
    file.close()

    # Read in Crime Stats data (2019 - Present)
    csv2_path = "data_sets/Crimes_-_2019.csv"
    crime_df = pd.read_csv(csv2_path)
    crime_df.dropna(inplace=True)
    crime_df.index = range(crime_df.shape[0])

    # Read in Affordable Housing dataset
    csv_afford = "data_sets/Affordable_Rental_Housing_Developments.csv" 
    afford_df1 = pd.read_csv(csv_afford) 
    afford_df1 = afford_df1[["Address","Property Type","Latitude","Longitude"]]
    afford_df1.columns = ["ADDRESS","DESCRIPTION","LATITUDE","LONGITUDE"] 
    afford_df1.dropna(inplace=True)
    # Read in Chicago Housing Authority (CHA) dataset
    csv_afford2 = "data_sets/CHA_Housing.csv" 
    afford_df2 = pd.read_csv(csv_afford2) 
    afford_df2 = afford_df2[["ADDRESS","DESCRIPTION","LATITUDE","LONGITUDE"]]
    afford_df2.dropna(inplace=True)
    # Merge them...
    affordable_df = afford_df1.append(afford_df2) 
    affordable_df.drop_duplicates(subset = ["LATITUDE","LONGITUDE"],keep=False,inplace=True) 
    affordable_df.index = range(affordable_df.shape[0])

    # Main Update Loop 
    for i in range(0, n, 1):
        print("Percentage Complete: " + str(round((i+1)/n*100, 2)) + "%")
        if pd.isnull(prop_df["COMMUTE_TIME"][i]): 
            home = prop_df['ADDRESS'][i] + " " + prop_df['CITY'][i]
            commute_info = commute.get_directions_from_google_api(redfinData_home = home, API_key = API_google, location_address = work)
            prop_df.at[i,"COMMUTE_NUM_STEPS"] = commute_info["COMMUTE_NUM_STEPS"]
            if pd.isnull(commute_info["COMMUTE_TIME"]): 
                prop_df.at[i,"COMMUTE_TIME"] = commute_info["COMMUTE_TIME"]
            else: 
                tMin = commute_info["COMMUTE_TIME"].split(" ")
                if len(tMin) > 2: 
                    prop_df.at[i,"COMMUTE_TIME"] = int(tMin[0])*60 + int(tMin[2])  
                else:  
                    prop_df.at[i,"COMMUTE_TIME"] = int(tMin[0]) 
            prop_df.at[i,"COMMUTE_STEPS"] = commute_info["COMMUTE_STEPS"]
            prop_df.at[i,"WALKING_TIME"] = commute_info["WALKING_TIME"]
        if pd.isnull(prop_df["GROCERY_CLOSEST_DST"][i]): 
            homeLatLon = [ prop_df['LATITUDE'][i] , prop_df['LONGITUDE'][i] ]
            food = search.get_places_from_google_api("Grocery Stores",API_google, homeLatLon)
            prop_df.at[i,"GROCERY_CLOSEST"] = food["CLOSEST"]
            prop_df.at[i,"GROCERY_CLOSEST_DST"] = food["CLOSEST_DST"]
            prop_df.at[i,"GROCERY_WALK_NUM"] = food["WALK_NUM"]
            prop_df.at[i,"GROCERY_WALK"] = food["WALK"]
            prop_df.at[i,"GROCERY_DRIVE_NUM"] = food["DRIVE_NUM"]
            prop_df.at[i,"GROCERY_DRIVE"] = food["DRIVE"]
        if pd.isnull(prop_df["ZILLOW_ID"][i]):
            address = ",".join([prop_df.ADDRESS[i],prop_df.CITY[i],prop_df.STATE[i]])
            zipcode = prop_df.ZIP[i]
            zHome = zillow.get_data_from_zillow_api(address,zipcode,API_zillow) 
            prop_df.at[i,'ESTIMATED_TAX'] = prop_df.PRICE[i]*0.02117    # Based on Average Tax Rate for Cook County 
            if zHome != None: 
                prop_df.at[i,'ZILLOW_ID'] = zHome.zillow_id
                prop_df.at[i,'ZILLOW_URL'] = zHome.home_detail_link 
                prop_df.at[i,'LAST_TAX_YEAR'] = zHome.tax_year
                if str(zHome.tax_value) != "None":
                    prop_df.at[i,'LAST_TAX_ASSESSMENT'] = float(zHome.tax_value)/10
                prop_df.at[i,'LAST_SOLD_DATE'] = zHome.last_sold_date
                prop_df.at[i,'LAST_SOLD_PRICE'] = zHome.last_sold_price
                prop_df.at[i,'ZESTIMATE'] = zHome.zestimate_amount 
                prop_df.at[i,'ZESTIMATE_LAST_UPDATED'] = zHome.zestimate_last_updated 
                prop_df.at[i,'ZESTIMATE_VALUE_CHANGE'] = zHome.zestimate_value_change 
                prop_df.at[i,'ZESTIMATE_RANGE_HIGH'] = zHome.zestimate_valuation_range_high
                prop_df.at[i,'ZESTIMATE_RANGE_LOW'] = zHome.zestimate_valuationRange_low
        if pd.isnull(prop_df["LIQUOR_CLOSEST_DST"][i]): 
            homeLatLon = [ prop_df['LATITUDE'][i] , prop_df['LONGITUDE'][i] ]
            beer = search.get_places_from_google_api("Liquor Store",API_google, homeLatLon)
            prop_df.at[i,"LIQUOR_CLOSEST_DST"] = beer["CLOSEST_DST"]
            prop_df.at[i,"LIQUOR_WALK_NUM"] = beer["WALK_NUM"]
            prop_df.at[i,"LIQUOR_WALK"] = beer["WALK"]
            prop_df.at[i,"LIQUOR_DRIVE_NUM"] = beer["DRIVE_NUM"]
            prop_df.at[i,"LIQUOR_DRIVE"] = beer["DRIVE"]
        if pd.isnull(prop_df["BARS_CLOSEST_DST"][i]): 
            homeLatLon = [ prop_df['LATITUDE'][i] , prop_df['LONGITUDE'][i] ]
            bars = search.get_places_from_google_api("Bars",API_google, homeLatLon)
            prop_df.at[i,"BARS_CLOSEST_DST"] = bars["CLOSEST_DST"]
            prop_df.at[i,"BARS_WALK_NUM"] = bars["WALK_NUM"]
            prop_df.at[i,"BARS_WALK"] = bars["WALK"]
            prop_df.at[i,"BARS_DRIVE_NUM"] = bars["DRIVE_NUM"]
            prop_df.at[i,"BARS_DRIVE"] = bars["DRIVE"]
        if pd.isnull(prop_df["PARKS_CLOSEST_DST"][i]): 
            homeLatLon = [ prop_df['LATITUDE'][i] , prop_df['LONGITUDE'][i] ]
            parks = search.get_places_from_google_api("Parks",API_google, homeLatLon)
            prop_df.at[i,"PARKS_CLOSEST_DST"] = parks["CLOSEST_DST"]
            prop_df.at[i,"PARKS_WALK_NUM"] = parks["WALK_NUM"]
            prop_df.at[i,"PARKS_WALK"] = parks["WALK"]
            prop_df.at[i,"PARKS_DRIVE_NUM"] = parks["DRIVE_NUM"]
            prop_df.at[i,"PARKS_DRIVE"] = parks["DRIVE"]
        if pd.isnull(prop_df["DAYCARE_CLOSEST_DST"][i]): 
            homeLatLon = [ prop_df['LATITUDE'][i] , prop_df['LONGITUDE'][i] ]
            baby = search.get_places_from_google_api("Daycare",API_google, homeLatLon)
            prop_df.at[i,"DAYCARE_CLOSEST_DST"] = baby["CLOSEST_DST"]
            prop_df.at[i,"DAYCARE_WALK_NUM"] = baby["WALK_NUM"]
            prop_df.at[i,"DAYCARE_WALK"] = baby["WALK"]
            prop_df.at[i,"DAYCARE_DRIVE_NUM"] = baby["DRIVE_NUM"]
            prop_df.at[i,"DAYCARE_DRIVE"] = baby["DRIVE"]
        if pd.isnull(prop_df["COLLEGE_CLOSEST_DST"][i]): 
            homeLatLon = [ prop_df['LATITUDE'][i] , prop_df['LONGITUDE'][i] ]
            college = search.get_places_from_google_api("College",API_google, homeLatLon)
            prop_df.at[i,"COLLEGE_CLOSEST_DST"] = college["CLOSEST_DST"]
            prop_df.at[i,"COLLEGE_WALK_NUM"] = college["WALK_NUM"]
            prop_df.at[i,"COLLEGE_WALK"] = college["WALK"]
            prop_df.at[i,"COLLEGE_DRIVE_NUM"] = college["DRIVE_NUM"]
            prop_df.at[i,"COLLEGE_DRIVE"] = college["DRIVE"]
        if pd.isnull(prop_df["AFFORDABLE_NUM"][i]):   
            homeLatLon = [ prop_df['LATITUDE'][i] , prop_df['LONGITUDE'][i] ]
            zAfford = afford.get_afford_features(homeLatLon,affordable_df)
            prop_df.at[i,"AFFORDABLE_NUM"] = zAfford["NUM_AFFORDABLE_HOMES"] 
            prop_df.at[i,"AFFORDABLE_DESC"] = zAfford["AFFORDABLE_DESC"] 
        if pd.isnull(prop_df["GUN_SCORE"][i]):   
            homeLatLon = [ prop_df['LATITUDE'][i] , prop_df['LONGITUDE'][i] ]
            zCrime = crime.get_crime_features(homeLatLon,crime_df)
            prop_df.at[i,"GUN_SCORE"] = zCrime["GUN_SCORE"]
            prop_df.at[i,"DRUG_SCORE"] = zCrime["DRUG_SCORE"]
            prop_df.at[i,"MURDER_SCORE"] = zCrime["MURDER_SCORE"]
            prop_df.at[i,"THEFT_SCORE"] = zCrime["THEFT_SCORE"]
            prop_df.at[i,"HUMAN_SCORE"] = zCrime["HUMAN_SCORE"]
            prop_df.at[i,"OTHER_SCORE"] = zCrime["OTHER_SCORE"]
    # Update Crime Scores
    prop_df["CRIME_GUN"] = (prop_df["GUN_SCORE"] - prop_df["GUN_SCORE"].min()) / (prop_df["GUN_SCORE"].max() - prop_df["GUN_SCORE"].min())
    prop_df["CRIME_DRUG"] = (prop_df["DRUG_SCORE"] - prop_df["DRUG_SCORE"].min()) / (prop_df["DRUG_SCORE"].max() - prop_df["DRUG_SCORE"].min())
    prop_df["CRIME_MURDER"] = (prop_df["MURDER_SCORE"] - prop_df["MURDER_SCORE"].min()) / (prop_df["MURDER_SCORE"].max() - prop_df["MURDER_SCORE"].min())
    prop_df["CRIME_THEFT"] = (prop_df["THEFT_SCORE"] - prop_df["THEFT_SCORE"].min()) / (prop_df["THEFT_SCORE"].max() - prop_df["THEFT_SCORE"].min())
    prop_df["CRIME_HUMAN"] = (prop_df["HUMAN_SCORE"] - prop_df["HUMAN_SCORE"].min()) / (prop_df["HUMAN_SCORE"].max() - prop_df["HUMAN_SCORE"].min())
    prop_df["CRIME_OTHER"] = (prop_df["OTHER_SCORE"] - prop_df["OTHER_SCORE"].min()) / (prop_df["OTHER_SCORE"].max() - prop_df["OTHER_SCORE"].min())

    # Write the new cleaned dataset to directory
    output_file_path = "output/final_data.csv"
    prop_df.to_csv(output_file_path, index=False)








