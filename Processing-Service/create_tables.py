import sqlite3
import datetime

conn = sqlite3.connect('stats.sqlite')

c = conn.cursor()
c.execute('''
    CREATE TABLE stats
    (id INTEGER PRIMARY KEY ASC,
    min_daily_steps INTEGER NOT NULL,
    min_calories_burned INTEGER NOT NULL,
    max_daily_steps INTEGER NOT NULL,
    max_calories_burned INTEGER,
    last_updated STRING(100) NOT NULL)
''')
conn.commit()
conn.close()