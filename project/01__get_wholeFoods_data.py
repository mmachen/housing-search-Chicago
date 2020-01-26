import pandas as pd
from arcgis.gis import GIS
from arcgis.geocoding import geocode

# Read data from CSV files
csv1_path = "data_sets/illinois_ZIP.csv"

# Read in zipCode data
prop_df = pd.read_csv(csv1_path)
prop_df = pd.DataFrame(prop_df)

# Only view zip codes in Cook County
prop_df = prop_df[prop_df['County'] == "Cook"]
print("Number of rows is " + str(prop_df.shape[0]))

# Find unique zip codes (219)
uniqueZip = prop_df['Zip Code'].unique()

n = len(uniqueZip)

# Print
print("Total number of rows: " + str(n) + "\n")

# Initialize List
whole = []
# Initiate GIS service
gis = GIS()

# Loop through all zip codes in Cook County and save unique items with geocode
id = 1

for id in range(n):
    yourZip = geocode(str(uniqueZip[id]))[0]
    wholeFoods = geocode("Whole Foods", yourZip['extent'], max_locations=1000)
    print("ID - " + str(id), end=" : ")
    print("ZIPCODE - " + str(uniqueZip[id]), end=" : ")
    print("NUM - " + str(len(wholeFoods)))
    for item2 in range(len(wholeFoods)):
        whole.append({"ADDRESS":wholeFoods[item2]['attributes']['Place_addr'],
                      "PHONE": wholeFoods[item2]['attributes']['Phone'],
                      "POSTAL": wholeFoods[item2]['attributes']['Postal'],
                      "LONGITUDE":wholeFoods[item2]['location']['x'],
                      "LATITUDE":wholeFoods[item2]['location']['y']})

whole = pd.DataFrame(whole)
print(whole)
print(len(whole))
print(whole.head())
print("\n")

print(whole.shape)
# Find if there are duplicates (by ADDRESS)
dup_index = whole.duplicated(["ADDRESS"])
prop_dup = whole[dup_index]
print(prop_dup.shape)

whole.drop_duplicates(subset=['ADDRESS'],inplace=True)
print(whole.shape)

# Write the new cleaned dataset to directory
csv2_path = "data_sets/wholeFoods.csv"
whole.to_csv(csv2_path,index=False)

