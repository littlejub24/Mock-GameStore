import psycopg2
import csv

# Uses INSERT statement to insert existing info as examples from a csv
def insert_dlc_from_csv(connection):
    try:
        cursor = connection.cursor()
        with open("DLC.csv", 'r') as file:
            csv_reader = csv.reader(file)

            for row in csv_reader:
                dlcid, gameid, title, price, rating, releasedate, companyid = row
                cursor.execute(
                    """
                    INSERT INTO public.dlc (dlcid, gameid, title, price, rating, releasedate, companyid)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (dlcid, gameid.strip(), title, price, rating, releasedate, companyid)
                )

        connection.commit()
        print("DLC inserted successfully")

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)