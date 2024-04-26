import sqlite3

'''
Create the database
'''
def create_database():
    conn = sqlite3.connect("RZADatabase.db")
    conn.close()

'''
All the table creation
'''
# create user table     
def create_account_table():
    conn = sqlite3.connect("RZADatabase.db")# connect to  database 
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE User (
            User_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Username VARCHAR(50),
            FirstName VARCHAR(50),
            LastName VARCHAR(50),
            Email VARCHAR(50),
            Postcode VARCHAR(50),
            Password VARCHAR(50))''')
    conn.commit()
    conn.close()

# create table profile table
def EXISTS_Profile():
    conn = sqlite3.connect("RZADatabase.db") # connect to  database 
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS Profile (
  Profile_ID INTEGER PRIMARY KEY AUTOINCREMENT,
  User_ID INTEGER,
  Registration_Date DATE,
  Activity_History TEXT,
  Reward_Points INTEGER,
  last_login_timestamp DATETIME)''')
    conn.commit() # Making the action stay
    conn.close() # closing the table

#create membership table    
def EXISTS_Membership():
    conn = sqlite3.connect("RZADatabase.db") # connect to  database 
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS Membership (
      Aduld_Child TEXT,
      Type_SorG TEXT,
      Price REAL,
      Membership_ID INTEGER PRIMARY KEY AUTOINCREMENT,
      Membership_Timestamp DATETIME ,
      Profile_ID INTEGER,
      FOREIGN KEY (Profile_ID) REFERENCES Profile(Profile_ID))''')
    conn.commit() # Making the action stay
    conn.close() # closing the table

#create book hote room    
def Book_Hotel_Room():
    conn = sqlite3.connect("RZADatabase.db")# connect to  database 
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS Book_Hotel_Room (
  Booking_ID INTEGER PRIMARY KEY AUTOINCREMENT,
  Profile_ID INTEGER,
  Check_in DATE,
  Check_out DATE,
  Number_Guests INTEGER,
  Room_type VARCHAR(50),
  Number_Days INTEGER,
  Total_Price DECIMAL(10, 2), 
  Quantity INTEGER,              
  Purchase_Timestamp DATETIME ,              
  Room_ID INTEGER,
  FOREIGN KEY (Profile_ID) REFERENCES Profile(User_ID),
  FOREIGN KEY (Room_ID) REFERENCES Availability_Room(Room_ID))''')
    conn.commit() # Making the action stay
    conn.close() # closing the table

# create ticket table 
def recreate_ticket_table():
    conn = sqlite3.connect("RZADatabase.db")# connect to  database 
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE Ticket (
        Ticket_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Profile_ID INTEGER,
        Date DATE,
        Slot_Time TIME,
        Price DECIMAL(10, 2),
        Ticket_type VARCHAR(50),
        Quantity INTEGER, 
        Purchase_Timestamp DATETIME,
        FOREIGN KEY (Profile_ID) REFERENCES Profile(User_ID))''')
    conn.commit()
    conn.close()
    
# create basket table
def EXISTS_Basket():
    conn = sqlite3.connect("RZADatabase.db") # connect to  database 
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS Basket (
  Basket_ID INTEGER PRIMARY KEY AUTOINCREMENT,
  Profile_ID INTEGER,
  User_ID INTEGER,
  Membership_ID INTEGER,
  Booking_ID INTEGER,
  Ticket_ID INTEGER,
  Code_ID INTEGER,
  quantities VARCHAR(255), 
  items VARCHAR(255), 
  prices VARCHAR(255),
  total FLOAT,
  Final_total FLOAT, 
  basket_Timestamp DATETIME, 
  FOREIGN KEY (User_ID) REFERENCES Profile(User_ID),
  FOREIGN KEY (Profile_ID) REFERENCES Profile(Profile_ID),
  FOREIGN KEY (Membership_ID) REFERENCES Membership(Membership_ID),
  FOREIGN KEY (Booking_ID) REFERENCES Book_Hotel_Room(Booking_ID),
  FOREIGN KEY (Ticket_ID) REFERENCES Ticket(Ticket_ID),
  FOREIGN KEY (Code_ID) REFERENCES Discount_Code(Code_ID))''')
    conn.commit() # Making the action stay
    conn.close() # closing the table

# create discount table     
def EXISTS_Discount_Code():
    conn = sqlite3.connect("RZADatabase.db")# connect to  database 
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS Discount (
      Code_ID INTEGER PRIMARY KEY AUTOINCREMENT,
      Code VARCHAR(20),
      Discount_Percentage DECIMAL(5, 2),
      Profile_ID INTEGER,
      Reward_Points INTEGER,          
      FOREIGN KEY (Profile_ID) REFERENCES Profile(User_ID),
      FOREIGN KEY (Reward_Points ) REFERENCES Profile(User_ID))
    ''')
    conn.commit() # Making the action stay
    conn.close() # closing the table
   
# create availability room     
def EXISTS_Availability_Room():
    conn = sqlite3.connect("RZADatabase.db")# connect to  database 
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS Availability_Room (
  Room_ID INTEGER PRIMARY KEY AUTOINCREMENT,
  Room_Type VARCHAR(50),
  Number_Guests INTEGER,
  Check_in DATE,
  Check_out DATE)''')
    conn.commit() # Making the action stay
    conn.close() # closing the table

recreate_ticket_table()
create_database()
create_account_table()
Book_Hotel_Room()
EXISTS_Discount_Code()
EXISTS_Availability_Room()
EXISTS_Membership()
EXISTS_Basket()
EXISTS_Profile()



