import tkinter as tk
import tkinter.messagebox as messagebox
import psycopg2
from connection import *

# Only use if you are sure you want to delete all data from the database

def delete_all_data(connection):
    cursor = connection.cursor()

    # Create a tkinter window for the confirmation dialog
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Ask the user for confirmation using a messagebox
    confirmation = messagebox.askquestion("Confirmation", "Are you sure you want to delete all data?", icon='warning')

    if confirmation == 'yes':
        # Delete all data from the "purchase" table
        cursor.execute("DELETE FROM public.purchase")
        
        # Delete all data from the "reviews" table
        cursor.execute("DELETE FROM public.reviews")
        
        # Delete all data from the "wishlist" table
        cursor.execute("DELETE FROM public.wishlist")

        # Delete all data from the "users" table
        cursor.execute("DELETE FROM public.users")

        # Delete all data from the "games" table
        cursor.execute("DELETE FROM public.games")

        # Delete all data from the "company" table
        cursor.execute("DELETE FROM public.company")

        # Delete all data from the "developer" table
        cursor.execute("DELETE FROM public.developer")

        # Delete all data from the "dlc" table
        cursor.execute("DELETE FROM public.dlc")

        # Commit the changes
        connection.commit()

        messagebox.showinfo("Deletion Completed", "All data has been deleted.")
    else:
        messagebox.showinfo("Deletion Canceled", "Deletion canceled.")