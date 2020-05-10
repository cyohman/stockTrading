import os
from datetime import date
from datetime import datetime
import sqlite3

local_Minimum_Date = date(2020, 3, 23)

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

conn = sqlite3.connect('stocks.db')

for symbol in symbols:
	cur = conn.execute('SELECT * FROM stocks WHERE symbol=:symbol order by date DESC', {"symbol": symbol})
	rows = cur.fetchall()

	currentDate=datetime.strptime(rows[0][0], "%Y-%m-%d").date()
	print(currentDate)
	currentPrice=rows[0][2]
	print(currentPrice)
	
	length = len(rows)
	print(length)	

	rows = rows[1:length-1]
	print(rows)	
	
	for row in rows:
        	print(row)
	        date=datetime.strptime(row[0], "%Y-%m-%d").date()
	        print(date)
	        
	        print(row[2])

	        delta = currentDate - date
	        print(delta.days)

	        priceDelta = currentPrice - row[2]
	        print(priceDelta)

	        percentageChange = priceDelta / currentPrice
	        print(percentageChange)
