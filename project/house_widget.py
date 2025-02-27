
#from subprocess import Popen, check_call 
#import os 
import pandas as pd
import numpy as np
import math 
import PySimpleGUI as sg
import webbrowser

import os 
os.getcwd()
os.chdir('G:\\My Drive\\python\\housingSearchApp\\project')
os.getcwd()

# Read Data
csv_path1 = "output/final_data.csv"
#csv_path1 = "output/training.csv"
prop_df = pd.read_csv(csv_path1)
n = prop_df.shape[0]
prop_df.sort_values(by=["PRICE"],ascending=True,inplace=True)
prop_df.index = range(len(prop_df.index))
prop_df_old = prop_df.copy()

# Read Languages
csvLanguage = "data_sets/languages_spoken.csv"
lang_df = pd.read_csv(csvLanguage)
languages = [lang for lang in lang_df.columns.tolist() if lang not in ["Community Area","Community Area Name","PREDOMINANT NON-ENGLISH LANGUAGE (%)","TOTAL"]]
languages.sort() 
# Add locations 
local = prop_df["LOCATION"].unique().tolist()
local.sort() 
local = ["NONE"] + local 

sg.theme('BluePurple')

# House Fact Column 
col_fact = [ 
        [sg.Text('Address:',size=(12,1)),sg.Text(size=(23,1), key='address')],
        [sg.Text('Location:',size=(12,1)),sg.Text(size=(23,1), key='location')],
        [sg.Text('Price:',size=(12,1)),sg.Text(size=(23,1),key='price')],
        [sg.Text('HOA:',size=(12,1)),sg.Text(size=(23,1),key='hoa')],
        [sg.Text('Year Built:',size=(12,1)),sg.Text(size=(23,1),key='year')]
]   
col_fact2 = [ 
        [sg.Text('# of Beds:',size=(12,1)),sg.Text(size=(10,1),key='beds')],
        [sg.Text('# of Bathrooms:',size=(12,1)),sg.Text(size=(10,1),key='baths')],
        [sg.Text('Sold Date:',size=(12,1)),sg.Text(size=(10,1),key='soldDT')],
        [sg.Text('Sold Price:',size=(12,1)),sg.Text(size=(10,1),key='soldP')],
        [sg.Text('SquareFeet:',size=(12,1)),sg.Text(size=(10,1), key='sqft')]
]
col_fact3 = [   
        [sg.Text('Tax Year:',size=(12,1)),sg.Text(size=(10,1),key='taxYear')],
        [sg.Text('Tax Assessed:',size=(12,1)),sg.Text(size=(10,1),key='assessTax')],
        [sg.Text('Zestimate:',size=(12,1)),sg.Text(size=(10,1),key='zest')],
        [sg.Text('Est Tax:',size=(12,1)),sg.Text(size=(10,1),key='estTax')],
        [sg.Text('Property Type:',size=(12,1)),sg.Text(size=(10,1),key="propType")]
]
# Commute Column 
col_commute1 = [
        [sg.Text('Commute Time:',pad=(5,2),size=(12,1)),sg.Text(pad=(5,2),size=(6,1),key='kommute')],
        [sg.Text('# of Transfers:',pad=(5,2),size=(12,1)),sg.Text(pad=(5,2),size=(6,1),key='kommuteTransfers')],
        [sg.Text('Walking Time:',pad=(5,2),size=(12,1)),sg.Text(pad=(5,2),size=(6,1),key='kommuteWalk')],
        [sg.Listbox(values=[],pad=(5,2),size=(20,4),key='kommuteSteps')]
] 
# Grocery Column 
col_grocery = [
         [sg.Listbox(values=[],pad=(5,5),size=(38,8),key='storeDrive')]
]
# Crime Column 
col_crime = [ 
        [sg.Text('GUN',size=(8,1)),sg.Text(size=(7,1),key='crimeGun')],
        [sg.Text('MURDER',size=(8,1)),sg.Text(size=(7,1),key='crimeMurder')],
        [sg.Text('DRUG',size=(8,1)),sg.Text(size=(7,1),key='crimeDrug')],
        [sg.Text('HUMAN',size=(8,1)),sg.Text(size=(7,1),key='crimeHuman')],
        [sg.Text('THEFT',size=(8,1)),sg.Text(size=(7,1),key='crimeTheft')],
        [sg.Text('OTHER',size=(8,1)),sg.Text(size=(7,1),key='crimeOther')]
]
# SocioEconomic Column
col_socio = [
        [sg.Text('% aged 25+ without HS diploma',size=(25,1)),sg.Text(size=(8,1),key='hsDiploma')],
        [sg.Text('% households below poverty',size=(25,1)),sg.Text(size=(8,1),key='homePoverty')],
        [sg.Text('% housing crowded',size=(25,1)),sg.Text(size=(8,1),key='homeCrowded')],
        [sg.Text('% aged 16+ unemployed',size=(25,1)),sg.Text(size=(8,1),key='unemployed')],
        [sg.Text('% aged under 18 or over 64',size=(25,1)),sg.Text(size=(8,1),key='aged')],
        [sg.Text('Per capita income',size=(25,1)),sg.Text(size=(8,1),key='income')]
]
# Language Column
col_language = [
        [sg.InputCombo(tuple(languages), key='lang1', default_value="CHINESE", enable_events=True,size=(10, 1)),
        sg.Text("",size=(8,1),key="perLang1")],
        [sg.InputCombo(tuple(languages), key='lang2', default_value="SPANISH", enable_events=True,size=(10, 1)),
        sg.Text("",size=(8,1),key="perLang2")],
        [sg.InputCombo(tuple(languages), key='lang3', default_value="POLISH", enable_events=True,size=(10, 1)),
        sg.Text("",size=(8,1),key="perLang3")],
        [sg.InputCombo(tuple(languages), key='lang4', default_value="RUSSIAN", enable_events=True,size=(10, 1)),
        sg.Text("",size=(8,1),key="perLang4")],
        [sg.InputCombo(tuple(languages), key='lang5', default_value="AFRICAN LANGUAGES", enable_events=True,size=(10, 1)),
        sg.Text("",size=(8,1),key="perLang5")],
        [sg.InputCombo(tuple(languages), key='lang6', default_value="GREEK", enable_events=True,size=(10, 1)),
        sg.Text("",size=(8,1),key="perLang6")]
]
# Affordable Rent Column
col_affordable = [
    [sg.Text("# of",size=(4,1)),sg.Text(size=(14,1),key="affordNum")],
    [sg.Text("type",size=(4,1)),sg.Listbox(values=[],size=(14,7),key="affordType")] 
]

# Button Column 
col_button = [
         [sg.Text(' ' * 25), sg.Button('',image_filename="images/thumbsDown.png",image_size=(100,100),image_subsample=5,border_width=0,key="dislike"),sg.Text(' ' * 25),
          sg.Button('',image_filename="images/unsure.png",image_size=(100,100),image_subsample=3,border_width=0,key="unsure"),sg.Text(' ' * 25),
          sg.Button('',image_filename="images/thumbsUp.png",image_size=(100,100),image_subsample=5,border_width=0,key="like") ]
]
# Score Column 
col_score = [
                [sg.Text("Your Rating: ",size=(15,1)),sg.Text(size=(10,1),key="rate")],
                [sg.Text("Predicted Score: ",size=(15,1)),sg.Text(size=(10,1),key="score")]
]
# RedFin and Zillow Link Column
col_website = [
    [sg.Button("Redfin Link",key="-redfin-"),
    sg.Button("Zillow Link",key="-zillow-")]
]

layout = [[sg.Text('Is this house Hot or Not?',font=('Helvetica', 20)),
          sg.Frame(layout=[[sg.Text('User Select: '),sg.InputCombo(('MM','XY'),size=(10,1),key='user',default_value='MM',enable_events=True)]],title="SELECT USER",title_color="blue"),
           sg.Frame(layout=[[sg.Text("View Select: "),sg.InputCombo(('ALL','UNRATED', 'RATED'), key='userRated', default_value="ALL", enable_events=True,size=(20, 1))]],
           title="RATING VIEW",title_color="blue"),
           sg.Text(" "*5),sg.Column(col_score,background_color="red")], 
          [sg.Text('Filter by: '),
          sg.InputCombo(local,key='filter', default_value="NONE", enable_events=True,size=(20, 1)),
          sg.Text('Sort by: '),
                sg.InputCombo(('ADDRESS','COMMUTE_TIME','WALKING_TIME', 'PRICE','XY_RATING','MM_RATING','PROPERTY_TYPE'), key='sortBy', default_value="PRICE", enable_events=True,size=(20, 1)), 
                sg.Radio("Ascending",group_id="radio1",key="ascend",default=True,enable_events=True),
                            sg.Radio("Descending",group_id="radio1",key="descend",enable_events=True),
                sg.Text(" "*5),sg.Column(col_website)],
          [sg.Frame(layout = [[sg.Listbox(values=prop_df["ADDRESS"],
                      size=(22, 7), key='-home-', enable_events=True)]],title="Home Selection:",title_color="blue"),
                      sg.Frame(layout = [[sg.Column(col_fact,background_color="grey"),
                      sg.Column(col_fact2,background_color="grey"),sg.Column(col_fact3,background_color="grey")]],title="General Information:",title_color="blue"),
                      sg.Frame(layout = [[sg.Column(col_language,background_color="orange")]],title="Language Spoken (%)",title_color="blue") 
                       ],
            [
                sg.Frame(layout = [[sg.Column(col_commute1,background_color="purple")]],title="Commute Information:",title_color="blue") , 
                    sg.Frame(layout = [[sg.Column(col_grocery,background_color="blue")]],title="Grocery Information:",title_color="blue") , 
                    sg.Frame(layout = [[sg.Column(col_affordable,background_color="yellow")]],title="Affordable Rentals",title_color="blue"),
                    sg.Frame(layout = [[sg.Column(col_socio,background_color="magenta")]],title="Socioeconomic Statistics:",title_color="blue") , 
                    sg.Frame(layout = [[sg.Column(col_crime,background_color="green")]],title="Crime Statistics:",title_color="blue")
            ],
          [sg.Column(col_button,justification="left")]
          ]
print(sg.Window.get_screen_size()) 
window = sg.Window('Housing Dating App', layout, resizable=True, size=sg.Window.get_screen_size())

while True:  # Event Loop

    event, values = window.read()
    print(event, values)
    print("EVENT: ", event)
    print("VALUE: ", values) 

    if event in ["-home-"]: 
        print(values["-home-"][0])
        i = prop_df["ADDRESS"].tolist().index(values["-home-"][0])

    if event in [None]:
        break
    
    if event in ['sortBy','ascend','descend']:
        print("ITEM1: ",values['sortBy'])
        prop_df.sort_values(by=[values['sortBy']],ascending=values['ascend'],inplace=True)
        prop_df.index = range(len(prop_df.index)) 
        window.Element("-home-").Update(prop_df["ADDRESS"])

    if event in ['filter','userRated','user']:
        print("ITEM1: ",values['filter'])
        print("ITEM2: ",values['userRated']) 
        if values['filter'] in ["NONE"]:
            if values['userRated'] in ['ALL']:
                prop_df = prop_df_old.copy()
                prop_df.sort_values(by=[values['sortBy']],ascending=values['ascend'],inplace=True)
                prop_df.index = range(len(prop_df.index)) 
                window.Element("-home-").Update(prop_df["ADDRESS"])
                n = prop_df.shape[0]
            elif values['userRated'] in ['UNRATED']:
                prop_df = prop_df_old.loc[pd.isnull(prop_df_old[values['user']+"_RATING"])].copy()
                prop_df.sort_values(by=[values['sortBy']],ascending=values['ascend'],inplace=True)
                prop_df.index = range(len(prop_df.index)) 
                window.Element("-home-").Update(prop_df["ADDRESS"])
                n = prop_df.shape[0]
            elif values['userRated'] in ['RATED']:
                prop_df = prop_df_old.loc[pd.notnull(prop_df_old[values['user']+"_RATING"])].copy()
                prop_df.sort_values(by=[values['sortBy']],ascending=values['ascend'],inplace=True)
                prop_df.index = range(len(prop_df.index)) 
                window.Element("-home-").Update(prop_df["ADDRESS"])
                n = prop_df.shape[0]
        else: 
            if values['userRated'] in ['ALL']:
                prop_df = prop_df_old.loc[prop_df_old["LOCATION"] == values["filter"]].copy()
                prop_df.sort_values(by=[values['sortBy']],ascending=values['ascend'],inplace=True)
                prop_df.index = range(len(prop_df.index)) 
                window.Element("-home-").Update(prop_df["ADDRESS"])
                n = prop_df.shape[0]
            elif values['userRated'] in ['UNRATED']:
                prop_df = prop_df_old.loc[(prop_df_old["LOCATION"] == values["filter"]) & (pd.isnull(prop_df_old[values['user']+"_RATING"]))].copy()
                prop_df.sort_values(by=[values['sortBy']],ascending=values['ascend'],inplace=True)
                prop_df.index = range(len(prop_df.index)) 
                window.Element("-home-").Update(prop_df["ADDRESS"])
                n = prop_df.shape[0]
            elif values['userRated'] in ['RATED']:
                prop_df = prop_df_old.loc[(prop_df_old["LOCATION"] == values["filter"]) & (pd.notnull(prop_df_old[values['user']+"_RATING"]))].copy()
                prop_df.sort_values(by=[values['sortBy']],ascending=values['ascend'],inplace=True)
                prop_df.index = range(len(prop_df.index)) 
                window.Element("-home-").Update(prop_df["ADDRESS"])
                n = prop_df.shape[0]

    if event in ["lang1"]:
        window['perLang1'].update(str(f'{prop_df[values["lang1"]][i]/prop_df["TOTAL"][i]:.2%}'))
    if event in ["lang2"]:
        window['perLang2'].update(str(f'{prop_df[values["lang2"]][i]/prop_df["TOTAL"][i]:.2%}'))
    if event in ["lang3"]:
        window['perLang3'].update(str(f'{prop_df[values["lang3"]][i]/prop_df["TOTAL"][i]:.2%}'))
    if event in ["lang4"]:
        window['perLang4'].update(str(f'{prop_df[values["lang4"]][i]/prop_df["TOTAL"][i]:.2%}'))
    if event in ["lang5"]:
        window['perLang5'].update(str(f'{prop_df[values["lang5"]][i]/prop_df["TOTAL"][i]:.2%}'))
    if event in ["lang6"]:
        window['perLang6'].update(str(f'{prop_df[values["lang6"]][i]/prop_df["TOTAL"][i]:.2%}'))

    if event in ["-redfin-"] and values["-home-"] not in [None]:
        try:
            webbrowser.open(prop_df['URL'][i])
        except: 
            pass
    if event in ["-zillow-"] and values["-home-"] not in [None]:
        try:
            webbrowser.open(prop_df['ZILLOW_URL'][i])
        except:
            pass

    if event in ["-home-","like","unsure","dislike"]:
        if n > 0: 
            id = prop_df_old["ADDRESS"].tolist().index(prop_df["ADDRESS"][i])
            if event == "like":
                prop_df_old.at[id,values['user']+"_RATING"] = 3  
                if values['userRated'] in ['UNRATED']:
                    prop_df.drop(prop_df.index[i],inplace=True)
                    prop_df.index = range(len(prop_df.index)) 
                    n = prop_df.shape[0]
                    if i == n: 
                        i = n-1
                    window.Element("-home-").Update(prop_df["ADDRESS"])
                else:
                    prop_df.at[i,values['user']+"_RATING"] = 3
                    if i < n-1:
                        i += 1
            if event == "unsure":
                prop_df_old.at[id,values['user']+"_RATING"] = 2
                if values['userRated'] in ['UNRATED']:
                    prop_df.drop(prop_df.index[i],inplace=True)
                    prop_df.index = range(len(prop_df.index)) 
                    n = prop_df.shape[0]
                    if i == n: 
                        i = n-1
                    window.Element("-home-").Update(prop_df["ADDRESS"])
                else:
                    prop_df.at[i,values['user']+"_RATING"] = 2
                    if i < n-1:
                        i += 1
            if event == "dislike":
                prop_df_old.at[id,values['user']+"_RATING"] = 1
                if values['userRated'] in ['UNRATED']:
                    prop_df.drop(prop_df.index[i],inplace=True)
                    prop_df.index = range(len(prop_df.index)) 
                    n = prop_df.shape[0]
                    if i == n: 
                        i = n-1
                    window.Element("-home-").Update(prop_df["ADDRESS"])
                else:
                    prop_df.at[i,values['user']+"_RATING"] = 1
                    if i < n-1:
                        i += 1
            window.Element("-home-").update(set_to_index=i,scroll_to_index=max(0,i-3))

        if n > 0: 
            
            #webbrowser.open(prop_df['URL'][i])
            
            #call_url = prop_df['URL'][i] 
            #mycmd = r'start chrome /new-tab {}'.format(call_url)
            #try: 
            #    os.system("taskkill /F /IM chrome.exe") 
            #except: 
            #    pass 
            #p1 = Popen(mycmd,shell=True) 

            window['address'].update(prop_df['ADDRESS'][i])
            window['location'].update(prop_df['LOCATION'][i])
            if pd.isnull(prop_df['SQFT'][i]):
                window['sqft'].update("")
            else: 
                window['sqft'].update(math.floor(prop_df['SQFT'][i]))
            if pd.isnull(prop_df['YEAR'][i]):
                window['year'].update("")
            else:
                window['year'].update(prop_df['YEAR'][i])
            if pd.isnull(prop_df['LAST_SOLD_DATE'][i]):
                window['soldDT'].update("")
            else: 
                window['soldDT'].update(prop_df['LAST_SOLD_DATE'][i])
            if pd.isnull(prop_df["ZESTIMATE"][i]):
                window['zest'].update("$")
            else:
                window['zest'].update("$" + str(f'{math.floor(prop_df["ZESTIMATE"][i]):,}'))
            if pd.isnull(prop_df["LAST_SOLD_PRICE"][i]):
                    window['soldP'].update("$") 
            else: 
                    window['soldP'].update("$" + str(f'{math.floor(prop_df["LAST_SOLD_PRICE"][i]):,}'))
            if pd.isnull(prop_df["ESTIMATED_TAX"][i]):
                window['estTax'].update("$")
            else:
                window['estTax'].update("$" + str(f'{math.floor(prop_df["ESTIMATED_TAX"][i]):,}'))
            if pd.isnull(prop_df["LAST_TAX_ASSESSMENT"][i]): 
                window['assessTax'].update("$")
            else:
                window['assessTax'].update("$" + str(f'{math.floor(prop_df["LAST_TAX_ASSESSMENT"][i]):,}'))
            if pd.isnull(prop_df['LAST_TAX_YEAR'][i]):
                window['taxYear'].update("")
            else:
                window['taxYear'].update(math.floor(prop_df['LAST_TAX_YEAR'][i]))
            if pd.isnull(prop_df["PRICE"][i]):
                window['price'].update("$")
            else:
                window['price'].update("$" + str(f'{math.floor(prop_df["PRICE"][i]):,}'))
            window['beds'].update(int(prop_df["BEDS"][i]))
            window['baths'].update(prop_df["BATHS"][i])
            if pd.isnull(prop_df["HOA"][i]):
                window['hoa'].update("$")
            else: 
                window['hoa'].update("$" + str(f'{math.floor(prop_df["HOA"][i]):,}'))
            if pd.isnull(prop_df['COMMUTE_TIME'][i]):
                window['kommute'].update("")
            else:
                window['kommute'].update(str(math.floor(prop_df['COMMUTE_TIME'][i])) + " min")
            if pd.isnull(prop_df['COMMUTE_STEPS'][i]):
                window['kommuteSteps'].update("")
            else:
                window['kommuteSteps'].update(prop_df['COMMUTE_STEPS'][i].split(","))
            if pd.isnull(prop_df['COMMUTE_NUM_STEPS'][i]):
                window['kommuteTransfers'].update("")
            else:
                window['kommuteTransfers'].update(prop_df['COMMUTE_NUM_STEPS'][i])
            if pd.isnull(prop_df['WALKING_TIME'][i]):
                window['kommuteWalk'].update("")
            else: 
                window['kommuteWalk'].update(str(math.floor(prop_df['WALKING_TIME'][i])) + " min")
            if pd.isnull(prop_df['AFFORDABLE_NUM'][i]):
                window['affordNum'].update("")
            else:
                window['affordNum'].update(int(prop_df['AFFORDABLE_NUM'][i]))
            if pd.isnull(prop_df['AFFORDABLE_DESC'][i]):
                window['affordType'].update("")
            else:    
                window['affordType'].update(list(dict.fromkeys(prop_df['AFFORDABLE_DESC'][i].split(","))))

            #if pd.isnull(prop_df['GROCERY_WALK'][i]):
            #    window['storeWalk'].update("")
            #else: 
            #    window['storeWalk'].update(prop_df['GROCERY_WALK'][i].split(","))
            if pd.isnull(prop_df['GROCERY_DRIVE'][i]):
                window['storeDrive'].update("")
            else:
                window['storeDrive'].update(prop_df['GROCERY_DRIVE'][i].split(","))
            window['crimeDrug'].update(str(f'{prop_df["CRIME_DRUG"][i]:.2%}')) 
            window['crimeGun'].update(str(f'{prop_df["CRIME_GUN"][i]:.2%}')) 
            window['crimeHuman'].update(str(f'{prop_df["CRIME_HUMAN"][i]:.2%}')) 
            window['crimeMurder'].update(str(f'{prop_df["CRIME_MURDER"][i]:.2%}')) 
            window['crimeOther'].update(str(f'{prop_df["CRIME_OTHER"][i]:.2%}')) 
            window['crimeTheft'].update(str(f'{prop_df["CRIME_THEFT"][i]:.2%}')) 
            if pd.isnull(prop_df[values['user']+"_RATING"][i]):
                window['rate'].update("UNRATED") 
            else:
                if prop_df[values['user']+"_RATING"][i] == 1:
                    window['rate'].update("Dislike")
                elif prop_df[values['user']+"_RATING"][i] == 2: 
                    window['rate'].update("Unsure") 
                elif prop_df[values['user']+"_RATING"][i] == 3: 
                    window['rate'].update("Like") 
                #window['rate'].update(prop_df[values['user']+"_RATING"][i])
            window['score'].update(prop_df['SCORE'][i])
            if pd.isnull(prop_df["PERCENT AGED 25+ WITHOUT HIGH SCHOOL DIPLOMA"][i]):
                window['hsDiploma'].update("") 
            else:
                window['hsDiploma'].update(str(prop_df["PERCENT AGED 25+ WITHOUT HIGH SCHOOL DIPLOMA"][i])+"%")
            if pd.isnull(prop_df["PERCENT HOUSEHOLDS BELOW POVERTY"][i]):
                window['homePoverty'].update("") 
            else:
                window['homePoverty'].update(str(prop_df["PERCENT HOUSEHOLDS BELOW POVERTY"][i])+"%")
            if pd.isnull(prop_df["PERCENT OF HOUSING CROWDED"][i]):
                window['homeCrowded'].update("") 
            else:
                window['homeCrowded'].update(str(prop_df["PERCENT OF HOUSING CROWDED"][i])+"%")
            if pd.isnull(prop_df["PERCENT AGED 16+ UNEMPLOYED"][i]):
                window['unemployed'].update("") 
            else:
                window['unemployed'].update(str(prop_df["PERCENT AGED 16+ UNEMPLOYED"][i])+"%")
            if pd.isnull(prop_df["PERCENT AGED UNDER 18 OR OVER 64"][i]):
                window['aged'].update("") 
            else:
                window['aged'].update(str(prop_df["PERCENT AGED UNDER 18 OR OVER 64"][i])+"%")
            if pd.isnull(prop_df["PER CAPITA INCOME "][i]):
                window['income'].update("") 
            else:
                window['income'].update("$"+str(f'{math.floor(prop_df["PER CAPITA INCOME "][i]):,}'))
            window['perLang1'].update(str(f'{prop_df[values["lang1"]][i]/prop_df["TOTAL"][i]:.2%}'))
            window['perLang2'].update(str(f'{prop_df[values["lang2"]][i]/prop_df["TOTAL"][i]:.2%}'))
            window['perLang3'].update(str(f'{prop_df[values["lang3"]][i]/prop_df["TOTAL"][i]:.2%}'))
            window['perLang4'].update(str(f'{prop_df[values["lang4"]][i]/prop_df["TOTAL"][i]:.2%}'))
            window['perLang5'].update(str(f'{prop_df[values["lang5"]][i]/prop_df["TOTAL"][i]:.2%}'))
            window['perLang6'].update(str(f'{prop_df[values["lang6"]][i]/prop_df["TOTAL"][i]:.2%}'))
            window['propType'].update(prop_df["PROPERTY_TYPE"][i])
window.close()

# Write the new cleaned dataset to directory
csv2_path = "output/final_data.csv"
prop_df_old.to_csv(csv2_path,index=False)

