import psycopg2
import csv
from passwordHash import *

def insert_users_from_csv(connection):
    try:
        cursor = connection.cursor()
        with open("Users.csv", 'r') as file:
            csv_reader = csv.reader(file)

            for row in csv_reader:
                name, username, password, email, dob = row
                cursor.execute(
                    """
                    INSERT INTO public.users (name, username, password, email, dob)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (name, username, hash_password(password), email, dob)
                    # Only notable thing is is the use of hash_password(password)
                    # Before inserting the password into the database it will use the function to encrypt the password
                )

        connection.commit()
        print("Users inserted successfully")

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)