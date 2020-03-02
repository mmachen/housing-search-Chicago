import datetime
import googlemaps

def get_directions_from_google_api(redfinData_home, API_key, location_address):
    """
    ##################################################################
    ###    This code generates public transportation to a location
    ###    using Google's Directions API.
    ###    _________________________________________________________
    ###    INPUT:    redfinData_home - Redfin Raw Source Data
    ###              API_key - Google API (string)
    ###              location_address - Location (string)
    ###    OUTPUT:   Dictionary
    ###################################################################
    """
    # Load GoogleMaps API (Monday arrive at Work @8:30 AM)
    gmaps = googlemaps.Client(key=API_key)  # Up to 40,000 calls per month
    now = datetime.datetime.now()
    last_monday = now - datetime.timedelta(days=now.weekday())
    aTime = last_monday.replace(hour=8, minute=30)

    # Add commute features
    directions_result = gmaps.directions(
                redfinData_home,
                location_address,
                mode="transit",
                arrival_time=aTime
            )

    if len(directions_result) != 0:
        # Number of steps and total commute time
        steps = len(directions_result[0]['legs'][0]['steps'])
        total_time = directions_result[0]['legs'][0]['duration']['text']

        # Append all steps and record total walk time
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

        return( ({  "COMMUTE_NUM_STEPS": steps,
                    "COMMUTE_TIME": total_time,
                    "COMMUTE_STEPS": ', '.join(STEPS),
                    "WALKING_TIME": walk_time
                        }) )
    else: 
        return( ({  "COMMUTE_NUM_STEPS": float('nan'),
                    "COMMUTE_TIME": float('nan'),
                    "COMMUTE_STEPS": float('nan'),
                    "WALKING_TIME": float('nan') 
                        }) )
