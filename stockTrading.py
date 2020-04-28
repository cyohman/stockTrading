import os
import pandas_datareader as pdr

os.environ["TIINGO_API_KEY"]="e64599a94ac46e01331bbe02499e7fd8cb7b8e84"
df = pdr.get_data_tiingo('GOOG', api_key=os.getenv('TIINGO_API_KEY'))
print(df.head())

