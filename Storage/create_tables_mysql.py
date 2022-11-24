import mysql.connector
db_conn = mysql.connector.connect(host="acit3855-lab6.westus3.cloudapp.azure.com", user="root", password="password", database="events")

db_cursor = db_conn.cursor()

db_cursor.execute('''
        CREATE TABLE daily_steps
        (id INT NOT NULL AUTO_INCREMENT,
        client_name VARCHAR(250) NOT NULL,
        age INTEGER NOT NULL,
        daily_steps INTEGER NOT NULL,
        timestamp VARCHAR(100) NOT NULL,
        date_created VARCHAR(100) NOT NULL,
        trace_id VARCHAR(100) NOT NULL,
        CONSTRAINT daily_steps PRIMARY KEY (id))
        ''')
db_cursor.execute('''
        CREATE TABLE calories_burned
        (id INT NOT NULL AUTO_INCREMENT,
        client_name VARCHAR(250) NOT NULL,
        age INTEGER NOT NULL,
        calories_burned INTEGER NOT NULL,
        timestamp VARCHAR(100) NOT NULL,
        date_created VARCHAR(100) NOT NULL,
        trace_id VARCHAR(100) NOT NULL,
        CONSTRAINT calories_burned PRIMARY KEY (id))
''')
db_conn.commit()
db_conn.close()