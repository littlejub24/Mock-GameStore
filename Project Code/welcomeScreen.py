import tkinter as tk
from tkinter import ttk
import psycopg2
from datetime import date

# Class used for error popups if needed.
class ErrorPopup:
    def __init__(self, root, title, message):
        self.popup = tk.Toplevel(root)
        self.popup.title(title)

        label = tk.Label(self.popup, text=message, padx=10, pady=10)
        label.pack()

        close_button = tk.Button(self.popup, text="Close", command=self.popup.destroy)
        close_button.pack(pady=10)

# Home page for store or first screen that appears after you login
def open_store_window(connection, username):
    global user_logout #Variable to be returned. If the user presses the logoutbutton then it should return as true
    user_logout = False
    if username is None:
        return

    # Will be called if profile button is clicked
    def open_profile():
        store_window.destroy()
        create_profile_page(connection,username)

    # Will be called if store button is clicked
    def open_store():
        store_window.destroy()
        create_store_page(connection, username)

    # Will be called if library button is clicked
    def open_library():
        store_window.destroy()
        open_library_page(connection, username)
    
    # It will close the home page return to the main function that user_logout was True so it will open the login window again
    def logout():
        global user_logout
        user_logout = True
        store_window.destroy()

    # Creation and dimensions of window
    store_window = tk.Tk()
    store_window.title("Welcome to our Store!")
    window_width = store_window.winfo_screenwidth()
    window_height = store_window.winfo_screenheight()
    store_window.geometry(f"{window_width}x{window_height}+0+0")  # Fullscreen

    welcome_label = tk.Label(store_window, text=f"Welcome, {username}!", font=("Helvetica", 16))
    welcome_label.pack(pady=20)


    # Creation of all buttons on page
    profile_button = tk.Button(store_window, text="Profile", command=open_profile)
    profile_button.pack()

    store_button = tk.Button(store_window, text="Store", command=open_store)
    store_button.pack()

    library_button = tk.Button(store_window, text="Library", command=open_library)
    library_button.pack()

    logout_button = tk.Button(store_window, text="Logout", command=logout)
    logout_button.pack()

    store_window.mainloop()

    return user_logout

# Function used if game information needs to be displayed on a page it will fetch the data using a select statement
def fetch_game_data(connection):
    cursor = connection.cursor()
    cursor.execute("""
        SELECT TRIM(g.gameid), g.title, g.price, g.rating, g.releasedate, c.name
        FROM public.games g
        JOIN public.company c ON g.companyid = c.companyid
    """)
    game_data = cursor.fetchall()
    cursor.close()
    return game_data

#It will check the username and game_id to check if they already purchased this game
def has_purchased(connection, username, game_id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM public.purchase WHERE username = %s AND gameid = %s", (username, game_id))
    return cursor.fetchone() is not None

# Used later to show if you have already purchased a game or if it was Successful 
# It is just a class to create an example window and the message is inserted later
class InfoPopup:
    def __init__(self, root, title, message):
        self.popup = tk.Toplevel(root)
        self.popup.title(title)

        label = tk.Label(self.popup, text=message, padx=10, pady=10)
        label.pack()

        close_button = tk.Button(self.popup, text="Close", command=self.popup.destroy)
        close_button.pack(pady=10)

# First will check if you purchased using previous functions. If you don't have it, then it will insert the purchase with the correct data.
def purchase_game(connection, root, username, game_id):
    try:
        if has_purchased(connection, username, game_id):
            ErrorPopup(root, "Already Purchased", "You have already purchased this game.")
            return

        cursor = connection.cursor()
        purchase_query = """
            INSERT INTO public.purchase (username, gameid, purchasedate)
            VALUES (%s, %s, %s)
        """
        purchase_data = (username, game_id, date.today())
        cursor.execute(purchase_query, purchase_data)
        connection.commit()
        InfoPopup(root, "Purchase Successful", "You have successfully purchased the game!")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error purchasing game: {error}")
    finally:
        cursor.close()


# Page to display profile information related to the user on their own profile page
def create_profile_page(connection, username):
    def go_back():
        profile_page_window.destroy()
        open_store_window(connection, username)
    
    # Creation and dimensions of window
    profile_page_window = tk.Tk()
    profile_page_window.title("Profile")
    window_width = profile_page_window.winfo_screenwidth()
    window_height = profile_page_window.winfo_screenheight()
    profile_page_window.geometry(f"{window_width}x{window_height}+0+0")  # Fullscreen

    # Fetch user information
    user_info = get_user_info(connection, username)

    # Labels to display user information
    username_label = tk.Label(profile_page_window, text=f"Username: {user_info[0]}", font=("Helvetica", 16))
    username_label.pack(pady=10)

    name_label = tk.Label(profile_page_window, text=f"Name: {user_info[1]}", font=("Helvetica", 16))
    name_label.pack(pady=10)

    email_label = tk.Label(profile_page_window, text=f"Email: {user_info[2]}", font=("Helvetica", 16))
    email_label.pack(pady=10)

    dob_label = tk.Label(profile_page_window, text=f"Date of Birth: {user_info[3]}", font=("Helvetica", 16))
    dob_label.pack(pady=10)

    # "Go Back" button
    go_back_button = tk.Button(profile_page_window, text="Go Back", command=go_back)
    go_back_button.pack(side=tk.TOP, anchor=tk.NE, padx=10, pady=10)

    # Run the main loop
    profile_page_window.mainloop()

#used in profile page to get info to be displayed
def get_user_info(connection, username):
    cursor = connection.cursor()
    cursor.execute("""
        SELECT username, name, email, dob
        FROM public.users
        WHERE username = %s
    """, (username,))
    user_info = cursor.fetchone()
    cursor.close()
    return user_info


# Page to display all games you can purchase
def create_store_page(connection, username):
    def go_back():
        root.destroy()
        open_store_window(connection, username)

    # Function that gets called when you click on the purchase button on the store. It will check if you have purchased it already and if not it will buy it
    def purchase_clicked(game_id):
        cleaned_game_id = game_id.strip()
        if has_purchased(connection, username, cleaned_game_id):
            ErrorPopup(root, "Already Purchased", "You have already purchased this game.")
        else:
            print(f"Purchasing game with ID: {cleaned_game_id}")
            purchase_game(connection, root, username, cleaned_game_id)

    # Function to call the view_game_page to see reviews for the game before you buy it
    def view_game_clicked(game_id):
        view_game_page(connection, game_id)

    # Function to display game information including reviews but will not let you leave a review. Function is repeated down furthur on library page. The other function lets you leave a review
    def view_game_page(connection, game_id):
        def go_back():
            game_page_window.destroy()

        def refresh_reviews():
            # Fetch reviews information after submitting a new review
            cursor = connection.cursor()
            cursor.execute("""
                SELECT r.username, r.content, r.rating, r.datewritten
                FROM public.reviews r
                WHERE r.gameid = %s
            """, (game_id,))
            reviews_info = cursor.fetchall()

            # Destroy previous reviews labels
            for widget in reviews_frame.winfo_children():
                widget.destroy()

            if reviews_info:
                for review in reviews_info:
                    review_text = (
                        f"Username: {review[0]}\n"
                        f"Content: {review[1]}\n"
                        f"Rating: {review[2]}\n"
                        f"Date Written: {review[3]}\n"
                    )
                    review_label = tk.Label(reviews_frame, text=review_text, font=("Helvetica", 12))
                    review_label.pack()

        # Creation and dimensions of window
        game_page_window = tk.Tk()
        game_page_window.title("Game Page")
        window_width = game_page_window.winfo_screenwidth()
        window_height = game_page_window.winfo_screenheight()
        game_page_window.geometry(f"{window_width}x{window_height}+0+0")  # Fullscreen


        cursor = connection.cursor()

        # Fetch game information
        cursor.execute("""
            SELECT g.title, c.name AS company_name, g.rating, g.releasedate
            FROM public.games g
            JOIN public.company c ON g.companyid = c.companyid
            WHERE g.gameid = %s
        """, (game_id,))
        game_info = cursor.fetchone()

        # All of the labels
        title_label = tk.Label(game_page_window, text=f"Game Title: {game_info[0]}", font=("Helvetica", 14))
        title_label.pack(pady=10)

        company_label = tk.Label(game_page_window, text=f"Company: {game_info[1]}", font=("Helvetica", 12))
        company_label.pack(pady=5)

        rating_label = tk.Label(game_page_window, text=f"Rating: {game_info[2]}", font=("Helvetica", 12))
        rating_label.pack(pady=5)

        release_date_label = tk.Label(game_page_window, text=f"Release Date: {game_info[3]}", font=("Helvetica", 12))
        release_date_label.pack(pady=10)

        # Fetch DLC information
        cursor.execute("""
            SELECT d.title, d.releasedate
            FROM public.dlc d
            WHERE d.gameid = %s
        """, (game_id,))
        dlc_info = cursor.fetchall()

        if dlc_info:
            dlc_label = tk.Label(game_page_window, text="DLCs:", font=("Helvetica", 14))
            dlc_label.pack(pady=10)

            for dlc in dlc_info:
                dlc_text = f"{dlc[0]} - Released on {dlc[1]}"
                dlc_label = tk.Label(game_page_window, text=dlc_text, font=("Helvetica", 12))
                dlc_label.pack()

        # Fetch reviews information
        cursor.execute("""
            SELECT r.username, r.content, r.rating, r.datewritten
            FROM public.reviews r
            WHERE r.gameid = %s
        """, (game_id,))
        reviews_info = cursor.fetchall()

        reviews_label = tk.Label(game_page_window, text="Reviews:", font=("Helvetica", 14))
        reviews_label.pack(pady=10)

        reviews_frame = tk.Frame(game_page_window)
        reviews_frame.pack()

        if reviews_info:
            for review in reviews_info:
                review_text = (
                    f"Username: {review[0]}\n"
                    f"Content: {review[1]}\n"
                    f"Rating: {review[2]}\n"
                    f"Date Written: {review[3]}\n"
                )
                review_label = tk.Label(reviews_frame, text=review_text, font=("Helvetica", 12))
                review_label.pack()

        cursor.close()

        go_back_button = tk.Button(game_page_window, text="Go Back", command=go_back)
        go_back_button.pack(pady=10)

        game_page_window.mainloop()

    # Creation and dimensions of window
    root = tk.Tk()
    root.title("Game Store")
    window_width = root.winfo_screenwidth()
    window_height = root.winfo_screenheight()
    root.geometry(f"{window_width}x{window_height}+0+0")  # Fullscreen

    # Placement and sizing things for tkinter
    canvas = tk.Canvas(root, height=window_height)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas.configure(yscrollcommand=scrollbar.set)

    frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor=tk.NW)

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    frame.bind("<Configure>", on_frame_configure)

    # Labels and buttons
    username_label = tk.Label(frame, text=f"Welcome, {username}!", font=("Helvetica", 12))
    username_label.grid(row=0, column=4, padx=10, pady=5)

    go_back_button = tk.Button(frame, text="Go Back", command=go_back)
    go_back_button.grid(row=0, column=5, padx=10, pady=5)

    headers = ["Title", "Price", "Rating", "Release Date", "Company", ""]
    

    #Places the headers in the same row at the top
    header_labels = [tk.Label(frame, text=header, font=("Helvetica", 12)) for header in headers]
    for i, header_label in enumerate(header_labels):
        header_label.grid(row=1, column=i, padx=10, pady=5)

    # Fetches all of the game data
    game_data = fetch_game_data(connection)

    # Places all of the information on the store page under the headers bars in the correct locations
    for row, game_info in enumerate(game_data, start=2):
        for col, value in enumerate(game_info[1:]):
            game_label = tk.Label(frame, text=value)
            game_label.grid(row=row, column=col, padx=10, pady=5)

        game_id = game_info[0]

        # purchase button will display and holds the game id in each row
        if has_purchased(connection, username, game_id):
            purchase_button = tk.Button(frame, text="Purchased", state=tk.DISABLED)
        else:
            purchase_button = tk.Button(frame, text="Purchase", command=lambda game_id=game_id: purchase_clicked(game_id))
        purchase_button.grid(row=row, column=col+1, padx=10, pady=5)

        # View Game button will appear as well and hold the gameid for that row
        view_game_button = tk.Button(frame, text="View Game", command=lambda game_id=game_id: view_game_clicked(game_id))
        view_game_button.grid(row=row, column=col+2, padx=10, pady=5)

    def on_mouse_wheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    canvas.bind("<MouseWheel>", on_mouse_wheel)

    root.mainloop()


def open_library_page(connection, username):
    def go_back():
        library_window.destroy()
        open_store_window(connection, username)

    # Same  function as the one on the store page. Except this one lets you leave a review since you already purchased it
    def view_game_page(connection, game_id):
        def go_back():
            game_page_window.destroy()
        #Popup window to leave a review for the game
        def leave_review():
            leave_review_popup = tk.Toplevel(game_page_window)
            leave_review_popup.title("Leave a Review")

            # Components for the popup window
            content_label = tk.Label(leave_review_popup, text="Write your review:")
            content_label.pack(pady=5)

            content_entry = tk.Entry(leave_review_popup, width=50)
            content_entry.pack(pady=5)

            rating_label = tk.Label(leave_review_popup, text="Select a rating (1-5):")
            rating_label.pack(pady=5)

            rating_var = tk.StringVar()
            rating_var.set("1")  # Default rating is 1

            rating_menu = tk.OptionMenu(leave_review_popup, rating_var, "1", "2", "3", "4", "5")
            rating_menu.pack(pady=5)

            submit_button = tk.Button(leave_review_popup, text="Submit Review", command=lambda: submit_review(content_entry.get(), rating_var.get(), leave_review_popup))
            submit_button.pack(pady=10)

        def submit_review(content, rating, popup):
            cursor = connection.cursor()

            # Fetch the highest current review ID and add 1 to it
            cursor.execute("SELECT MAX(reviewid) FROM public.reviews")
            max_review_id = cursor.fetchone()[0]
            new_review_id = int(max_review_id) + 1 if max_review_id is not None else 1

            # Insert the new review into the table
            cursor.execute("""
                INSERT INTO public.reviews (reviewid, rating, content, datewritten, username, gameid)
                VALUES (%s, %s, %s, CURRENT_DATE, %s, %s)
            """, (new_review_id, rating, content, username, game_id))
            connection.commit()

            cursor.close()

            # Refresh the reviews display
            refresh_reviews()

            popup.destroy()

        def refresh_reviews():
            # Fetch reviews information after submitting a new review
            cursor = connection.cursor()
            cursor.execute("""
                SELECT r.username, r.content, r.rating, r.datewritten
                FROM public.reviews r
                WHERE r.gameid = %s
            """, (game_id,))
            reviews_info = cursor.fetchall()

            # Destroy previous reviews labels
            for widget in reviews_frame.winfo_children():
                widget.destroy()

            if reviews_info:
                for review in reviews_info:
                    review_text = (
                        f"Username: {review[0]}\n"
                        f"Content: {review[1]}\n"
                        f"Rating: {review[2]}\n"
                        f"Date Written: {review[3]}\n"
                    )
                    review_label = tk.Label(reviews_frame, text=review_text, font=("Helvetica", 12))
                    review_label.pack()

        # Creation and dimensions of window
        game_page_window = tk.Tk()
        game_page_window.title("Game Page")
        window_width = game_page_window.winfo_screenwidth()
        window_height = game_page_window.winfo_screenheight()
        game_page_window.geometry(f"{window_width}x{window_height}+0+0")  # Fullscreen


        cursor = connection.cursor()

        # Fetch game information
        cursor.execute("""
            SELECT g.title, c.name AS company_name, g.rating, g.releasedate
            FROM public.games g
            JOIN public.company c ON g.companyid = c.companyid
            WHERE g.gameid = %s
        """, (game_id,))
        game_info = cursor.fetchone()

        #Labels created and placed
        title_label = tk.Label(game_page_window, text=f"Game Title: {game_info[0]}", font=("Helvetica", 14))
        title_label.pack(pady=10)

        company_label = tk.Label(game_page_window, text=f"Company: {game_info[1]}", font=("Helvetica", 12))
        company_label.pack(pady=5)

        rating_label = tk.Label(game_page_window, text=f"Rating: {game_info[2]}", font=("Helvetica", 12))
        rating_label.pack(pady=5)

        release_date_label = tk.Label(game_page_window, text=f"Release Date: {game_info[3]}", font=("Helvetica", 12))
        release_date_label.pack(pady=10)

        # Fetch DLC information
        cursor.execute("""
            SELECT d.title, d.releasedate
            FROM public.dlc d
            WHERE d.gameid = %s
        """, (game_id,))
        dlc_info = cursor.fetchall()

        # Formatting of the DLC information to be displayed
        if dlc_info:
            dlc_label = tk.Label(game_page_window, text="DLCs:", font=("Helvetica", 14))
            dlc_label.pack(pady=10)

            for dlc in dlc_info:
                dlc_text = f"{dlc[0]} - Released on {dlc[1]}"
                dlc_label = tk.Label(game_page_window, text=dlc_text, font=("Helvetica", 12))
                dlc_label.pack()

        # Fetch reviews information
        cursor.execute("""
            SELECT r.username, r.content, r.rating, r.datewritten
            FROM public.reviews r
            WHERE r.gameid = %s
        """, (game_id,))
        reviews_info = cursor.fetchall()

        reviews_label = tk.Label(game_page_window, text="Reviews:", font=("Helvetica", 14))
        reviews_label.pack(pady=10)

        # Reviews have their own frame within the window to neatly display info
        reviews_frame = tk.Frame(game_page_window)
        reviews_frame.pack()

        # Display all of the review information corresponding to specific date in order
        if reviews_info:
            for review in reviews_info:
                review_text = (
                    f"Username: {review[0]}\n"
                    f"Content: {review[1]}\n"
                    f"Rating: {review[2]}\n"
                    f"Date Written: {review[3]}\n"
                )
                review_label = tk.Label(reviews_frame, text=review_text, font=("Helvetica", 12))
                review_label.pack()

        leave_review_button = tk.Button(game_page_window, text="Leave a Review", command=leave_review)
        leave_review_button.pack(pady=10)

        cursor.close()

        go_back_button = tk.Button(game_page_window, text="Go Back", command=go_back)
        go_back_button.pack(pady=10)

        game_page_window.mainloop()

    def view_company_page(connection, company_id):
        def go_back():
            company_page_window.destroy()

        # Creation and dimensions of window
        company_page_window = tk.Tk()
        company_page_window.title("Company Page")
        window_width = company_page_window.winfo_screenwidth()
        window_height = company_page_window.winfo_screenheight()
        company_page_window.geometry(f"{window_width}x{window_height}+0+0")  # Fullscreen

        cursor = connection.cursor()

        # Fetch company information
        cursor.execute("""
    SELECT company_name, game_title, game_releasedate, developer_name
    FROM company_games_developers_view
    WHERE companyid = %s
""", (company_id,))
        company_info = cursor.fetchall()

        company_name_label = tk.Label(company_page_window, text=f"Company: {company_info[0][0]}", font=("Helvetica", 14))
        company_name_label.pack(pady=10)

        # Display games and their release dates
        games_label = tk.Label(company_page_window, text="Games and Release Dates:", font=("Helvetica", 12))
        games_label.pack(pady=5)

        for game in company_info:
            game_text = f"Game: {game[1]}, Release Date: {game[2]}"
            game_label = tk.Label(company_page_window, text=game_text, font=("Helvetica", 12))
            game_label.pack()

        # Display developers
        developers_label = tk.Label(company_page_window, text="Developers:", font=("Helvetica", 12))
        developers_label.pack(pady=10)

        developers = set(game[3] for game in company_info)  # Use a set to avoid duplicates
        for developer in developers:
            developer_label = tk.Label(company_page_window, text=f"Developer: {developer}", font=("Helvetica", 12))
            developer_label.pack()

        cursor.close()

        go_back_button = tk.Button(company_page_window, text="Go Back", command=go_back)
        go_back_button.pack(pady=10)

        company_page_window.mainloop()

    # Creation and dimensions of window
    library_window = tk.Tk()
    library_window.title("Your Library")
    window_width = library_window.winfo_screenwidth()
    window_height = library_window.winfo_screenheight()
    library_window.geometry(f"{window_width}x{window_height}+0+0")  # Fullscreen

    # Placement/formating information in tkinter
    canvas = tk.Canvas(library_window, height=window_height)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(library_window, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas.configure(yscrollcommand=scrollbar.set)

    frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor=tk.NW)

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    frame.bind("<Configure>", on_frame_configure)

    # Displays your username showing it is your library
    username_label = tk.Label(frame, text=f"Your Library, {username}!", font=("Helvetica", 12))
    username_label.grid(row=0, column=3, padx=10, pady=5)

    go_back_button = tk.Button(frame, text="Go Back", command=go_back)
    go_back_button.grid(row=0, column=4, padx=10, pady=5)

    headers = ["Game Title", "Date Purchased", "Company", "View Game", "View Company"]
    # Places all the header labels in your library similar to store page
    header_labels = [tk.Label(frame, text=header, font=("Helvetica", 12)) for header in headers]
    for i, header_label in enumerate(header_labels):
        header_label.grid(row=1, column=i, padx=10, pady=5)

    # Fetch user's library data
    cursor = connection.cursor()
    cursor.execute("""
        SELECT p.gameid, g.title, p.purchasedate, c.name AS company_name
        FROM public.purchase p
        JOIN public.games g ON p.gameid = g.gameid
        JOIN public.company c ON g.companyid = c.companyid
        WHERE p.username = %s
    """, (username,))
    library_data = cursor.fetchall()
    cursor.close()

    # Displays all of the information for each game
    for row, library_info in enumerate(library_data, start=2):
        for col, value in enumerate(library_info[1:]):
            game_label = tk.Label(frame, text=value)
            game_label.grid(row=row, column=col, padx=10, pady=5)

        game_id, _, _, company_name = library_info

        view_game_button = tk.Button(frame, text="View Game", command=lambda game_id=game_id: view_game_page(connection,game_id))
        view_game_button.grid(row=row, column=col + 1, padx=10, pady=5)

        company_id = get_company_id(connection, company_name)
        view_company_button = tk.Button(frame, text="View Company", command=lambda company_id=company_id: view_company_page(connection,company_id))
        view_company_button.grid(row=row, column=col + 2, padx=10, pady=5)

    def on_mouse_wheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    canvas.bind("<MouseWheel>", on_mouse_wheel)

    library_window.mainloop()

# Slects the company id and returns it
def get_company_id(connection, company_name):
    cursor = connection.cursor()
    cursor.execute("SELECT companyid FROM public.company WHERE name = %s", (company_name,))
    company_id = cursor.fetchone()
    cursor.close()
    return company_id[0] if company_id else None