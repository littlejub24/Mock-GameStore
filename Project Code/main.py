from register import *
from connection import *
from importCompanies import *
from importUsers import *
from importGames import *
from importReviews import *
from importDevelopers import *
from importDLC import *
from deleteALL import *
from welcomeScreen import *

if __name__ == "__main__":
    connection = connect() # This initially opens the connection to the datbase and should be running everytime no matter what

    # # Uncomment the following if they are not already inserted into the tables
    # insert_companies_from_csv(connection)
    # insert_users_from_csv(connection)
    # insert_games_from_csv(connection)
    # insert_reviews_from_csv(connection)
    # insert_dlc_from_csv(connection)
    # insert_developers_from_csv(connection)
    
    username = None
    logout = True  #initially set to True so it will open at least once

    while logout == True:   # If logout returns with false it means the program was closed without logging out and will break the loop and not open any more pages
        username = login(connection)
        logout = open_store_window(connection,username)


    close_connection(connection) # This should be running every single time to make sure the connection is getting closed if it is open