import sqlite3

state = input('what state?')

connection = sqlite3.connect(state+'.sqlite')
cursor = connection.cursor()
cursor.execute("""CREATE TABLE state1 
               (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL
                ,name TEXT NOT NULL)""")
connection.commit()
connection.close()