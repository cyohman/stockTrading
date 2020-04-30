import os
import pandas_datareader as pdr
import pandas as pd
import datetime

local_Minimum_Date = datetime.datetime(2020, 3, 23)

print(local_Minimum_Date)

with open('symbols') as symbolsFile:
    symbols = symbolsFile.read().splitlines()

print(symbols)

os.environ["TIINGO_API_KEY"]="e64599a94ac46e01331bbe02499e7fd8cb7b8e84"
df = pdr.get_data_tiingo('GOOG', api_key=os.getenv('TIINGO_API_KEY'))
print(df.columns)
print(df.index)
print(df.head())

print (df.loc[('GOOG', '2020-04-28 00:00:00+00:00')]);

#today_df=df[df['date']=='2020-04-28 00:00:00+00:00']
#print(today_df.head())

#print(pdr.tiingo.get_tiingo_symbols())
