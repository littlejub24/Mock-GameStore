import psycopg2
from config import config  

# Function to get info from "database.ini" which is info like port number, username, password to succesfully connect to database
def connect():
    connection = None
    try:
        params = config()
        print('Connecting to the PostgreSQL database...')
        connection = psycopg2.connect(**params)
        print("Connection successful")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    return connection

# Function to close the connection if there is one currently open
def close_connection(connection):
    if connection is not None:
        connection.close()
        print('Database connection terminated')
