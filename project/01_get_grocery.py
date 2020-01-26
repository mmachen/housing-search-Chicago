
import pandas as pd

# Read data from CSV files
csv1_path = "output/commute_data.csv"

# Read in RedFin data
prop_df = pd.read_csv(csv1_path)
n = prop_df.shape[0]
print("Total Number of Homes: " + str(n) + "\n")

# Read data from CSV files
csv2_path = "data_sets/aldi.csv"
ALDI = pd.read_csv(csv2_path)
ALDI['NAME'] = "ALDI"

csv2_path = "data_sets/jewelOsco.csv"
JEWEL = pd.read_csv(csv2_path)
JEWEL['NAME'] = "JEWEL"

csv2_path = "data_sets/mariano.csv"
MARIANO = pd.read_csv(csv2_path)
MARIANO['NAME'] = "MARIANO"

csv2_path = "data_sets/traderJoes.csv"
TJ = pd.read_csv(csv2_path)
TJ['NAME'] = "TRADERJOE"

csv2_path = "data_sets/wholeFoods.csv"
WHOLEFOODS = pd.read_csv(csv2_path)
WHOLEFOODS['NAME'] = "WHOLEFOODS"

GROCERY = pd.concat([ALDI,JEWEL,MARIANO,TJ,WHOLEFOODS],sort=False)
GROCERY.index = range(GROCERY.shape[0])
#print(GROCERY.at[0,'ADDRESS'])
#print(prop_df.at[0,'ADDRESS'])

from math import sin, cos, sqrt, atan2, radians
# Returns miles between two points
def distanceGPS(lat1,lon1,lat2,lon2):
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

prop_df['GROCERY_driving'] = ""
prop_df['GROCERY_walking'] = ""
for home in range(n):
    print("House Number: " + str(home))
    x1 = prop_df.LATITUDE[home]
    y1 = prop_df.LONGITUDE[home]
    tempDistance = []
    for store in range(GROCERY.shape[0]):
        x2 = GROCERY.LATITUDE[store]
        y2 = GROCERY.LONGITUDE[store]
        d = distanceGPS(x1,y1,x2,y2)
        tempDistance.append({"NAMES":GROCERY.NAME[store],
                             "DISTANCE":d })
    tempDistance = pd.DataFrame(tempDistance)
    #tempDistance.sort_values(by=['DISTANCE'],inplace=True)
    #tempDistance['BLOCKS'] = tempDistance['DISTANCE']*8

    closeSubset = tempDistance[tempDistance['DISTANCE'] <= 0.5]
    closeSubset = closeSubset['NAMES'].unique().tolist()
    #print("Grocery Stores in 1/2 Mile",end=" : ")
    #print(*closeSubset,sep=",")
    prop_df.at[home,'GROCERY_walking_num'] = len(closeSubset)
    prop_df.at[home,'GROCERY_walking'] = ', '.join(closeSubset)

    if "ALDI" in closeSubset:
        prop_df.at[home,'ALDI_walking'] = 1
    else:
        prop_df.at[home, 'ALDI_walking'] = 0

    if "JEWEL" in closeSubset:
        prop_df.at[home,'JEWEL_walking'] = 1
    else:
        prop_df.at[home, 'JEWEL_walking'] = 0

    if "MARIANO" in closeSubset:
        prop_df.at[home,'MARIANO_walking'] = 1
    else:
        prop_df.at[home, 'MARIANO_walking'] = 0

    if "TRADERJOE" in closeSubset:
        prop_df.at[home,'TRADERJOE_walking'] = 1
    else:
        prop_df.at[home, 'TRADERJOE_walking'] = 0

    if "WHOLEFOODS" in closeSubset:
        prop_df.at[home,'WHOLEFOODS_walking'] = 1
    else:
        prop_df.at[home, 'WHOLEFOODS_walking'] = 0

    fartherSubset = tempDistance[tempDistance['DISTANCE'] <= 2]
    fartherSubset = fartherSubset['NAMES'].unique().tolist()
    #print("Grocery Stores in 2 Miles",end=" : ")
    #print(*fartherSubset,sep=",")

    prop_df.at[home,'GROCERY_driving'] = len(fartherSubset)
    prop_df.at[home,'GROCERY_driving'] = ', '.join(fartherSubset)

    if "ALDI" in fartherSubset:
        prop_df.at[home, 'ALDI_driving'] = 1
    else:
        prop_df.at[home, 'ALDI_driving'] = 0

    if "JEWEL" in fartherSubset:
        prop_df.at[home, 'JEWEL_driving'] = 1
    else:
        prop_df.at[home, 'JEWEL_driving'] = 0

    if "MARIANO" in fartherSubset:
        prop_df.at[home, 'MARIANO_driving'] = 1
    else:
        prop_df.at[home, 'MARIANO_driving'] = 0

    if "TRADERJOE" in fartherSubset:
        prop_df.at[home, 'TRADERJOE_driving'] = 1
    else:
        prop_df.at[home, 'TRADERJOE_driving'] = 0

    if "WHOLEFOODS" in fartherSubset:
        prop_df.at[home, 'WHOLEFOODS_driving'] = 1
    else:
        prop_df.at[home, 'WHOLEFOODS_driving'] = 0

# Write the new cleaned dataset to directory
csv3_path = "output/commute_grocery_data.csv"
prop_df.to_csv(csv3_path,index=False)