import pandas as pd
from arcgis.gis import GIS
from arcgis.geocoding import geocode


# Read in zipCode data
prop_df = pd.read_csv("data_sets/illinois_ZIP.csv")

# Only view zip codes in Cook County
prop_df = prop_df[prop_df['County'] == "Cook"]
print("Number of rows is", len(prop_df))

# Find unique zip codes (219)
uniqueZip = prop_df['Zip Code'].unique()

n = len(uniqueZip)

# Print
print("Total number of rows:", n, "\n")

# Initialize List
listedList = []
# Initiate GIS service
gis = GIS()

# Loop through all zip codes in Cook County and save unique items with geocode
for id in range(n):
    yourZip = geocode(str(uniqueZip[id]))[0]
    searchedItem = geocode("ALDI", yourZip['extent'], max_locations=1000)
    print("ID - " + str(id), end=" : ")
    print("ZIPCODE - " + str(uniqueZip[id]), end=" : ")
    print("NUM - " + str(len(searchedItem)))
    for item2 in range(len(searchedItem)):
        listedList.append({"ADDRESS": searchedItem[item2]['attributes']['Place_addr'],
                            "PHONE": searchedItem[item2]['attributes']['Phone'],
                            "POSTAL": searchedItem[item2]['attributes']['Postal'],
                            "LONGITUDE": searchedItem[item2]['location']['x'],
                            "LATITUDE": searchedItem[item2]['location']['y']})

listedList = pd.DataFrame(listedList)
print(listedList)
print(len(listedList))
print(listedList.head())
print("\n")

print(listedList.shape)
# Find if there are duplicates (by ADDRESS)
dup_index = listedList.duplicated(["ADDRESS"])
prop_dup = listedList[dup_index]
print(prop_dup.shape)

listedList.drop_duplicates(subset=['ADDRESS'],inplace=True)
print(listedList.shape)

# Write the new cleaned dataset to directory
csv2_path = "data_sets/aldi.csv"
listedList.to_csv(csv2_path,index=False)

