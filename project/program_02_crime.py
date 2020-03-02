
import extra_programs as helper
import pandas as pd 
from math import exp 

def get_crime_features(redfinHome_LatLon, crimeSet):
    """
    ##################################################################
    ###    This code generates public transportation to a location
    ###    using Google's Directions API.
    ###    _________________________________________________________
    ###    INPUT:    redfinHome_LatLon - List of latitude / longitude
    ###              groceryList - Pandas DataFrame of grocery stores 
    ###    OUTPUT:   Dictionary
    ###################################################################
    """
    x1 = redfinHome_LatLon[0]
    y1 = redfinHome_LatLon[1]
    tempDistance = []
    for crm in range(crimeSet.shape[0]):
        x2 = crimeSet.Latitude[crm]
        y2 = crimeSet.Longitude[crm]
        d = helper.distanceGPS(x1,y1,x2,y2)
        tempDistance.append({"TYPE": crimeSet['Primary Type'][crm],
                                "DESCRIPTION": crimeSet['Description'][crm],
                                "DISTANCE": d})
    tempDistance = pd.DataFrame(tempDistance)
    # Restrict Crimes to 2 Miles
    tempDistance = tempDistance[tempDistance['DISTANCE'] < 2]
    tempDistance.index = range(tempDistance.shape[0])

    gunScore = 0
    drugScore = 0
    murderScore = 0
    theftScore = 0
    humanScore = 0
    otherScore = 0 
    for crm in range(len(tempDistance)): 
        if tempDistance.at[crm,"TYPE"] in ["WEAPONS VIOLATION","CONCEALED CARRY LICENSE VIOLATION"]:
            gunScore += 1 / exp(tempDistance.at[crm,"DISTANCE"]) 
        elif tempDistance.at[crm,"DESCRIPTION"] in ["HANDGUN","ARMOR","GUN","FIREARM","AMMO","AMMUNITION","RIFLE"]:
            gunScore += 1 / exp(tempDistance.at[crm,"DISTANCE"]) 
        if tempDistance.at[crm,"TYPE"] in ["NARCOTICS","OTHER NARCOTIC VIOLATION"]:
            drugScore += 1 / exp(tempDistance.at[crm,"DISTANCE"]) 
        if tempDistance.at[crm,"TYPE"] in ["HOMICIDE"]:
            murderScore += 1 / exp(tempDistance.at[crm,"DISTANCE"]) 
        if tempDistance.at[crm,"TYPE"] in ["BURGLARY","CRIM SEXUAL ASSAULT","ASSAULT","BATTERY","ROBBERY","MOTOR VEHICLE THEFT","THEFT"]:
            theftScore += 1 / exp(tempDistance.at[crm,"DISTANCE"]) 
        if tempDistance.at[crm,"TYPE"] in ["OFFENSE INVOLVING CHILDREN","SEX OFFENSE","OBSCENITY","KIDNAPPING","PROSTITUTION","HUMAN TRAFFICKING","PUBLIC INDECENCY","STALKING"]:
            humanScore += 1 / exp(tempDistance.at[crm,"DISTANCE"]) 
        if tempDistance.at[crm,"TYPE"] in ["DECEPTIVE PRACTICE","CRIMINAL DAMAGE","OTHER OFFENSE","INTIMIDATION","GAMBLING","CRIMINAL TRESPASS","PUBLIC PEACE VIOLATION",
            "ARSON","INTERFERENCE WITH PUBLIC OFFICER","LIQUOR LAW VIOLATION","NON-CRIMINAL"]:
            otherScore += 1 / exp(tempDistance.at[crm,"DISTANCE"]) 

    return( ({  "GUN_SCORE" : gunScore,
                "DRUG_SCORE" : drugScore,
                "MURDER_SCORE": murderScore,
                "THEFT_SCORE": theftScore,
                "HUMAN_SCORE": humanScore,
                "OTHER_SCORE": otherScore
                        }) )
