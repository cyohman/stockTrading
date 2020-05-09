import os
import pandas_datareader as pdr
import pandas as pd
from datetime import datetime
from datetime import date
import csv
import sqlite3

local_Minimum_Date = date(2020, 3, 23)

print(local_Minimum_Date)

with open('symbols', 'r', newline='') as symbolsFile:
    symbols = symbolsFile.read().splitlines()

symbols = sorted(symbols, key=str.upper)

#2020.05.01, cey, Remove the duplicate symbols
symbols = list(dict.fromkeys(symbols))

#2020.05.02, cey, Output the symbols to the original list
os.rename('symbols', 'old_symbol_lists/symbols_'+datetime.now().strftime("%m-%d-%Y_%H:%M"))

newSymbolsFile=open('symbols','w')

for element in symbols:
     newSymbolsFile.write(element)
     newSymbolsFile.write('\n')

newSymbolsFile.close()

#2020.04.30, cey, Read in symbols, alphabetize, and remove duplicates

os.environ["TIINGO_API_KEY"]="e64599a94ac46e01331bbe02499e7fd8cb7b8e84"

conn = sqlite3.connect('stocks.db')

for symbol in symbols:
	df = pdr.get_data_tiingo(symbol, local_Minimum_Date, date.today(), api_key=os.getenv('TIINGO_API_KEY'))
	print(df.index)
	
	i = 0	

	for row in df.index:
	       print(i)
	       symbol = row[0]
	       print(symbol)
	       date = row[1].date()
	       print(date)
	       print(df.loc[row])
	       cur= conn.execute('SELECT COUNT(*) FROM stocks WHERE symbol=:symbol and date=:date', {"symbol": symbol, "date":  date})
	       if (cur.fetchone()[0] > 0):
	          print("Entry found")
	       else:
		  #print df[row]
	          print("No entry found")
	          #entry = [(date, symbol,
                  #conn.execute('INSERT INTO stocks value(?,?,?)', 

#2020.04.30, cey, Store data in database
