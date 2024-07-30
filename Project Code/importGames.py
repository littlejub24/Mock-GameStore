import psycopg2
import csv

def insert_games_from_csv(connection):
    try:
        cursor = connection.cursor()
        with open("Games.csv", 'r') as file:
            csv_reader = csv.reader(file)

            for row in csv_reader:
                gameid, price, title, release_date, rating, companyid = row
                cursor.execute(
                    """
                    INSERT INTO public.games (gameid, price, title, releasedate, rating, companyid)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (gameid, price, title, release_date, rating, companyid)
                )

        connection.commit()
        print("Games inserted successfully")

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)