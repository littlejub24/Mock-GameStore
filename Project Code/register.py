import tkinter as tk
import psycopg2
from config import config 
import tkinter.messagebox as messagebox
import datetime
from insertUser import insert_user
from passwordHash import *

def create_account(connection):
    def save_user_data():
        # Retrieve input values
        name_value = name_entry.get()
        username_value = username_entry.get()
        password_value = password_entry.get()
        email_value = email_entry.get()
        dob_value = dob_entry.get()

        # Check if any field is empty
        if not name_value or not username_value or not password_value or not email_value or not dob_value:
            messagebox.showerror("Error", "All fields must be filled out.")
            return

        # Validate unique username and email
        if not is_unique_username(connection, username_value):
            messagebox.showerror("Error", "Username already exists. Please choose a different username.")
            return

        if not is_unique_email(connection, email_value):
            messagebox.showerror("Error", "Email already exists. Please use a different email.")
            return

        # Validate date format
        if not is_valid_date(dob_value):
            messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")
            return

        # Insert the user data into the database
        insert_user(connection, username_value, name_value, hash_password(password_value), email_value, dob_value) # Calls the insert_user function but it will hash the password before inserting it into the database.

        messagebox.showinfo("Success", "Profile Created Successfully!")

        # Close the registration window
        switch_to_login()


    def switch_to_login():
        window.destroy()  # Close the registration window

    # Create a tkinter window
    window = tk.Tk()
    window.title("User Registration")

    window_width = window.winfo_screenwidth()
    window_height = window.winfo_screenheight()
    window.geometry(f"{window_width}x{window_height}+0+0")  # Fullscreen

    # Labels and Entry Widgets
    name_label = tk.Label(window, text="Name")
    name_label.pack()
    name_entry = tk.Entry(window)
    name_entry.pack()

    username_label = tk.Label(window, text="Username")
    username_label.pack()
    username_entry = tk.Entry(window)
    username_entry.pack()

    password_label = tk.Label(window, text="Password")
    password_label.pack()
    password_entry = tk.Entry(window, show="*")  # Show asterisks for password input
    password_entry.pack()

    email_label = tk.Label(window, text="Email")
    email_label.pack()
    email_entry = tk.Entry(window)
    email_entry.pack()

    dob_label = tk.Label(window, text="Date of Birth (YYYY-MM-DD)")
    dob_label.pack()
    dob_entry = tk.Entry(window)
    dob_entry.pack()

    # Save Button
    save_button = tk.Button(window, text="Create", command=save_user_data)
    save_button.pack()

    # Already Have an Account Button
    login_button = tk.Button(window, text="Already Have an Account", command=switch_to_login)
    login_button.pack()

    window.mainloop()

# Helper function to check if the username is unique
def is_unique_username(connection, username):
    cursor = connection.cursor()
    cursor.execute("SELECT username FROM public.users WHERE username = %s", (username,))
    return cursor.fetchone() is None

# Helper function to check if the email is unique
def is_unique_email(connection, email):
    cursor = connection.cursor()
    cursor.execute("SELECT email FROM public.users WHERE email = %s", (email,))
    return cursor.fetchone() is None

# Helper function to check if the date is in the correct format
def is_valid_date(date_string):
    try:
        datetime.datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except ValueError:
        return False

# Function to insert user data into the database and return the username
def login(connection):

    result = None  # Initialize result as None

    # Create a tkinter window
    login_window = tk.Tk()
    login_window.title("Login")

    # Function to check the provided username and password
    def check_credentials():
        nonlocal result
        provided_username = username_entry.get()
        provided_password = password_entry.get()

        # Check if both fields are non-empty
        if not provided_username or not provided_password:
            messagebox.showerror("Error", "Both username and password must be filled out.")
            return

        try:
            if connection is None:
                # Handle the case where the connection is None
                messagebox.showerror("Error", "Connection to the database is not established.")
                return

            cursor = connection.cursor()
            
            # This statement is checking if a username and password match in the database
            # To do this you have to hash the password that was input at the login screen with the, already hashed password currently in the database
            cursor.execute("SELECT username, password FROM public.users WHERE username = %s AND password = %s", (provided_username, hash_password(provided_password)))
            user = cursor.fetchone()

            if user:
                print("Login successful")
                result = provided_username
                login_window.destroy()
            else:
                messagebox.showerror("Error", "Username and Password do not match.")

            cursor.close()
        except psycopg2.Error as error:
            print("Error connecting to the database:", error)


    window_width = login_window.winfo_screenwidth()
    window_height = login_window.winfo_screenheight()
    login_window.geometry(f"{window_width}x{window_height}+0+0")  # Fullscreen

    # Labels and Entry Widgets
    username_label = tk.Label(login_window, text="Username")
    username_label.pack()
    username_entry = tk.Entry(login_window)
    username_entry.pack()

    password_label = tk.Label(login_window, text="Password")
    password_label.pack()
    password_entry = tk.Entry(login_window, show="*")  # Show asterisks for password input
    password_entry.pack()

    # Login Button
    login_button = tk.Button(login_window, text="Login", command=check_credentials)
    login_button.pack()

    # Create Account Button
    create_account_button = tk.Button(login_window, text="Create an account", command=lambda: [create_account(connection)])
    create_account_button.pack()

    login_window.mainloop()

    return result