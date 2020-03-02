import pandas as pd

# Read data from CSV files
csv1_path = "output/commute_grocery_zillow_data.csv"

# Read in RedFin data
prop_df = pd.read_csv(csv1_path)
n = prop_df.shape[0]
print("Total Number of Homes: " + str(n) + "\n")

# Read in Crime Stats data (2019 - Present)
csv2_path = "data_sets/Crimes_-_2019.csv"
crime = pd.read_csv(csv2_path)
print(crime.head())
print(crime.shape)

crime.dropna(inplace=True)
crime.index = range(crime.shape[0])
print(crime.head())
print(crime.shape)

from math import sin, cos, sqrt, atan2, radians


def distanceGPS(lat1, lon1, lat2, lon2):
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
    return (R * c * 0.62137)

for home in range(n):
    print("House Number: " + str(home))
    x1 = prop_df.LATITUDE[home]
    y1 = prop_df.LONGITUDE[home]
    tempDistance = []
    for item in range(crime.shape[0]):
        x2 = crime.Latitude[item]
        y2 = crime.Longitude[item]
        d = distanceGPS(x1, y1, x2, y2)
        tempDistance.append({"TYPE": crime['Primary Type'][item],
                             "DESCRIPTION": crime['Description'][item],
                             "DISTANCE": d})
    tempDistance = pd.DataFrame(tempDistance)
    tempDistance.sort_values(by=['DISTANCE'], inplace=True)
    tempDistance['BLOCKS'] = tempDistance['DISTANCE'] * 8
    # Restrict Crimes to 2 Miles
    tempDistance = tempDistance[tempDistance['DISTANCE'] < 2]

    from collections import Counter

    def topKFrequent(nums, k):
        # nums=[1,1,1,2,2,3], k=2
        c = Counter(nums)  # Counter({1: 3, 2: 2, 3: 1})
        k_most_common = c.most_common(k)  # [(1, 3), (2, 2)]
        return [element for element, count in k_most_common]  # [1, 2]

    A = topKFrequent(tempDistance['TYPE'].tolist(), 5)
    B = topKFrequent(tempDistance['DESCRIPTION'],5)
    #print(A)
    #print(B)
    prop_df.at[home,'top5crime'] = ", ".join(A)

    list_ = tempDistance['TYPE'].tolist()
    li = [k for k in list_ if "THEFT" in k]
    print("Number of Theft: " + str(len(li)))
    prop_df.at[home,'theft_cnt'] = len(li)

    list_ = tempDistance['DESCRIPTION'].tolist()
    li = [k for k in list_ if "GUN" in k]
    print("Number of Gun Related Crime: " + str(len(li)))
    prop_df.at[home,'gun_cnt'] = len(li)

# Write the new cleaned dataset to directory
csv3_path = "output/temporary_data.csv"
prop_df.to_csv(csv3_path,index=False)


# Create a Crime Score 
# Rank order crimes and use frequency 
