import psycopg2
import csv

def insert_reviews_from_csv(connection):
    try:
        cursor = connection.cursor()
        with open("Reviews.csv", 'r') as file:
            csv_reader = csv.reader(file)

            for row in csv_reader:
                review_id, rating, content, date_written, username, game_id = row
                # Strip leading and trailing whitespaces from game_id
                game_id = game_id.strip()
                cursor.execute(
                    """
                    INSERT INTO public.reviews (reviewid, rating, content, datewritten, username, gameid)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (review_id, rating, content, date_written, username, game_id)
                )

        connection.commit()
        print("Reviews inserted successfully")

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
