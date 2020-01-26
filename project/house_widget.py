
import pandas as pd
import numpy as np
import PySimpleGUI as sg
import webbrowser
#import googlemaps
#from datetime import datetime

# Google API
#API = 

# Initialize Google API
#gmaps = googlemaps.Client(key = API)  # Up to 40,000 calls per month
#now = datetime.now()
#A = now.replace(hour=8,minute=30)

# Read Data
csv_path1 = "output/commute_grocery_zillow_data.csv"
prop_df = pd.read_csv(csv_path1)
n = prop_df.shape[0]

sg.theme('BluePurple')

layout = [[sg.Text('Is this house Hot or Not?')],
          [sg.Button('Show Me The Next House / SKIP'), sg.Button('Exit')],
         # [sg.Text('Commute Address:'),sg.InputText(key='commute'),sg.Button('Get Commute Info')],
          [sg.Text('Address:',size=(10,1)),sg.Text(size=(35,1), key='address')],
          [sg.Text('Price:',size=(10,1)),sg.Text(size=(8,1),key='price'),sg.Text('HOA per month:',size=(15,1)),sg.Text(size=(6,1),key='hoa')],
          [sg.Text('# of Beds:',size=(10,1)),sg.Text(size=(8,1),key='beds'),sg.Text('# of Bathrooms:',size=(15,1)),sg.Text(size=(6,1),key='baths')],
          [sg.Text('Commute Time:',size=(25,1)),sg.Text(size=(6,1),key='kommute')],
          [sg.Text('Commute Steps:',size=(25,1)),sg.Text(size=(50,1),key='kommuteSteps')],
          [sg.Text('Grocery Stores (walking):',size=(25,1)),sg.Text(size=(50,1),key='storeWalk')],
        #  [sg.Text('Most Frequent Crime:',size=(25,1)),sg.Text(size=(50,1),key='crime')],
          [sg.Button('Hate this house!'), sg.Button('Unsure.'), sg.Button('Love this house!')]]

window = sg.Window('Housing Dating App', layout)
i = 0
#prop_df['RATING'] = np.nan
#prop_df['COMMUTE'] = ""
while True:  # Event Loop

    event, values = window.read()
    print(event, values)

    if event in ('Exit'):
        break
    if event == 'Love this house!':
        print("Smashing House!")
        prop_df.at[i-1,'RATING'] = 3
    if event == "Unsure.":
        print("Not sure...")
        prop_df.at[i-1,'RATING'] = 2
    if event == "Hate this house!":
        print("Leave ME ALONE!")
        prop_df.at[i-1,'RATING'] = 1
    if event == 'Show Me The Next House / SKIP':
        print("Not in your life PAL")

    #if event == 'Get Commute Info':
    #    home = prop_df['ADDRESS'][i-1] + prop_df['CITY'][i-1]
    #    print("VALUES: " + str(values['commute']))
    #    directions_result = gmaps.directions(
    #        home,
    #        values['commute'],
    #        mode="transit",
    #        arrival_time=A
    #    )
    #    prop_df.at[i-1,'COMMUTE'] = directions_result[0]['legs'][0]['duration']['text']
    #    window['kommute'].update(prop_df['COMMUTE'][i-1])
    #else:
    webbrowser.open(prop_df['URL'][i])
    window['address'].update(prop_df['ADDRESS'][i])
    window['price'].update("$" + str(f'{prop_df["PRICE"][i]:,}'))
    window['beds'].update(prop_df["BEDS"][i])
    window['baths'].update(prop_df["BATHS"][i])
    window['hoa'].update("$" + str(f'{prop_df["HOA PER MONTH"][i]:,}'))
    window['kommute'].update(prop_df['COMMUTE'][i])
    window['kommuteSteps'].update(prop_df['COMMUTE_STEPS'][i])
    window['storeWalk'].update(prop_df['GROCERY_walking'][i])
   # window['crime'].update(prop_df['top5crime'][i])

    i += 1

    if i == n:
        break

window.close()

# Write the new cleaned dataset to directory
csv2_path = "output/temp2.csv"
prop_df.to_csv(csv2_path,index=False)

