import sqlite3
conn = sqlite3.connect('stocks.db')

#conn.execute('''CREATE TABLE stocks
#             (date text, symbol text, adjClose real)''')

#conn.commit()

for row in conn.execute('SELECT * FROM stocks'):
        print(row)

conn.close()
