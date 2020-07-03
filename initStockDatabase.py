import sqlite3
conn = sqlite3.connect('stocks.db')

conn.execute('''CREATE TABLE stocks
             (date text, symbol text, adjClose real, PRIMARY KEY(date, symbol))''')

conn.commit()

for row in conn.execute('SELECT * FROM stocks'):
        print(row)

conn.execute('''CREATE TABLE marketCaps
             (symbol text, marketCap real, PRIMARY KEY(symbol))''')

conn.commit()

for row in conn.execute('SELECT * FROM marketCaps'):
        print(row)

conn.close()
