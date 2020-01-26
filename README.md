# The Chicago Housing Search Utility
This project is designed to save individuals countless hours by customizing your very own housing recommendation model. Data is sourced from [Redfin](https://www.redfin.com/), [Zillow's API](https://www.zillow.com/howto/api/APIOverview.htm), [Google Directions API](https://developers.google.com/maps/documentation/directions/start), [ARCGIS API](https://developers.arcgis.com/python/), and [Chicago's Data Portal](https://data.cityofchicago.org/). This project was created using python 3.7 64-bit.  

## Commute Features Available
Input raw RedFin search data into program called "get_commute.py". Inside the file "get_commute.py", you will need to specify your [Google API key](https://developers.google.com/maps/documentation/javascript/get-api-key) in order for the program to properly work. 
- Total commute time to specified address (public transit) 
- Total walking time to specified address (public transit) 
- Route path to specified address (ex. TRAIN - BUS - WALKING)
- Total number of transfers to specified address (public transit) 

## Grocery Store Features Available 
Input raw RedFin search data into program called "get_grocery.py". Some prerequisites would be the geocoordinates of your favorite grocery stores. The csv file called "illinois_ZIP.csv" contains all the zip codes in Illinois. Using the zip codes and for example "get_wholeFoods_data.py" use ARCGIS API to search through zip codes containing key words. This will return a dataset with all the geocoordinates of the grocery stores. 
- Number of grocery stores within 1/2 mile (walking distance) 
- List of grocery stores within 1/2 mile (walking distance) 
- Indicator if Aldi's, Jewel-Osco, Mariano's, Trader Joe's, or WholeFoods are within 1/2 mile (walking distance) 
- Number of grocery stores within 2 miles (driving distance) 
- List of grocery stores within 2 miles (driving distance) 
- Indicator if Aldi's, Jewel-Osco, Mariano's, Trader Joe's, or WholeFoods are within 2 miles (driving distance) 

## Zillow Features Available 
Input raw RedFin's address and zipcode into Zillow's API will get you several features. 
- Zillow ID
- Zillow URL
- Last Tax Year
- Last Tax Assessment Amount
- Estimated Yearly Tax (based on Cook County average tax rate 2.117%) 
- Last Sold Date
- Last Sold Price
- Zestimate 

## Tasks to Complete
- Text analysis on crime statistics
- Closest gun crime (distance) 
- Text analysis on census data
- Number of parks in a fixed range
- Closest park (distance)
- Liquor Stores and Tobacco Stores

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)
