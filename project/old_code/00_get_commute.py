from datetime import datetime

import pandas as pd
import googlemaps


def get_data_from_google_api(work, csv1_path):

    """
    ##################################################################
    ###    This code generates public transportation to a location
    ###    using Google's Directions API.
    ###    _________________________________________________________
    ###    INPUT:    Redfin Raw Source Data
    ###              Google API (string)
    ###              Location (string)
    ###    OUTPUT:   Saved File
    ###################################################################
    """

    # Read in RedFin data
    prop_df = pd.read_csv(csv1_path)
    n = prop_df.shape[0]

    # Initialize Google API
    csvK_path = "delete/input.txt"
    file = open(csvK_path, "r")
    API = file.read()
    file.close()

    gmaps = googlemaps.Client(key=API)  # Up to 40,000 calls per month
    now = datetime.now()
    aTime = now.replace(hour=8, minute=30)

    # Add commute features
    for i in range(0, n):
        print("Percentage Complete: " + str(round((i+1)/n*100, 2)) + "%")
        home = prop_df['ADDRESS'][i] + " " + prop_df['CITY'][i]
        directions_result = gmaps.directions(
                    home,
                    work,
                    mode="transit",
                    arrival_time=aTime
                )
        if len(directions_result) != 0:
            # Number of Transfers (Steps)
            steps = len(directions_result[0]['legs'][0]['steps'])
            # Record the number of commute steps
            prop_df.at[i, 'COMMUTE_NUM_STEPS'] = steps

            total_time = directions_result[0]['legs'][0]['duration']['text']
            # Record the total commute time to work, arriving at 8:30AM
            prop_df.at[i, 'COMMUTE'] = total_time

            # Print All Steps
            STEPS = []
            walk_time = 0
            for step in range(steps):
                _temp = directions_result[0]['legs'][0]['steps'][step]
                if _temp['travel_mode'] == "WALKING":
                    STEPS.append(str(_temp['travel_mode']).upper() + "(" + str(_temp['duration']['text']).upper() + ")")
                    walk_time += int(directions_result[0]['legs'][0]['steps'][step]['duration']['text'].split(" ")[0])
                elif _temp['travel_mode'] == "TRANSIT":
                    try:
                        _temp1 = _temp['transit_details']['line']['vehicle']['type']
                        _temp2 = _temp['transit_details']['line']['short_name']
                        _temp3 = str(_temp1) + str(_temp2)

                    except:
                        _temp3 = _temp['transit_details']['line']['name']
                    STEPS.append(str(_temp3).upper() + "(" + str(_temp['duration']['text']) + ")")

            # Record all commute steps in a string
            prop_df.at[i, 'COMMUTE_STEPS'] = ', '.join(STEPS)
            # Record total walking time
            prop_df.at[i, 'WALKING_TIME'] = walk_time

    # Write the new cleaned dataset to directory
    output_file_path = "output/commute_data.csv"
    prop_df.to_csv(output_file_path, index=False)


if __name__ == '__main__':

    # Work Address
    work = "111 E Pearson St, Chicago, IL"

    # Read data from CSV files
    csv1_path = "data_sets/RedFin_raw_data.csv"

    get_data_from_google_api(work, csv1_path)



