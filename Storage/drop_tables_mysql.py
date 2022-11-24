import mysql.connector

db_conn = mysql.connector.connect(host="acit3855-lab6.westus3.cloudapp.azure.com", user="root", password="password", database="events")

db_cursor = db_conn.cursor()

db_cursor.execute('''
DROP TABLE daily_steps, calories_burned
''')
db_conn.commit()
db_conn.close()