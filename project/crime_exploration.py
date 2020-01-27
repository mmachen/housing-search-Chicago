
import pandas as pd

# Read in Crime Stats data (2019 - Present)
csv2_path = "data_sets/Crimes_-_2019.csv"
crime = pd.read_csv(csv2_path)
print(crime.head())
print(crime.shape)

crime.dropna(inplace=True)
crime.index = range(crime.shape[0])
print(crime.head())
print(crime.shape)

for item in range(len(crime)):