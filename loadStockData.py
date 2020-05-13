import os
import pandas_datareader as pdr
import pandas as pd
from datetime import datetime
from datetime import date, timedelta
import csv
import sqlite3
from dateutil.relativedelta import relativedelta

local_Minimum_Date = date(2020, 3, 23)

with open('symbols', 'r', newline='') as symbolsFile:
    symbols = symbolsFile.read().splitlines()

symbols = sorted(symbols, key=str.upper)

#2020.05.01, cey, Remove the duplicate symbols
symbols = list(dict.fromkeys(symbols))

#2020.05.02, cey, Output the symbols to the original list
os.rename('symbols', 'old_symbol_lists/symbols_'+datetime.now().strftime("%m-%d-%Y_%H:%M:%S"))

newSymbolsFile=open('symbols','w')

for element in symbols:
     newSymbolsFile.write(element)
     newSymbolsFile.write('\n')

newSymbolsFile.close()

#2020.04.30, cey, Read in symbols, alphabetize, and remove duplicates

os.environ["TIINGO_API_KEY"]="e64599a94ac46e01331bbe02499e7fd8cb7b8e84"

conn = sqlite3.connect('stocks.db')

#2020.05.11, cey, Rewrite this so we are only calling tiingo when we need data
for symbol in symbols:

	oneYearAgo = date.today() - timedelta(365)
	print('Current Date :',date.today())
	print('365 days before Current Date :',oneYearAgo)

	df = pdr.get_data_tiingo(symbol, oneYearAgo, date.today(), api_key=os.getenv('TIINGO_API_KEY'))
	
	for row in df.index:
	       symbol = row[0]
	       date = row[1].date()
	       cur = conn.execute('SELECT COUNT(*) FROM stocks WHERE symbol=:symbol and date=:date', {"symbol": symbol, "date":  date})
	       
	       if (cur.fetchone()[0] > 0):
	          print("Entry found")
	       else:
	          print("No entry found")
	          print(row)
	          entry = [date, symbol, df.loc[row].close]
	          cur = conn.cursor() 
	          cur.execute('INSERT INTO stocks VALUES(?,?,?)',entry)
	          conn.commit()
