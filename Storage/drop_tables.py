import sqlite3

conn = sqlite3.connect('point.sqlite')

c = conn.cursor()
c.execute('''
          DROP TABLE daily_steps, calories_burned
          ''')

conn.commit()
conn.close()
