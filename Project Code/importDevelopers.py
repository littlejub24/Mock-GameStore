import psycopg2
import csv
from passwordHash import *

def insert_developers_from_csv(connection):
    try:
        cursor = connection.cursor()
        with open("Developers.csv", 'r') as file:
            csv_reader = csv.reader(file)

            for row in csv_reader:
                devid, worksat, name, email, username, password, dob = row
                cursor.execute(
                    """
                    INSERT INTO public.developer (devid, worksat, name, email, username, password, dob)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (devid, worksat, name, email, username, hash_password(password), dob)
                )

        connection.commit()
        print("Developers inserted successfully")

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
