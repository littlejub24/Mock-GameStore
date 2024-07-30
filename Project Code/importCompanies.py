import csv
import psycopg2
from config import config

def insert_companies_from_csv(connection):
    try:
        cursor = connection.cursor()

        # Open the CSV file for reading
        with open("Companies.csv", mode="r") as csv_file:
            csv_reader = csv.reader(csv_file)

            for row in csv_reader:
                if len(row) == 3:
                    company_id, name, date_founded = row

                    # Insert the company data into the database
                    insert_query = """
                        INSERT INTO public.company (companyid, name, datefounded)
                        VALUES (%s, %s, %s)
                    """
                    company_data = (company_id, name, date_founded)
                    cursor.execute(insert_query, company_data)

        connection.commit()
        print("Companies inserted successfully")

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)