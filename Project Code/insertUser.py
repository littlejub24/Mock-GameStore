import psycopg2
from config import config

def insert_user(connection, username, name, password, email, dob):
    try:
        # Create a cursor
        crsr = connection.cursor()

        # Insert a new user
        insert_query = """
            INSERT INTO public.users (username, name, password, email, dob)
            VALUES (%s, %s, %s, %s, %s)
        """
        user_data = (username, name, password, email, dob)
        crsr.execute(insert_query, user_data)
        connection.commit()
        print("User inserted successfully")

        crsr.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)