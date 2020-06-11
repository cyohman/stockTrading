import os
from datetime import date
from datetime import datetime
import sqlite3
from pathlib import Path
import operator
import csv
import sys

local_Minimum_Date = date(2020, 3, 23)
path=os.getcwd()

#2020.05.12, cey, Add the hour, minute, and second to the folder in 24 hour time
savePath = path+"/"+datetime.now().strftime("%m-%d-%Y_%H%M%S")+"/";
os.mkdir(savePath);
print("The save root directory is %s" % savePath)
savePath = savePath+"percentageChanges/";
os.mkdir(savePath);
print ("The save directory is %s" % savePath)


with open('symbols', 'r', newline='') as symbolsFile:
    symbols = symbolsFile.read().splitlines()

symbols = sorted(symbols, key=str.upper)

#2020.05.01, cey, Remove the duplicate symbols
symbols = list(dict.fromkeys(symbols))

#2020.05.02, cey, Output the symbols to the original list
os.rename('symbols', 'old_symbol_lists/symbols_'+datetime.now().strftime("%m-%d-%Y_%H:%M%S"))

newSymbolsFile=open('symbols','w')

for element in symbols:
     newSymbolsFile.write(element)
     newSymbolsFile.write('\n')

newSymbolsFile.close()

conn = sqlite3.connect('stocks.db')

conn.execute('''CREATE TABLE percentageChanges
             (dayDelta int, date text,  symbol text, percentageChange real, PRIMARY KEY(dayDelta, symbol))''')

for symbol in symbols:
	
	print(symbol)

	cur = conn.execute('SELECT * FROM stocks WHERE symbol=:symbol order by date DESC', {"symbol": symbol})
	rows = cur.fetchall()
	print(rows)
	print(len(rows))

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

	        percentageChange = priceDelta / row[2]
	        print(percentageChange)

	        entry = [delta.days, date, symbol, percentageChange]

	        cur = conn.cursor()
	        cur.execute('INSERT INTO percentageChanges VALUES(?,?,?,?)',entry)
	        conn.commit()

		#if delta.days-1<55*7:
		#	percentageChanges[delta.days-1].append((symbol, percentageChange))
		        	

	        #finalSavePath = savePath+str(delta.days).zfill(3)+"-"+str(date)+".csv"
	        #print(finalSavePath)

	        #Path(savePath).touch()	       
                
	        #if os.path.exists(savePath):
                #   append_write = 'a' # append if already exists
	        #else:
                #   append_write = 'w' # make a new file if not
	
	        #print(append_write)
	        
	        #with open(finalSavePath, append_write) as percentageGainFile:
	        #   percentageGainFile.write(symbol+","+str(percentageChange)+"\n")
	        #   percentageGainFile.close()

cur = conn.execute('SELECT DISTINCT dayDelta FROM percentageChanges')
rows = cur.fetchall()
print(rows)
print(len(rows))

for row in rows:
	cur = conn.execute('SELECT date, symbol, percentageChange FROM percentageChanges WHERE dayDelta=:dayDelta ORDER BY percentageChange DESC', {"dayDelta": row[0]})
	rows2 = cur.fetchall()
	finalSavePath = savePath+str(row[0]).zfill(3)+"-"+str(rows2[0][0])+".csv"
	print(finalSavePath)
	
	with open(finalSavePath, 'w') as percentageGainFile:
                for row2 in rows2:
	                 percentageGainFile.write(row2[1]+","+str(row2[2])+"\n")
        
	percentageGainFile.close()

conn.execute('''DROP TABLE percentageChanges''')

#print(percentageChanges)

#lengthOfPercentageChanges = length(percentageChagnes)
#days=percentagesChanges[0:lengthOfPercentagesChanges-2]

#i = 0

#for day in days:
#	day.sort(key=lambda x:x[1])
#	for symbol in day:
#		finalSavePath = savePath+str(i).zfill(3)+"-"+str(date)+".csv"		

#directory = os.fsencode(savePath)

#for file in os.listdir(directory):
#     filename = os.fsdecode(file)
#     fullFilePath=os.path.join(directory, filename)
#     print(fullFilePath)
#     reader = csv.reader(open(fullFilePath), delimiter=",")
#     sortedlist = sorted(reader, key=operator.itemgetter(1), reverse=True)
#     print(sortedList)
