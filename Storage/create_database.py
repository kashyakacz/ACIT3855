import sqlite3

conn = sqlite3.connect('readings.sqlite')

c = conn.cursor()
c.execute('''
          CREATE TABLE daily_steps
          (id INTEGER PRIMARY KEY ASC, 
           client_name VARCHAR(250) NOT NULL,
           age INTEGER NOT NULL,
           daily_steps INTEGER NOT NULL,
           timestamp VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL)
          ''')

c.execute('''
          CREATE TABLE calories_burned
          (id INTEGER PRIMARY KEY ASC, 
           client_name VARCHAR(250) NOT NULL,
           age INTEGER NOT NULL,
           calories_burned INTEGER NOT NULL,
           timestamp VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL)
          ''')

conn.commit()
conn.close()
