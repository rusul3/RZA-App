import sqlite3
from datetime import datetime

# create function to connect with database to fetch the username if is exists 
def check_username_exists(Username):
    conn = sqlite3.connect("RZADatabase.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM User WHERE Username=?", (Username,))
    result = cur.fetchone()
    conn.close()
    return result is not None

# create function to connect with database to fetch and cheeck the username and the password ,also add reward points to user profile 
def check_credentials(username, password):
    conn = sqlite3.connect("RZADatabase.db")
    cur = conn.cursor()
    cur.execute('''SELECT User_ID FROM User WHERE Username = ? AND Password = ?''', (username, password))
    user_id = cur.fetchone()
    if user_id:
        # add reward points for logging in, e.g., 10 points
        cur.execute('''UPDATE Profile SET Reward_Points = Reward_Points + 10 WHERE User_ID = ?''', (user_id[0],))
        # fetch Profile_ID using User_ID
        cur.execute("SELECT Profile_ID FROM Profile WHERE User_ID = ?", (user_id,))
        profile_id = cur.fetchone()
        if profile_id:
            profile_id = profile_id[0]
        conn.commit()
    conn.close()
    return user_id if user_id else None

#create function to fetch the activity history to show it in profile of user
def fetch_activity_history(profile_id):
    conn = sqlite3.connect("RZADatabase.db")
    cur = conn.cursor()
    cur.execute("SELECT Activity_History FROM Profile WHERE Profile_ID = ?", (profile_id,))
    activity_history = cur.fetchone()
    conn.close()
    return activity_history[0] if activity_history else ""

#create function to update the acivity history 
def update_activity_history(user_id, new_activity):
    conn = sqlite3.connect("RZADatabase.db")
    cur = conn.cursor()
    # fetch the existing activity history
    current_activity_history = fetch_activity_history(user_id)
    #append the new activity
    updated_activity_history = f"{current_activity_history};{new_activity}" if current_activity_history else new_activity
    # update the Profile table
    cur.execute("UPDATE Profile SET Activity_History = ? WHERE User_ID = ?", (updated_activity_history, user_id))
    conn.commit()
    conn.close()

# create function connect with database to fetch the user informations from database
def get_user_info(user, pword):
    conn = sqlite3.connect("RZADatabase.db")
    cur = conn.cursor()
    cur.execute("SELECT Username, Password, Postcode, Email, User_ID FROM User WHERE Username = ? AND Password = ?", (user, pword))
    userInfo = cur.fetchone()
    conn.close()
    return userInfo

# create function connect to database to insert the data of user when create account also insert the date of regiseration and point to profile table
def create_new_user(Username, Password, Postcode, Email, FirstName, LastName):
    conn = sqlite3.connect("RZADatabase.db")
    cur = conn.cursor()
    # insert User
    cur.execute("INSERT INTO User (Username, Password, Postcode, Email, FirstName, LastName) VALUES (?, ?, ?, ?, ?, ?)", (Username, Password, Postcode, Email, FirstName, LastName))
    user_id = cur.lastrowid   
   # increment the user's points by 10
    cur.execute("""INSERT INTO Profile (User_ID, Registration_Date, Activity_History, Reward_Points) VALUES (?, CURRENT_DATE, CURRENT_DATE, 10)""", (user_id,))
    conn.commit()
    conn.close()
        
#create function to connect to database to fetch the profile information for the user
def profile_user(username,password):
    try:
        conn = sqlite3.connect("RZADatabase.db")
        cur = conn.cursor()
        # Fetch user info along with points
        cur.execute("SELECT Username, FirstName, LastName, Email, Password, FROM User WHERE Username = ? AND Password = ?", (username, password,))
        profile_data = cur.fetchone()  # fetches the first row of the query result
        return profile_data
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
    finally:
        conn.close()

#create the function to connect to database to fetch customer informations from user table and prfile table to show in profile page 
def get_profile(user_id):
    conn = sqlite3.connect("RZADatabase.db")
    cur = conn.cursor()
    # Assuming you want to select User_ID from the User table
    cur.execute("SELECT User.Username, User.FirstName, User.LastName, User.Email, User.Postcode,User.Password ,Profile.Registration_Date, Profile.Activity_History, Profile.Reward_Points, User.User_ID FROM User JOIN Profile ON User.User_ID = Profile.User_ID WHERE User.User_ID = ?", (user_id,))
    profile_data = cur.fetchone()
    conn.close()
    return profile_data

# create function to fetch user id from database
def get_new_user_id(username):
    conn = sqlite3.connect("RZADatabase.db")
    cur = conn.cursor()
    cur.execute("SELECT User_ID FROM User WHERE Username = ?", (username,))
    result = cur.fetchone()
    conn.close()
    if result:
        return result[0] 
    else:
        return None

#create function to fetch user id and update the informations for the user 
def edit_information(user_id, new_password, new_postcode, new_email):
     conn = sqlite3.connect("RZADatabase.db")
     cur = conn.cursor()
     cur.execute("SELECT Username FROM User WHERE User_ID=?", (user_id,))
     username_result = cur.fetchone()
     if username_result:
        username = username_result[0]
        cur.execute("UPDATE User SET Password=?, Postcode=?, Email=? WHERE Username=?", (new_password, new_postcode, new_email, username))
        conn.commit()
     conn.close()

#create function to connect to database and delete the information of user     
def delete_profile_data(user_id):
    conn = sqlite3.connect('RZADatabase.db')
    cursor = conn.cursor()
    sql_command = ("DELETE FROM User.Username, User.FirstName, User.LastName, User.Email, User.Postcode,User.Password ,Profile.Registration_Date, Profile.Activity_History, Profile.Reward_Points, User.User_ID FROM User JOIN Profile ON User.User_ID = Profile.User_ID WHERE User.User_ID = ?", (user_id,))
    try:
        cursor.execute(sql_command, (user_id,))
        conn.commit()
        print("Profile deleted successfully.")
    except Exception as e:
        print("Error deleting profile:", e)
    finally:
        conn.close() 

# availability data  for buy tickets
ticket_availability = {
    '2024-04-01': 100,
    '2024-04-02': 50,
    '2024-04-03': 0,
    '2024-04-04': 0, 
    '2024-04-05': 0,
    '2024-04-06': 0,
    '2024-04-07': 100,
    '2024-04-08': 100,
    '2024-04-09': 100,
    '2024-04-10': 30,
    '2024-04-11': 100,
    '2024-04-12': 40,
    '2024-04-13': 100,
    '2024-04-14': 10,
    '2024-04-15': 30,
    '2024-04-16': 100,
    '2024-04-17': 100,
    '2024-04-18': 100,
    '2024-04-19': 100,
    '2024-04-20': 100,
    '2024-04-21': 100,
    '2024-04-22': 100,
    '2024-04-23': 100
}

#create function to get the availabl date
def get_ticket_availability(date_str):
    # returns the number of available tickets for the given date
    return ticket_availability.get(date_str, 0) 

#create function to connect with database and insert the tickets data 
def insert_ticket_data(profile_id, date, slot_time, ticket_data, ticket_counts):
    conn = sqlite3.connect("RZADatabase.db")
    cur = conn.cursor()
    purchase_timestamp = datetime.now()  # current time as purchase timestamp
    # iterate over ticket_data and ticket_counts to insert each ticket type and its count
    for item, price in ticket_data.items():
        count = ticket_counts[item]
        if count > 0:  # only insert if tickets were selected
            # insert ticket data into the database, including the Profile_ID
            cur.execute('''
            INSERT INTO Ticket (Profile_ID, Date, Slot_Time, Ticket_type, Quantity, Price, Purchase_Timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (profile_id, date, slot_time, item, count, price, purchase_timestamp))
    conn.commit()
    conn.close()
    print("Ticket data inserted successfully.")

# Data of tickets and prices  
itemsArray = [
    "Standard Adult Admission", 
    "Standard Child", 
    "Standard Senior/Student",
    "Saver Ticket (2 adults + 2 children)"
]
ticket_prices = [
    22.50,
    16.85,
    19.10,
    70.80
]

# create a dictionary from itemsArray and ticket_prices for easy lookup
def get_all_products():
 ticket_data = dict(zip(itemsArray, ticket_prices))
 return ticket_data

#create function to connect with database to fetch the last ticket buy from customer
def fetch_tickets_since_last_login(profile_id):
    print(f"Fetching tickets for profile ID: {profile_id}")
    conn = sqlite3.connect("RZADatabase.db")
    cur = conn.cursor()
    cur.execute("SELECT last_login_timestamp FROM Profile WHERE Profile_ID = ?", (profile_id,))
    last_login_timestamp_result = cur.fetchone()
    print(f"Last login timestamp result: {last_login_timestamp_result}")
    if last_login_timestamp_result:
        last_login_timestamp = last_login_timestamp_result[0]
        print(f"Last login timestamp: {last_login_timestamp}")
        if last_login_timestamp:
            cur.execute("""
                SELECT Ticket_type, Quantity, Price
                FROM Ticket
                WHERE Profile_ID = ? AND Purchase_Timestamp >= ?
                ORDER BY Purchase_Timestamp DESC
            """, (profile_id, last_login_timestamp))
            tickets = cur.fetchall()
            print(f"Fetched tickets: {tickets}")
            return tickets

    return []

# create function to connect with database to update the last login time stamp
def update_last_login_timestamp(profile_id):
    conn = sqlite3.connect("RZADatabase.db")
    cur = conn.cursor()
    current_time = datetime.now()
    cur.execute("UPDATE Profile SET last_login_timestamp = ? WHERE Profile_ID = ?", (current_time, profile_id))
    conn.commit()
    conn.close()

# create function to connect with database to fetch the profile id from profile table 
def get_profile_id_by_user_id(user_id):
    conn = sqlite3.connect("RZADatabase.db")
    cur = conn.cursor()
    cur.execute("SELECT Profile_ID FROM Profile WHERE User_ID = ?", (user_id,))
    result = cur.fetchone()
    conn.close()
    if result:
        return result[0] 
    else:
        return None
 
# create function to connect wih database to fetch reward points from profile table    
def fetch_reward_points(profile_id):
    """Fetches reward points for the given user."""
    conn = sqlite3.connect("RZADatabase.db")
    cur = conn.cursor()
    cur.execute('''SELECT Reward_Points FROM Profile WHERE Profile_ID = ?''', (profile_id,))
    result = cur.fetchone()
    conn.close()
    return result[0] if result else 0

# reward setup the discount tiers as (points, discount_percentage)
def calculate_and_show_discount(reward_points, total_price):
    """Calculates and shows discount based on reward points."""
    # the discount tiers as (points, discount_percentage)
    discount_tiers = [
        (10, 20),
        (20, 30),
        (30, 40),
        (40, 50),
        (100, 75)
    ]
    discount_percentage = 0
    for points_threshold, percentage in discount_tiers:
        if reward_points >= points_threshold:
            discount_percentage = percentage
        else:
            break

    if discount_percentage > 0:
        discount_rate = discount_percentage / 100.0
        discount_amount = total_price * discount_rate
        discounted_price = total_price - discount_amount

        print(f"Original price: ${total_price}")
        print(f"Discount applied: ${discount_amount} ({discount_percentage}%)")
        print(f"Discounted price: ${discounted_price}")

        return discounted_price
    else:
        print(f"No discount applied. Original price: ${total_price}")
        return total_price
    
#fetch ticket id from database     
def get_ticket_id(profile_id):
    conn = sqlite3.connect('RZADatabase.db')
    cursor = conn.cursor()
    # SQL query to fetch the ticket_id
    query = "SELECT Ticket_ID FROM Ticket WHERE Profile_ID = ?"
    cursor.execute(query, (profile_id,))
    # fetch the result
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    else:
        return None 
    
# insert the buy ticket to database     
def insert_basket_data(profile_id, ticket_data):
    conn = sqlite3.connect('RZADatabase.db') 
    cursor = conn.cursor()
    for item_data in ticket_data:
        ticket_id = get_ticket_id(profile_id)
        if item_data[1] > 0:  # check if quantity (count) is more than 0
            total = item_data[1] * item_data[2]  # calculate total (quantity * price)
            cursor.execute('''
                INSERT INTO basket (Profile_ID, Ticket_ID, quantities, prices, items, total)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (profile_id, ticket_id, item_data[1], item_data[2], item_data[0], total)) 
    conn.commit()
    conn.close()

# fetch booking id from database
def get_booking_id(profile_id):
    conn = sqlite3.connect('RZADatabase.db')
    cursor = conn.cursor()
    # SQL query to fetch the booking_id
    query = "SELECT Booking_ID FROM Book_Hotel_Room WHERE Profile_ID = ?"
    cursor.execute(query, (profile_id,))
    result = cursor.fetchone() 
    conn.close()
    if result:
        return result[0]  
    else:
        return None 
    
# insert the booking room to database     
def insert_roomtobasket_data(profile_id, booking_data):
    conn = sqlite3.connect('RZADatabase.db') 
    cursor = conn.cursor()
    for item_data in booking_data:
        booking_id = get_booking_id(profile_id)
        if item_data[1] > 0:  
            cursor.execute('''
                INSERT INTO basket (Profile_ID, Booking_ID, quantities, prices, items)
                VALUES (?, ?, ?, ?, ?)
            ''', (profile_id, booking_id, item_data[1], item_data[2], item_data[0])) 
    conn.commit()
    conn.close()
    
# fetch ticket details from database    
def fetch_ticket_basket(profile_id):
    conn = sqlite3.connect('RZADatabase.db')
    cursor = conn.cursor()
    # Get the last login timestamp for the profile
    cursor.execute("SELECT last_login_timestamp FROM Profile WHERE Profile_ID = ?", (profile_id,))
    last_login_timestamp_result = cursor.fetchone()
    if last_login_timestamp_result:
        last_login_timestamp = last_login_timestamp_result[0]
        if last_login_timestamp:
            # to find the tickets purchased after the last login timestamp
            cursor.execute("""SELECT Ticket_type, Quantity, Price , Date, Slot_Time
                FROM Ticket
                WHERE Profile_ID = ? AND Purchase_Timestamp >= ?
                ORDER BY Purchase_Timestamp DESC
            """, (profile_id, last_login_timestamp))
            # fetch all the results
            ticket_details = cursor.fetchall()
            print(f"Latest purchase timestamp: {ticket_details}")

            if ticket_details:
                print(f"Latest purchase timestamp: {ticket_details[0][0]}")  #print the latest timestamp
                conn.close()
                return ticket_details

    conn.close()
    return []

#fetch booking details from database    
def fetch_booking_basket(profile_id):
    conn = sqlite3.connect('RZADatabase.db')
    cursor = conn.cursor()
    # Get the last login timestamp for the profile
    cursor.execute("SELECT last_login_timestamp FROM Profile WHERE Profile_ID = ?", (profile_id,))
    last_login_timestamp_result = cursor.fetchone()
    if last_login_timestamp_result:
        last_login_timestamp = last_login_timestamp_result[0]
        if last_login_timestamp:
            cursor.execute("""
                SELECT Room_type, Quantity, Total_Price, Number_Days, Check_in, Check_out
                FROM Book_Hotel_Room
                WHERE Profile_ID = ? AND Purchase_Timestamp >= ?
                ORDER BY Purchase_Timestamp DESC
            """, (profile_id, last_login_timestamp))
            room = cursor.fetchall()
            print(f"Fetched room: {room}")

            if room:
                print(f"Latest purchase timestamp: {room[0][0]}")  #print the latest timestamp to help see the data fetch
                conn.close()
                return room
    conn.close()
    return []

# data of room and prices
roomArray = [
    "Single Room", 
    "Double Room "
]
room_prices = [
    75,
    120
]

# create a dictionary from roomArray and room_prices for easy lookup
def get_all_room():
 room_data = dict(zip(roomArray, room_prices))
 return room_data

# create function to connect with database and insert the booking room in book hotel room table
def insert_room_data(profile_id, checkin_str, checkout_str, noG, room_data, room_counts):
    date_format = "%d-%m-%Y"   
    checkin_date = datetime.strptime(checkin_str, date_format)
    checkout_date = datetime.strptime(checkout_str, date_format)

    # calculate the number of days between check-in and check-out
    number_of_days = (checkout_date - checkin_date).days

    conn = sqlite3.connect("RZADatabase.db")
    cur = conn.cursor()
    purchase_timestamp = datetime.now()

    # iterate over room data and room counts to insert each entry
    for room_type, count in room_counts.items():
        if count > 0:  # Only insert if rooms were selected
            price_per_day = room_data[room_type]
            total_price = count * price_per_day * number_of_days  # Calculate total price
            cur.execute('''
                INSERT INTO Book_Hotel_Room (Profile_ID, Check_in, Check_out, Number_Guests, Room_type, Number_Days, Total_Price, Quantity, Purchase_Timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (profile_id, checkin_str, checkout_str, noG, room_type, number_of_days, total_price, count, purchase_timestamp))
    conn.commit()
    conn.close()
    print("Your booking data inserted successfully.")

# create function to connect with database and fetch the booking infromation from database    
def fetch_booking_since_last_login(profile_id):
    print(f"Fetching booking for profile ID: {profile_id}")# to see the data that fetch
    conn = sqlite3.connect("RZADatabase.db")
    cur = conn.cursor()
    
    cur.execute("SELECT last_login_timestamp FROM Profile WHERE Profile_ID = ?", (profile_id,))
    last_login_timestamp_result = cur.fetchone()
    print(f"Last login timestamp result: {last_login_timestamp_result}")

    if last_login_timestamp_result:
        last_login_timestamp = last_login_timestamp_result[0]
        print(f"Last login timestamp: {last_login_timestamp}")

        if last_login_timestamp:
            cur.execute("""
                SELECT Room_type, Quantity, Total_Price,Number_Days
                FROM Book_Hotel_Room
                WHERE Profile_ID = ? AND Purchase_Timestamp >= ?
                ORDER BY Purchase_Timestamp DESC
            """, (profile_id, last_login_timestamp))
            room = cur.fetchall()
            print(f"Fetched room: {room}")
            return room

    return []

#create function to connect with database and insert the final price to basket table in database
def insert_finalpricetobasket_data(profile_id, final_total):
    conn = sqlite3.connect("RZADatabase.db")
    cur = conn.cursor()
    basket_Timestamp = datetime.now()
    cur.execute('''
        INSERT INTO Basket (Profile_ID, Final_total,basket_Timestamp)
        VALUES (?, ?, ?)''', (profile_id, final_total, basket_Timestamp))
    conn.commit()
    conn.close()

# create function ti connect with database and fetch the final price from basket table   
def fetch_finalprice_basket(profile_id):
    conn = sqlite3.connect('RZADatabase.db')
    cursor = conn.cursor()
    # get the last login timestamp for the profile
    cursor.execute("SELECT last_login_timestamp FROM Profile WHERE Profile_ID = ?", (profile_id,))
    last_login_timestamp_result = cursor.fetchone()

    if last_login_timestamp_result:
        last_login_timestamp = last_login_timestamp_result[0]

        if last_login_timestamp:
            cursor.execute("""
                SELECT Final_total
                FROM Basket
                WHERE Profile_ID = ? AND basket_Timestamp > ?
                ORDER BY Basket_ID DESC """, (profile_id, last_login_timestamp))
            final_price = cursor.fetchall()
            print(f"Fetched room: {final_price}")

            if final_price:
                print(f"Latest purchase timestamp: {final_price[0][0]}")  #print the latest timestamp for check
                conn.close()
                return final_price

    conn.close()
    return []    

# create function to connect with database and add member ship information to database
def add_membership_to_database(membership_type, profile_id):
   try:
    conn = sqlite3.connect('RZADatabase.db')
    cursor = conn.cursor()
    Membership_Timestamp = datetime.now()
    if membership_type == "Silver for Adult":
        price = 64 
        Aduld_Child = 'Adult'
    if membership_type == "Gold for Adult":
        price = 45 
        Aduld_Child = 'Adult'
    if membership_type == "Silver for Child":
        price = 44.75
        Aduld_Child = 'Child'
    if membership_type == "Gold for Child":
        price = 35 
        Aduld_Child = 'Child'
    cursor.execute("INSERT INTO Membership (Aduld_Child, Type_SorG, Price, Membership_Timestamp, Profile_ID) VALUES (?, ?, ?, ?, ?)", (Aduld_Child, membership_type, price,Membership_Timestamp, profile_id))
    conn.commit()
    print("Inserting with Profile ID:", profile_id)
   except sqlite3.Error as error:
        print("Error while inserting into database:", error)
   finally:
        conn.close()

# create function to connect with database and fetch the membership details from database
def fetch_membership_since_last_login(profile_id):
    print(f"Fetching membership for profile ID: {profile_id}")
    conn = sqlite3.connect("RZADatabase.db")
    cur = conn.cursor()
    
    cur.execute("SELECT last_login_timestamp FROM Profile WHERE Profile_ID = ?", (profile_id,))
    last_login_timestamp_result = cur.fetchone()
    print(f"Last login timestamp result: {last_login_timestamp_result}")

    if last_login_timestamp_result:
        last_login_timestamp = last_login_timestamp_result[0]
        print(f"Last login timestamp: {last_login_timestamp}")

        if last_login_timestamp:
            # query to filter memberships added after the last login
            cur.execute("""
                SELECT Type_SorG, Price
                FROM Membership
                WHERE Profile_ID = ? AND Membership_Timestamp > ?
                ORDER BY Membership_ID DESC """, (profile_id, last_login_timestamp))
            memberships = cur.fetchall()
            print(f"Fetched memberships since last login: {memberships}")
            return memberships

    return []   

#create function to connect with database and insert the membership information to database basket table    
def insert_membershiptobasket(profile_id, membership_data):
    conn = sqlite3.connect('RZADatabase.db') 
    cursor = conn.cursor()

    for item_data in membership_data:
        member_id = get_membership_id(profile_id)
        if item_data[1] > 0: 
            cursor.execute('''
                INSERT INTO basket (Profile_ID, Membership_ID, prices, items)
                VALUES (?, ?, ?, ?)
            ''', (profile_id, member_id, item_data[1], item_data[0])) 
    conn.commit()
    conn.close()

# create function to connect with database and fetch the membership id from database
def get_membership_id(profile_id):
    conn = sqlite3.connect('RZADatabase.db')
    cursor = conn.cursor()
    query = "SELECT Membership_ID FROM Membership WHERE Profile_ID = ?"
    cursor.execute(query, (profile_id,))
    result = cursor.fetchone()  
    conn.close()
    if result:
        return result[0] 
    else:
        return None  

# create function to fetch room availability 
def get_room_availability(date):
    available_single = 5  
    available_double = 3  
    return available_single, available_double