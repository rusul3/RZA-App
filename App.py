from cgi import test
import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from tkinter import font
from DatabaseFunctions import *
from PIL import Image, ImageTk
from tkinter import messagebox
from tkcalendar import Calendar
import datetime
from tkinter import scrolledtext
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import cv2
import os
import pyttsx3
import hashlib


# Create root screen for the front end app
root = Tk()
root.geometry("700x800")
root.resizable(False, False)
root.config(bg="#FFFFFF")

# store users info in variables
_user = ""
_password = ""
_postcode = ""
_email = ""
_user_id = ""
_lastname = ""
_firstnamr = ""
profile_id = ""

# Declare theme state globally for the dark mood 
is_dark_theme = False
photo_dark = None
photo_light = None
toggle_button = None

# load and open the photo function 
def load_images():
    global photo_light, photo_dark
    # Load and resize the icon image for dark theme
    image = Image.open("accessibility.png")
    image_dark = image.resize((30, 30))
    photo_dark = ImageTk.PhotoImage(image_dark)
    # Load and resize the icon image for light theme
    image_light = Image.open("accessibility.png")  
    image_light = image_light.resize((30, 30))
    photo_light = ImageTk.PhotoImage(image_light)

#create the dark mood and light mood function
def toggle_theme():
    global toggle_button, photo_dark, photo_light, is_dark_theme
    if is_dark_theme:
        # Switch to light theme
        root.config(bg='white')
        mainFrame.config(bg='white')
        toggle_button.config(image=photo_light, bg='white')  # Use light theme icon
        is_dark_theme = False
    else:
        # Switch to dark theme
        root.config(bg='black')
        mainFrame.config(bg='black')
        toggle_button.config(image=photo_dark, bg='black')  # Use dark theme icon
        is_dark_theme = True

#create the welcome page function 
def starter_screen():
    global mainFrame
    global profileButton
    global toggle_button
    # Load image
    image = Image.open("logo.jpg")
    image = image.resize((150, 70))
    photo = ImageTk.PhotoImage(image)
    # Create label with the image
    logo = Label(root, image=photo)
    logo.image = photo
    logo.place(x=0, y=0)
    # Nav main bar
    navFrame = tk.Frame(root, bg = '#8FBB6C')
    navFrame.place(width=545, height=60, x=151, y=3)
    # Nav buttons
    #create the account button
    AccountButton = tk.Button(navFrame, text="Account", fg='white', font=("Times New Roman", 12), bg = '#8FBB6C', command=Account_p)
    AccountButton.focus_set()
    AccountButton.bind('<Return>', lambda event: Account_p()) # accesible to keybord
    #create the plan your visite button
    plan_yourvisitButton = tk.Button(navFrame, text="Plan Your Visit ", fg='white', font=("Times New Roman", 12), bg = '#8FBB6C', command=Plan_p)
    plan_yourvisitButton.focus_set()
    plan_yourvisitButton.bind('<Return>', lambda event: Plan_p()) # accesible to keybord
    #create the offers button
    offersButton = tk.Button(navFrame, text="Offers", fg='white', font=("Times New Roman", 12), bg = '#8FBB6C', command=offers_p)
    offersButton.focus_set()
    offersButton.bind('<Return>', lambda event: offers_p()) # accesible to keybord
    #create the about us button
    AboutButton = tk.Button(navFrame, text="About us", fg='white', font=("Times New Roman", 12), bg = '#8FBB6C', command=about_p)
    AboutButton.focus_set()
    AboutButton.bind('<Return>', lambda event: about_p()) # accesible to keybord
    #create the plan your Educational Visits button
    educational_visitsButton = tk.Button(navFrame, text="Educational Visits", fg='white', font=("Times New Roman", 12), bg = '#8FBB6C', command=educationvisit_p)
    educational_visitsButton.focus_set()
    educational_visitsButton.bind('<Return>', lambda event: educationvisit_p()) # accesible to keybord

    #profile button
    # Load the profile icon image
    image = Image.open("account.png")
    image = image.resize((40, 40), Image.LANCZOS)
    photo = ImageTk.PhotoImage(image)
    # Creating the Profile button with an icon
    PButton = tk.Button(navFrame, image=photo, compound="left", bg='#8FBB6C', command=lambda: load_profile_data(_user_id) if _user_id else messagebox.showerror("Error", "Please login to view profile."))
    PButton.focus_set()
    PButton.bind('<Return>', lambda event: load_profile_data(_user_id) if _user_id else messagebox.showerror("Error", "Please login to view profile.") )
    PButton.photo = photo
        
    #help button
    # Load the help icon image
    image = Image.open("info-center.png")
    image = image.resize((40, 40), Image.LANCZOS)
    photo = ImageTk.PhotoImage(image)
    # Creating the help button with an icon
    HButton = tk.Button(navFrame, image=photo, compound="left", bg = '#8FBB6C', command=help_p)
    HButton.photo = photo
    
    #basket button
    # Load the basket icon image
    image = Image.open("shopping-cart.png")
    image = image.resize((40, 40), Image.LANCZOS)
    photo = ImageTk.PhotoImage(image)
    #Creating the basket button with an icon
    BButton = tk.Button(navFrame, image=photo, compound="left", bg = '#8FBB6C', command=lambda:basket_p(profile_id)if profile_id else messagebox.showerror("Error", "Please login to view profile to open basket."))
    BButton.focus_set()
    BButton.bind('<Return>', lambda event: basket_p(profile_id)if profile_id else messagebox.showerror("Error", "Please login to view profile to open basket.") )
    BButton.photo = photo
    #place the buttons
    AccountButton.place(width=60, height=60, x=0, y=0)
    plan_yourvisitButton.place(width=100, height=60, x=60, y=0)
    offersButton.place(width=45, height=60, x=160, y=0)
    AboutButton.place(width=60, height=60, x=205, y=0)
    educational_visitsButton.place(width=115, height=60, x=265, y=0)
    PButton.place(width=50, height=60, x=380, y=0)
    HButton.place(width=50, height=60, x=430, y=0)
    BButton.place(width=65, height=60, x=480, y=0)
    # put the button in list to help acceisble them to keyboard
    buttons = [ AccountButton, plan_yourvisitButton, offersButton, AboutButton, educational_visitsButton, PButton, HButton, BButton ]
    def move_focus(button, direction):
        index = buttons.index(button)
        next_index = (index + direction) % len(buttons)
        buttons[next_index].focus_set()
    # Bind Left and Right arrow keys for navigation
    for button in buttons:
        button.bind('<Left>', lambda event, b=button: move_focus(b, -1))
        button.bind('<Right>', lambda event, b=button: move_focus(b, 1))

    # Where the myjority of content will fit in so create the frame 
    mainFrame =tk.Frame(root, bg="#FFFFFF")
    mainFrame.place(width=700, height=800, x=0, y=70) 
    #welcome photo
    image1 = Image.open("bird.jpeg")
    image1 = image1.resize((700, 450))
    photo = ImageTk.PhotoImage(image1)
    #create label with the image
    w_photo = Label(mainFrame, image=photo)
    w_photo.image = photo
    w_photo.place(x=0, y=0)
    #welcome message
    welcome1 = tk.Label(mainFrame, text="Welcome to Riget Zoo Adventure ,Dive into",fg='#2B8D06', font=("Times New Roman", 24), bg="white")
    welcome1.place(x=60, y=480)
    welcome2 = tk.Label(mainFrame, text="an Unforgettable Wild Expedition !",fg='#2B8D06', font=("Times New Roman", 24), bg="white")
    welcome2.place(x=120, y=530)
    # create the buy ticket button
    openButton = tk.Button(mainFrame, text="Buy a Ticket for Your Adventure ", bg='#8FBB6C', command=ticket_p)
    openButton.focus_set()
    openButton.bind('<Return>', lambda event: ticket_p())
    openButton.place(width=350, height=50, x=160, y=600)
    # navigate down from the last navigation button to buy your ticket Button
    buttons[-1].bind('<Down>', lambda event: openButton.focus_set())
    # Navigate up from buy your ticket to the last navigation button
    openButton.bind('<Up>', lambda event: buttons[-1].focus_set())
    #load and open the accessibility photo
    image = Image.open("accessibility.png")
    image = image.resize((30, 30))
    photoD = ImageTk.PhotoImage(image)
    # create the accessiblity button
    toggle_button = tk.Button(mainFrame, image=photoD, font=('Helvetica', 24),bg='#8FBB6C', command=toggle_theme)
    toggle_button.place(y=600)
    
    # Run the Tkinter event loop
    root.mainloop() 

import datetime # reimport the datetime library because code miss it frome the top  
#create log in verify functions
def login_verify(user, pword):
    if not user or not pword :
        userIncorect.config(text="All fields are required.")
        return
    hashed_input_password = hashlib.sha256(pword.encode()).hexdigest()  # Hash the input passwor
    userInfo = get_user_info(user, hashed_input_password)# use get_user_info(usr, pword) function from model DatabaseFunctions to check the user information
    # validation for empty fields and proper email format
    if userInfo:
        global _user, _password, _postcode, _email, _user_id
        _user, _password, _postcode, _email, _user_id = userInfo
        _user = userInfo[0]
        _password = userInfo[1]
        _postcode = userInfo[2]
        _email = userInfo[3]
        userIncorect.config(text="Nice to see you again,enjoy!")
        if _user_id:
            load_profile_data(_user_id)
            # Log the login event
            login_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            update_activity_history(_user_id, f"Login at {login_datetime}")
            # to login verification logic
            update_last_login_timestamp(_user_id)
        else:
            userIncorect.config(text="User ID not found.")
    else:
        userIncorect.config(text="Username or Password Incorrect")

#create register verify function 
def register_verify(user, pword, pcode, email, lastname, firstname):
    # validation for empty fields and proper email format
    if not user or not pword or not pcode or not email or not lastname or not firstname:
        accountExists.config(text="All fields are required.")
        return  # Stop the function if any field is empty
    if '@' not in email:
        accountExists.config(text="Invalid email format.")
        return  # Stop the function if email does not contain '@'
    if not password_check(password):
        return  # Stop if password is invalid
    # Continue with the registration if all validations pass
    if not check_username_exists(user):
        hashed_password = hashlib.sha256(pword.encode()).hexdigest()  # Hash the password
        create_new_user(user, hashed_password, pcode, email, lastname, firstname) # use this function from model DatabaseFunctions to creat new account
        global _user, _password, _postcode, _email, _firstnamr, _lastname, _user_id

        _user = user
        _password = pword
        _postcode = pcode
        _email = email
        _firstnamr = firstname
        _lastname = lastname
        _user_id = get_new_user_id(user) # use this function from model DatabaseFunctions to fetch user id from database
        # update UI components or proceed with next steps
        if _user_id:
            accountExists.config(text="Registration successful.")
            load_profile_data(_user_id)  # Load profile after confirming user ID is valid
            messagebox.showinfo("Note","Thank you! Please log in after registration to save your points.")
             # send welcome email
            sender_email = "RigetZooAdventures@outlook.com"
            sender_password = "12qw##12QW##" 
             # email content
            email_body = f"Hello {_firstnamr} {_lastname},\n\n" \
                         "Thank you for registering with us. Here are your registration details:\n" \
                         f"Username: {_user}\n" \
                         f"Email: {_email}\n" \
                         f"Postcode: {_postcode}\n\n" \
                         "Welcome to Riget Zoo Adventures!"
            email_subject = "Welcome to Riget Zoo Adventures"
        
            send_email(email, email_subject, email_body, sender_email, sender_password )
        else:
            accountExists.config(text="Error fetching user ID.")
        load_profile_data(_user_id)
    else:
        accountExists.config(text="Account already exists.")
#create send email function when the user cretae new account         
def send_email(recipient, subject, body, sender_email, sender_password):
    # SMTP server configuration for Outlook.com
    smtp_server = 'smtp.office365.com'
    smtp_port = 587  # or 465 for SSL

    # Create MIME multipart message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient
    message["Subject"] = subject
    message.attach(MIMEText(body, 'plain'))

    try:
        # establish a secure session with the server
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # upgrade the connection to secure
            server.login(sender_email, sender_password)
            server.send_message(message)
            print("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")
        
#create the show information of user in his profile function 
def load_profile_data(user_id):
    if not user_id:
        messagebox.showerror("Error", "Invalid user ID.")
        return
    profile_data = get_profile(user_id) # use get_profile(user_id) function from model DatabaseFunctions to show customer informations
    print("Profile Data:", profile_data)
    # check if profile data is not None
    if not profile_data:
        messagebox.showerror("Error", "No profile data found for the user.")
        return
    global profileFrame
    profileFrame = tk.Frame(root, bg="#FFFFFF")
    profileFrame.place(width=700, height=800, x=0, y=70)
    display_profile_data(profileFrame, profile_data)
     # button to open the update form
    updateButton = tk.Button(profileFrame, text="Update Profile", command=lambda: open_update_form(user_id, profileFrame))
    updateButton.grid(row=10, column=1)
    # inside the load_profile_data function after setting up the profile frame
    deleteButton = tk.Button(profileFrame, text="Delete Profile", command=lambda: delete_profile(user_id))
    deleteButton.grid(row=11, column=1)
    # log out button
    logoutButton = tk.Button(profileFrame, text="Log Out", command=log_out)
    logoutButton.grid(row=12, column=1)

# show the informatopn of user in profile page 
def display_profile_data(profileFrame, profile_data):
    # Clear existing data in the frame
    for widget in profileFrame.winfo_children():
        widget.destroy()

    fields = ['Username', 'First Name', 'Last Name', 'Email', 'Postcode', 'Password', 'Registration Date', 'Activity History', 'Reward Points']
    for i, field in enumerate(fields):
        data = profile_data[i] if i < len(profile_data) else "N/A"
        tk.Label(profileFrame, text=f"{field}:", bg="white").grid(row=i, column=0, sticky='w')
        tk.Label(profileFrame, text=data, bg="white").grid(row=i, column=1, sticky='w')
    #back button 
    storeBackButton = tk.Button(profileFrame, text="<-", bg="#8FBB6C", command=starter_screen)
    storeBackButton.place(width=70, height=30, y=550, x=18)

#update the profile     
def open_update_form(user_id, profileFrame):
    global updateFrame
    global new_password
    global new_postcode
    global new_email
    
    updateFrame = tk.Toplevel(root)
    updateFrame.title("Update Profile")
    # entry fields for new information
    new_password = tk.Entry(updateFrame, show="*")
    new_postcode = tk.Entry(updateFrame)
    new_email = tk.Entry(updateFrame)
    # labels
    tk.Label(updateFrame, text="New Password:").grid(row=0, column=0)
    new_password.grid(row=0, column=1)
    tk.Label(updateFrame, text="New Postcode:").grid(row=1, column=0)
    new_postcode.grid(row=1, column=1)
    tk.Label(updateFrame, text="New Email:").grid(row=2, column=0)
    new_email.grid(row=2, column=1)
    # update button now also passes profileFrame for refreshing the profile view
    updateButton = tk.Button(updateFrame, text="Update", command=lambda: refresh(user_id))
    updateButton.grid(row=3, column=1)

#to get the update information function    
def refresh(user_id):
    edit_information(user_id, new_password.get(), new_postcode.get(), new_email.get())
    updateFrame.destroy()  # Cclose the update form
    profile_data = get_profile(user_id)  # fetch updated profile data
    display_profile_data(profileFrame, profile_data)    

#delet profile function
def delete_profile(user_id):
    # Code to delete the profile from the database or storage
    global _user_id
    delete_profile_data(user_id) 
    _user_id = None
    messagebox.showinfo("Success", "Profile deleted successfully.")
    profileFrame.destroy()  # Close the profile frame
    starter_screen()

#log out from profile function 
def log_out():
    # clear any session data 
    global _user_id
    _user_id = None
    profileFrame.destroy()  
    starter_screen()

# function to validate the password
def password_check(_password):
    special_ch = ['~', '`', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '+', '=', '{', '}', '[', ']', '|', '\\', '/', ':', ';', '"', "'", '<', '>', ',', '.', '?']
    name = _password.get()
    if not any(ch in special_ch for ch in name):
                accountExists.config(text="special character required")
                return False
    if not any(ch.isupper() for ch in name):
        accountExists.config(text="uppercase character required!") 
        return False
    if not any(ch.islower() for ch in name):
        accountExists.config(text="lowercase character required!")  
        return False
    if not any(ch.isdigit() for ch in name):
        accountExists.config(text="number required") 
        return False
    if len(name) < 8:
        accountExists.config(text="minimum of 8 characters")
        return False
      
    return True
       
# global variable to track the account frame
global accountFrame
accountFrame = None        
#create the account page and toggle the account frame 
def Account_p():
    global accountFrame
    # check if the account frame already exists 
    if accountFrame is not None:
        # destroy the existing account frame to hide it
        accountFrame.destroy()
        # reset accountFrame to None to indicate it's no longer being displayed
        accountFrame = None
    else:
        # page farme
        accountFrame = tk.Frame(root, bg = '#FFFFFF')
        accountFrame.place(width=300, height=250, x=151, y=65)
        # Buttons
        RegistrationButton = tk.Button(accountFrame, text="Registration", bg = '#8FBB6C', command=Registration_p)
        RegistrationButton.focus_set()
        RegistrationButton.bind('<Return>', lambda event: Registration_p()) # accesible to keybord
        
        LogInButton = tk.Button(accountFrame, text="LogIn", bg = '#8FBB6C', command=login_p)
        LogInButton.focus_set()
        LogInButton.bind('<Return>', lambda event: login_p()) # accesible to keybord
        
        MembershipButton = tk.Button(accountFrame, text="Membership", bg = '#8FBB6C', command=membership_p)
        MembershipButton.focus_set()
        MembershipButton.bind('<Return>', lambda event: membership_p()) # accesible to keybord
        
        #place the buttons in page
        RegistrationButton.place(width=215, height=50, x=40, y=20)
        LogInButton.place(width=215, height=50, x=40, y=80)
        MembershipButton.place(width=215, height=50, x=40, y=140)

        buttons = [RegistrationButton, LogInButton, MembershipButton]
        def move_focus(button, direction):
         index = buttons.index(button)
         next_index = (index + direction) % len(buttons)
         buttons[next_index].focus_set()

        # Bind Left and Right arrow keys for navigation
        for button in buttons:
         button.bind('<Down>', lambda event, b=button: move_focus(b, -1))
         button.bind('<Up>', lambda event, b=button: move_focus(b, 1))
        
            
#create the registration page  
def Registration_p():
    global accountExists
    global password
    # page farme
    RegistrationFrame = tk.Frame(accountFrame, bg = '#8FBB6C')
    RegistrationFrame.place(width=300, height=250, x=0, y=0)
    #labels
    regLabel = tk.Label(RegistrationFrame, text="Registration",font=("Times New Roman", 12), bg='#8FBB6C')
    userLabel = tk.Label(RegistrationFrame, text="User name*",bg='#8FBB6C', font=("Times New Roman", 12))
    FirstnameLabel = tk.Label(RegistrationFrame, text="First name *", bg='#8FBB6C', font=("Times New Roman", 12))
    LastnameLabel = tk.Label(RegistrationFrame, text="Last name *", bg='#8FBB6C', font=("Times New Roman", 12))
    passwordLabel = tk.Label(RegistrationFrame, text="Password *", bg='#8FBB6C', font=("Times New Roman", 12))
    postcodeLabel = tk.Label(RegistrationFrame, text="Postcode *", bg='#8FBB6C', font=("Times New Roman", 12))
    emailLabel = tk.Label(RegistrationFrame, text="Email       *", bg='#8FBB6C', font=("Times New Roman", 12))
    accountExists = tk.Label(RegistrationFrame, bg='#8FBB6C', fg='red')
    inflabelpassword = tk.Label (RegistrationFrame,text="must be minimum of 8 characters", bg='#8FBB6C', font=("Times New Roman", 10))
    inflabelpassword1 = tk.Label (RegistrationFrame,text="1 lowercase, 1 number ", bg='#8FBB6C',font=("Times New Roman", 10))
    inflabelpassword2 = tk.Label (RegistrationFrame,text="1 special character,1 uppercase", bg='#8FBB6C', font=("Times New Roman", 10))

    # entry bars
    user = tk.Entry(RegistrationFrame)
    password = tk.Entry(RegistrationFrame, show="*")
    postcode = tk.Entry(RegistrationFrame)
    first_name = tk.Entry(RegistrationFrame)
    last_name = tk.Entry(RegistrationFrame)
    email = tk.Entry(RegistrationFrame)

    # Button
    RegistrationButton = tk.Button(RegistrationFrame, text="Registration", command= lambda: [register_verify(user.get(), password.get(), postcode.get(), email.get(), first_name.get(),last_name.get())])
    RegistrationButton.place(width=210, height=35, x=50, y=210)

    # layout the label and entry
    regLabel.place(width=100, x=100, y=0)
    userLabel.place(width=100, x=20, y=25)
    user.place(width=150, x=105, y=25)
        
    FirstnameLabel.place(width=100, x=20, y=45)
    first_name.place(width=150, x=105, y=45)
        
    LastnameLabel.place(width=100, x=20, y=65)
    last_name.place(width=150, x=105, y=65)
        
    passwordLabel.place(width=100, x=20, y=85)
    password.place(width=150, x=105, y=85)
        
    emailLabel.place(width=100, x=20, y=150)
    email.place(width=150, x=105, y=150)
        
    postcodeLabel.place(width=100, x=20, y=170)
    postcode.place(width=150, x=105, y=170)
        
    inflabelpassword.place( x=100, y=100)
    inflabelpassword1.place( x=100, y=115)
    inflabelpassword2.place( x=100, y=130)

    accountExists.place(width=225, x=50, y=190)
    
#creat the login screen page
def login_p():
    global userIncorect
    global user
    global password
    # page farme
    loginFrame = tk.Frame(accountFrame, bg = '#8FBB6C')
    loginFrame.place(width=300, height=250, x=0, y=0)
    # Labels
    logLabel = tk.Label(loginFrame, text="Log In",font=("Times New Roman", 12), bg='#8FBB6C')
    userLabel = tk.Label(loginFrame, text="User name " ,font=("Times New Roman", 12), bg='#8FBB6C')
    passwordLabel = tk.Label(loginFrame, text="Password ",font=("Times New Roman", 12), bg='#8FBB6C')
    userIncorect = tk.Label(loginFrame, text="", bg='#8FBB6C')

    # Entry bars
    user = tk.Entry(loginFrame)
    password = tk.Entry(loginFrame, show="*")

    # Button
    loginButton = Button(loginFrame, text="Log In", command = lambda: login_verify(user.get(), password.get()))

    # Layout
    logLabel.place(width=100, x=100, y=0)
    
    userLabel.place(width=100, x=20, y=35)
    user.place(width=150, x=105, y=35)
    
    passwordLabel.place(width=100, x=20, y=65)
    password.place(width=150, x=105, y=65)
    
    loginButton.place(width=210, height=35, x=50, y=210)
    userIncorect.place(width=280, x=20, y=180)

#creat the membership page and all functions need 
is_dark_theme1 = False
photo_dark1 = None
photo_light1 = None
toggle_button1 = None   
#load and open photo function
def load_images1():
    global photo_light1, photo_dark1
    # Load and resize the icon image for both themes
    image = Image.open("accessibility2.png")
    resized_image = image.resize((30, 30))
    photo_dark1 = ImageTk.PhotoImage(resized_image)
    photo_light1 = ImageTk.PhotoImage(resized_image)
#creat darck mood function to membership page 
def toggle_theme1():
    global toggle_button1, is_dark_theme1, memberFrame
    if is_dark_theme1:
        # Switch to light theme
        memberFrame.config(bg='white')
        toggle_button1.config(image=photo_light1, bg='white')  # Use light theme icon
        is_dark_theme1 = False
    else:
        # Switch to dark theme
        memberFrame.config(bg='black')
        toggle_button1.config(image=photo_dark1, bg='black')  # Use dark theme icon
        is_dark_theme1 = True
# creat the read text function for the membership page 
def read_aloud():
    global text
    global reading_enabled
    global memberFrame
    global read_aloud_button

    engine = pyttsx3.init()
    if reading_enabled:
        # Read the text aloud
        engine.say(text)
        engine.runAndWait()
        reading_enabled = False
# the membership page
def membership_p():
    global memberFrame ,toggle_button1, text, profile_id
    load_images1() 
    # Where all contents will fit in
    memberFrame =tk.Frame(root, bg="#FFFFFF")
    memberFrame.place(width=700, height=800, x=0, y=70) 
    #welcome message
    welcome1 = tk.Label(memberFrame, text="Become a Riget Zoo Adventure Member today!.", bg="white",font=("Times New Roman", 18), fg="#8FBB6C")
    welcome1.place(x=5, y=10)
    # #text
    # text1 = tk.Label(memberFrame, text="Silver Membership", bg="white",font=("Times New Roman", 16))
    # text1.place(x=5, y=50)
    # define the long text
    text = ("*** Silver Membership ***\n"
            "* Unlimited year-round admission to Riget Zoo Adventure.\n"
                 "* Access to exclusive early morning tours.\n"
                 "* Discounts on special events, educational programs, and workshops.\n"
                 "* 10% off at zoo coffee and gift shops.\n" 
                 "* Priority booking for behind-the-scenes experiences.\n\n"
                 "*** Gold Membership ***\n"
                 "* All the benefits of the Explorer Membership.\n"
                 "* Invitations to VIP events and exhibit openings.\n"
                 "* One free behind-the-scenes experience per year.\n"
                 "* Recognition in the zoo's annual report. \n"
                 "* 15% off at zoo cafes and gift shops.")

    #label widget with the text, setting a fixed width and enabling word wrap
    label = tk.Label(memberFrame, text=text, wraplength=650, justify="left", bg="white", fg="black", padx=10, pady=10, font=("Times New Roman", 12))
    label.place(x=5, y=75)
    #image touse it in membership page 
    image1 = Image.open("membership .jpg")
    image1 = image1.resize((555, 100))
    photo = ImageTk.PhotoImage(image1)
    # create label with the image
    w_photo = Label(memberFrame, image=photo)
    w_photo.image = photo
    w_photo.place(x=60, y=350)
    profile_id = get_profile_id_by_user_id(_user_id)
    #buttons of sliver and golden and the place of them in page 
    sliverButton = tk.Button(memberFrame, text="buy Silver Membership for Adult ", bg = '#8FBB6C', command=lambda:add_membership_to_database('Silver for Adult', profile_id))
    goldButton = tk.Button(memberFrame, text="buy Gold Membership for Adult", bg = '#8FBB6C', command=lambda:add_membership_to_database('Gold for Adult', profile_id))
    sliverButton.place(width=250, height=40, x=60, y=500)
    goldButton.place(width=250, height=40, x=360, y=500)
    
    sliverButton = tk.Button(memberFrame, text="buy Silver Membership for Child ", bg = '#8FBB6C', command=lambda:add_membership_to_database('Silver for Child', profile_id))
    goldButton = tk.Button(memberFrame, text="buy Gold Membership for Child", bg = '#8FBB6C', command=lambda:add_membership_to_database('Gold for Child', profile_id))
    sliverButton.place(width=250, height=40, x=60, y=550)
    goldButton.place(width=250, height=40, x=360, y=550)
    # function to encapsulate adding to basket and showing message
    def add_to_basket():
        global profile_id
        profile_id = get_profile_id_by_user_id(_user_id)
        if not profile_id:
         messagebox.showerror("Error", "Please log in to buy the membership .")
         Account_p()
        else: 
            messagebox.showinfo("Success", "Your membership added to basket successfully.")
            basket_p(profile_id)
    #creat the basket button
    BasketButton = tk.Button(memberFrame, text=" Add To Basket ", bg='#8FBB6C', command=add_to_basket)
    BasketButton.place(width=350, heigh=40, x=190, y=610)
    #back button 
    storeBackButton = tk.Button(memberFrame, text="<-", bg="#8FBB6C", command=starter_screen)
    storeBackButton.place(width=70, height=30, y=680, x=18)
    #dark mood Button
    toggle_button1 = tk.Button(memberFrame, image=photo_light1, font=('Helvetica', 24),bg='#8FBB6C', command=toggle_theme1)
    toggle_button1.place(x=5, y=600)
    #load and open the photo to use it in accissablity button
    image = Image.open("auditory.png")
    image_resized = image.resize((30, 30))
    photo1 = ImageTk.PhotoImage(image_resized)
    photoD = tk.Label(memberFrame, image=photo1)
    photoD.image = photo1
    # bcreat the button to read the text aloud
    read_aloud_button = tk.Button(memberFrame, image=photo1, command=read_aloud, bg="white")
    read_aloud_button.place(x=600, y=600)
    
# Global variable to track the plan frame
global planFrame
planFrame = None        
#creat the plan your visit page and toggle the plan frame 
def Plan_p():
    global planFrame
    # check if the plan frame already exists and is being displayed
    if planFrame is not None:
        # destroy the existing frame to hide it
        planFrame.destroy()
        # Reset Frame to None to indicate it's no longer being displayed
        planFrame = None
    else:
        # page farme
        planFrame = tk.Frame(root, bg = '#FFFFFF')
        planFrame.place(width=300, height=280, x=210, y=65)
        # buttons
        OpeningTimeButton = tk.Button(planFrame, text="Opening Time ", bg = '#8FBB6C', command=OpeningTime_p)
        HotelButton = tk.Button(planFrame, text="Hotel", bg = '#8FBB6C', command=hotel_p)
        PricesButton = tk.Button(planFrame, text="Prices", bg = '#8FBB6C', command=prices_p)
        FoodandDrinkButton = tk.Button(planFrame, text="Food and Drink", bg = '#8FBB6C', command=fooddrink_p)
        MapButton = tk.Button(planFrame, text="Map", bg = '#8FBB6C', command=map_p)
        #place the buttons in page
        OpeningTimeButton.place(width=215, height=40, x=40, y=10)
        HotelButton.place(width=215, height=40, x=40, y=60)
        PricesButton.place(width=215, height=40, x=40, y=110)
        FoodandDrinkButton.place(width=215, height=40, x=40, y=160)
        MapButton.place(width=215, height=40, x=40, y=210)

#create the opening time page with all functions need 
is_dark_theme2 = False
photo_dark2 = None
photo_light2 = None
toggle_button1 = None   
#creat load and open function to use in dark mood 
def load_images2():
    global photo_light2, photo_dark2
    # Load and resize the icon image for both themes
    image = Image.open("accessibility2.png")
    resized_image = image.resize((30, 30))
    photo_dark2 = ImageTk.PhotoImage(resized_image)
    photo_light2 = ImageTk.PhotoImage(resized_image)
#creat the dark and light mood function 
def toggle_theme2():
    global toggle_button2, is_dark_theme2, openFrame
    if is_dark_theme2:
        # Switch to light theme
        openFrame.config(bg='white')
        toggle_button2.config(image=photo_light2, bg='white')  # Use light theme icon
        is_dark_theme2 = False
    else:
        # Switch to dark theme
        openFrame.config(bg='black')
        toggle_button2.config(image=photo_dark2, bg='black')  # Use dark theme icon
        is_dark_theme2 = True
#the opening Time page 
def OpeningTime_p():
    global openFrame ,toggle_button2
    load_images2() 
    # create the frame where all the content will fit in
    openFrame =tk.Frame(root, bg="#FFFFFF")
    openFrame.place(width=700, height=800, x=0, y=70) 
    # create a canvas widget1
    canvas1 = tk.Canvas(openFrame, width=300, height=50)
    canvas1.place(x=50,y=50)
    # draw a rectangle1 
    canvas1.create_rectangle(0, 0, 300, 50, fill="#8FBB6C", outline="#8FBB6C")
    # create a canvas widget2
    canvas2 = tk.Canvas(openFrame, width=300, height=50)
    canvas2.place(x=350,y=50)
    # draw a rectangle 2
    canvas2.create_rectangle(0, 0, 300, 50, fill="#8FBB6C", outline="#8FBB6C")
    # create a canvas widget3
    canvas2 = tk.Canvas(openFrame, width=300, height=50)
    canvas2.place(x=50,y=110)
    # draw a rectangle 3
    canvas2.create_rectangle(0, 0, 300, 50, fill="#8FBB6C", outline="#8FBB6C")
    # create a canvas widget4
    canvas2 = tk.Canvas(openFrame, width=300, height=50)
    canvas2.place(x=350,y=110)
    # draw a rectangle4 
    canvas2.create_rectangle(0, 0, 300, 50, fill="#8FBB6C", outline="#8FBB6C")
    # create a canvas widget5
    canvas2 = tk.Canvas(openFrame, width=300, height=50)
    canvas2.place(x=50,y=170)
    # draw a rectangle 5
    canvas2.create_rectangle(0, 0, 300, 50, fill="#8FBB6C", outline="#8FBB6C")
    # create a canvas widget6
    canvas2 = tk.Canvas(openFrame, width=300, height=50)
    canvas2.place(x=350,y=170)
    # draw a rectangle6 
    canvas2.create_rectangle(0, 0, 300, 50, fill="#8FBB6C", outline="#8FBB6C")
    #label (text) over the rectangle 1
    label = tk.Label(root, text="Open", font=("Times New Roman", 20), bg="#8FBB6C")
    label.place(x=150, y=130)
    #label (text) over the rectangle2
    label = tk.Label(root, text="10 am ", font=("Times New Roman", 20), bg="#8FBB6C")
    label.place(x=450, y=130)
    #label (text) over the rectangle3
    label = tk.Label(root, text="Close ", font=("Times New Roman", 20), bg="#8FBB6C")
    label.place(x=150, y=190)
    #label (text) over the rectangle4
    label = tk.Label(root, text="4:30 pm ", font=("Times New Roman", 20), bg="#8FBB6C")
    label.place(x=450, y=190)
    #label (text) over the rectangle5
    label = tk.Label(root, text="Last admission ", font=("Times New Roman", 20), bg="#8FBB6C")
    label.place(x=150, y=250)
    #label (text) over the rectangle6
    label = tk.Label(root, text="3 pm  ", font=("Times New Roman", 20), bg="#8FBB6C")
    label.place(x=450, y=250)
    
    #back button 
    storeBackButton = tk.Button(openFrame, text="<-", bg="#8FBB6C", command=starter_screen)
    storeBackButton.place(width=70, height=30, y=550, x=18)
    # dark mood Button
    toggle_button2 = tk.Button(openFrame, image=photo_light2, font=('Helvetica', 24),bg='#8FBB6C', command=toggle_theme2)
    toggle_button2.place(x=5, y=600)

#create the hotel page with all functions need
is_dark_theme3 = False
photo_dark3 = None
photo_light3 = None
toggle_button2 = None 
#creat load and open function to use in dark mood 
def load_images3():
    global photo_light3, photo_dark3
    # Load and resize the icon image for both themes
    image = Image.open("accessibility2.png")
    resized_image = image.resize((30, 30))
    photo_dark3 = ImageTk.PhotoImage(resized_image)
    photo_light3 = ImageTk.PhotoImage(resized_image)
#creat the dark and light mood function 
def toggle_theme3():
    global toggle_button3, is_dark_theme3, hotelFrame
    if is_dark_theme3:
        # Switch to light theme
        hotelFrame.config(bg='white')
        toggle_button3.config(image=photo_light2, bg='white')  # Use light theme icon
        is_dark_theme3 = False
    else:
        # Switch to dark theme
        hotelFrame.config(bg='black')
        toggle_button3.config(image=photo_dark2, bg='black')  # Use dark theme icon
        is_dark_theme3 = True      
#create the hotel page 
def hotel_p():
    global hotelFrame ,toggle_button3
    load_images3()
    #create the frame where all contents will fit in
    hotelFrame =tk.Frame(root, bg="#FFFFFF")
    hotelFrame.place(width=700, height=800, x=0, y=70) 
    #welcome photo
    image1 = Image.open("hote.jpg")
    image1 = image1.resize((700, 450))
    photo = ImageTk.PhotoImage(image1)
    # create label with the image
    w_photo = Label(hotelFrame, image=photo)
    w_photo.image = photo
    w_photo.place(x=0, y=100)
    #welcome message
    welcome1 = tk.Label(hotelFrame, text="Welcome to Hotel on site in Riget Zoo Adventure ",fg='#2B8D06', font=("Times New Roman", 24), bg="white")
    welcome1.place(x=25, y=10)
    welcome2 = tk.Label(hotelFrame, text="Your Sanctuary Amidst the Wonders of the Wild!",fg='#2B8D06', font=("Times New Roman", 24), bg="white")
    welcome2.place(x=30, y=50)
    # book room 
    openButton = tk.Button(hotelFrame, text="Book a Room ", bg='#8FBB6C',command=roomhotel_p)
    openButton.place(width=350, height=50, x=160, y=600) 
    #back button 
    storeBackButton = tk.Button(hotelFrame, text="<-", bg="#8FBB6C", command=starter_screen)
    storeBackButton.place(width=70, height=30, y=680, x=18)
    #dark mood Button
    toggle_button3 = tk.Button(hotelFrame, image=photo_light3, font=('Helvetica', 24),bg='#8FBB6C', command=toggle_theme3)
    toggle_button3.place(x=5, y=600)

#create the prices page with all functions need    
is_dark_theme4 = False
photo_dark4 = None
photo_light4 = None
toggle_button4 = None 
#creat load and open function to use in dark mood 
def load_images4():
    global photo_light4, photo_dark4
    # Load and resize the icon image for both themes
    image = Image.open("accessibility2.png")
    resized_image = image.resize((30, 30))
    photo_dark4 = ImageTk.PhotoImage(resized_image)
    photo_light4 = ImageTk.PhotoImage(resized_image)
#creat the dark and light mood function 
def toggle_theme4():
    global toggle_button4, is_dark_theme4, pricesFrame
    if is_dark_theme4:
        # Switch to light theme
        pricesFrame.config(bg='white')
        toggle_button4.config(image=photo_light4, bg='white')  # Use light theme icon
        is_dark_theme4 = False
    else:
        # Switch to dark theme
        pricesFrame.config(bg='black')
        toggle_button4.config(image=photo_dark4, bg='black')  # Use dark theme icon
        is_dark_theme4 = True  
#the prices page 
def prices_p():
    global pricesFrame ,toggle_button4
    load_images4()
    #create the frame where all contents will fit in
    pricesFrame =tk.Frame(root, bg="#FFFFFF")
    pricesFrame.place(width=700, height=800, x=0, y=70) 
    #welcome message
    welcome1 = tk.Label(pricesFrame, text="Welcome to Your Ultimate Guide for Adventures and Comfort!", font=("Times New Roman", 20), bg="white")
    welcome1.place(x=5, y=10)
    # define the long text
    long_text = ("Embark on an unforgettable journey with ease and confidence! Here, we bring you the latest"
             "and most competitive prices for both zoo adventures and hotel accommodations. Whether you're"
             "planning a family day out to explore the wonders of wildlife or looking for the perfect place "
             "to rest after a day's adventure, our comprehensive guide is designed to help you make the best choices without the hassle.")

    #label widget with the text, setting a fixed width and enabling word wrap
    label = tk.Label(pricesFrame, text=long_text, wraplength=650, justify="left", bg="white", fg="black", padx=10, pady=10)
    label.place(x=10, y=50)
    #photo
    image1 = Image.open("bigstock-Kids.jpg")
    image1 = image1.resize((642, 107))
    photo = ImageTk.PhotoImage(image1)
    # create label with the image
    w_photo = Label(pricesFrame, image=photo)
    w_photo.image = photo
    w_photo.place(x=20, y=130)
    #prices for the zoo
    welcome1 = tk.Label(pricesFrame, text="Prices for zoo ticket , offering you a glimpse into the animal kingdom that awaits your discovery.", font=("Times New Roman", 12), bg="white")
    welcome1.place(x=25, y=250)
    #create the rectangles use a canvas widget1
    canvas1 = tk.Canvas(pricesFrame, width=300, height=30)
    canvas1.place(x=25,y=280)
    # Draw a rectangle1 
    canvas1.create_rectangle(0, 0, 300, 30, fill="#8FBB6C", outline="#8FBB6C")
    # Create a canvas widget2
    canvas2 = tk.Canvas(pricesFrame, width=300, height=30)
    canvas2.place(x=350,y=280)
    # Draw a rectangle 2
    canvas2.create_rectangle(0, 0, 300, 30, fill="#8FBB6C", outline="#8FBB6C")
    # Create a canvas widget3
    canvas2 = tk.Canvas(pricesFrame, width=300, height=30)
    canvas2.place(x=25,y=320)
    # Draw a rectangle 3
    canvas2.create_rectangle(0, 0, 300, 30, fill="#8FBB6C", outline="#8FBB6C")
    # Create a canvas widget4
    canvas2 = tk.Canvas(pricesFrame, width=300, height=30)
    canvas2.place(x=350,y=320)
    # Draw a rectangle4 
    canvas2.create_rectangle(0, 0, 300, 30, fill="#8FBB6C", outline="#8FBB6C")
    # Create a canvas widget5
    canvas2 = tk.Canvas(pricesFrame, width=300, height=30)
    canvas2.place(x=25,y=360)
    # Draw a rectangle 5
    canvas2.create_rectangle(0, 0, 300, 30, fill="#8FBB6C", outline="#8FBB6C")
    # Create a canvas widget6
    canvas2 = tk.Canvas(pricesFrame, width=300, height=30)
    canvas2.place(x=350,y=360)
    # Draw a rectangle6 
    canvas2.create_rectangle(0, 0, 300, 30, fill="#8FBB6C", outline="#8FBB6C")
    # Create a canvas widget7
    canvas2 = tk.Canvas(pricesFrame, width=300, height=30)
    canvas2.place(x=25,y=400)
    # Draw a rectangle7
    canvas2.create_rectangle(0, 0, 300, 30, fill="#8FBB6C", outline="#8FBB6C")
    # Create a canvas widget8
    canvas2 = tk.Canvas(pricesFrame, width=300, height=30)
    canvas2.place(x=350,y=400)
    # Draw a rectangle8
    canvas2.create_rectangle(0, 0, 300, 30, fill="#8FBB6C", outline="#8FBB6C")
    #label (text) over the rectangle 1
    label = tk.Label(root, text="standard adult admission", font=("Times New Roman", 12), bg="#8FBB6C")
    label.place(x=90, y=355)
    #label (text) over the rectangle2
    label = tk.Label(root, text=" 22.5 £ ", font=("Times New Roman", 12), bg="#8FBB6C")
    label.place(x=450, y=355)
    #label (text) over the rectangle3
    label = tk.Label(root, text="standard child  ", font=("Times New Roman", 12), bg="#8FBB6C")
    label.place(x=90, y=395)
    #label (text) over the rectangle4
    label = tk.Label(root, text=" 16.85 £ ", font=("Times New Roman", 12), bg="#8FBB6C")
    label.place(x=450, y=395)
    #label (text) over the rectangle5
    label = tk.Label(root, text="standard student ", font=("Times New Roman", 12), bg="#8FBB6C")
    label.place(x=90, y=435)
    #label (text) over the rectangle6
    label = tk.Label(root, text=" 19.1 £ ", font=("Times New Roman", 12), bg="#8FBB6C")
    label.place(x=450, y=435)
    #label (text) over the rectangle7
    label = tk.Label(root, text="saver ticket(2 adults + 2 children) ", font=("Times New Roman", 12), bg="#8FBB6C")
    label.place(x=90, y=475)
    #label (text) over the rectangle8
    label = tk.Label(root, text=" 70.8 £ ", font=("Times New Roman", 12), bg="#8FBB6C")
    label.place(x=450, y=475)
    # Define the long text
    long_text = ("Pair your day with a comfortable stay by exploring our selection of hotel rooms, from cozy "
                 "singles to luxurious doubles, ensuring your relaxation is just as memorable as your day out.")

    #Label widget with the text, setting a fixed width and enabling word wrap
    label = tk.Label(pricesFrame, text=long_text, wraplength=650, justify="left", bg="white", fg="black", padx=10, pady=10, font=("Times New Roman", 12))
    label.place(x=25, y=460)
    # Create a canvas widget9
    canvas9 = tk.Canvas(pricesFrame, width=300, height=30)
    canvas9.place(x=25,y=520)
    # Draw a rectangle 9
    canvas9.create_rectangle(0, 0, 300, 30, fill="#8FBB6C", outline="#8FBB6C")
    
    # Create a canvas widget10
    canvas10 = tk.Canvas(pricesFrame, width=300, height=30)
    canvas10.place(x=350,y=520)
    # Draw a rectangle10
    canvas10.create_rectangle(0, 0, 300, 30, fill="#8FBB6C", outline="#8FBB6C")
    
    # Create a canvas widget11
    canvas11 = tk.Canvas(pricesFrame, width=300, height=30)
    canvas11.place(x=25,y=560)
    # Draw a rectangle1
    canvas11.create_rectangle(0, 0, 300, 30, fill="#8FBB6C", outline="#8FBB6C")
    
    # Create a canvas widget12
    canvas12 = tk.Canvas(pricesFrame, width=300, height=30)
    canvas12.place(x=350,y=560)
    # Draw a rectangle12
    canvas12.create_rectangle(0, 0, 300, 30, fill="#8FBB6C", outline="#8FBB6C")
    #label (text) over the rectangle9
    label = tk.Label(root, text="Single ", font=("Times New Roman", 12), bg="#8FBB6C")
    label.place(x=90, y=595)
    #label (text) over the rectangle10
    label = tk.Label(root, text="  75 £", font=("Times New Roman", 12), bg="#8FBB6C")
    label.place(x=450, y=595)
    #label (text) over the rectangle11
    label = tk.Label(root, text="Double ", font=("Times New Roman", 12), bg="#8FBB6C")
    label.place(x=90, y=635)
    #label (text) over the rectangle12
    label = tk.Label(root, text="  120 £ ", font=("Times New Roman", 12), bg="#8FBB6C")
    label.place(x=450, y=635)
    #back button 
    storeBackButton = tk.Button(pricesFrame, text="<-", bg="#8FBB6C", command=starter_screen)
    storeBackButton.place(width=70, height=30, y=680, x=18)
    # dark mood Button
    toggle_button4 = tk.Button(pricesFrame, image=photo_light4, font=('Helvetica', 24),bg='#8FBB6C', command=toggle_theme4)
    toggle_button4.place(x=5, y=600)

#create the food and drink page with all functions need     
is_dark_theme5 = False
photo_dark5 = None
photo_light5 = None
toggle_button5 = None  
#load and open photo to use it in the dark mood function
def load_images5():
    global photo_light5, photo_dark5
    # Load and resize the icon image for both themes
    image = Image.open("accessibility2.png")
    resized_image = image.resize((30, 30))
    photo_dark5 = ImageTk.PhotoImage(resized_image)
    photo_light5 = ImageTk.PhotoImage(resized_image)
#create the dark mood function 
def toggle_theme5():
    global toggle_button5, is_dark_theme5, fooddrinkFrame
    if is_dark_theme5:
        # Switch to light theme
        fooddrinkFrame.config(bg='white')
        toggle_button5.config(image=photo_light5, bg='white')  # Use light theme icon
        is_dark_theme5 = False
    else:
        # Switch to dark theme
        fooddrinkFrame.config(bg='black')
        toggle_button5.config(image=photo_dark5, bg='black')  # Use dark theme icon
        is_dark_theme5 = True  
#the food and drink page
def fooddrink_p():
    global fooddrinkFrame ,toggle_button5
    load_images5()
    #create the frame where all contents will fit in
    fooddrinkFrame =tk.Frame(root, bg="#FFFFFF")
    fooddrinkFrame.place(width=700, height=800, x=0, y=70) 
    #welcome message
    welcome1 = tk.Label(fooddrinkFrame, text="Welcome to the RZA  Culinary Oasis!", font=("Times New Roman", 20), bg="white")
    welcome1.place(x=5, y=5)
    # Define the long text
    long_text = ("Step into a world where exquisite flavors meet the wild - welcome to our Food and Drink haven "
                 "at Riget Zoo Adventures. As you journey through the wonders of nature, we invite you to indulge" 
                 "in a culinary adventure that complements the excitement of your exploration. Here, every sip and bite" 
                 "is part of your zoo adventure, curated to enhance your experience with us.")

    #label widget with the text, setting a fixed width and enabling word wrap
    label = tk.Label(fooddrinkFrame, text=long_text, wraplength=650, justify="left", bg="white", fg="black", padx=10, pady=10, font=("Times New Roman", 12))
    label.place(x=10, y=40) 
    # define the juice text
    long_text = (" *****     Juice Bar     *****  " 
                 " A Refreshing Escape ,Our juice bar offers a refreshing.")

    #label widget with the text, setting a fixed width and enabling word wrap
    label = tk.Label(fooddrinkFrame, text=long_text, wraplength=200, justify="left", bg="white", fg="black", padx=10, pady=10, font=("Times New Roman", 12))
    label.place(x=10, y=125) 
     # define the cafe text
    long_text = ("*****     Café Delights     ***** Sip and Savor "
                 "For those in search of warmth and comfort, our café awaits.")

    #label widget with the text, setting a fixed width and enabling word wrap
    label = tk.Label(fooddrinkFrame, text=long_text, wraplength=313, justify="left", bg="white", fg="black", padx=10, pady=10, font=("Times New Roman", 12))
    label.place(x=350, y=125)
    #photo of juice menu with zoom function
    def zoomed_image():
        zoomed_window = Toplevel()
        zoomed_window.title("Zoomed Image")
        image_large = image1.resize((500, 560))  # Larger size for the zoomed image
        photo_large = ImageTk.PhotoImage(image_large)
        label_large = Label(zoomed_window, image=photo_large)
        label_large.image = photo_large  #a reference
        label_large.pack()
    # Image setup
    image1 = Image.open("juice.png")
    image1 = image1.resize((250, 280))
    photo = ImageTk.PhotoImage(image1)
    w_photo = Label(fooddrinkFrame, image=photo)
    w_photo.image = photo  # a reference
    w_photo.place(x=10, y=195)
    # bind click event to the photo label to show a larger image on click
    w_photo.bind("<Button-1>", lambda event: zoomed_image())
    #photo of cafe menu with zoom function
    def zoomed_cafe():
        zoomed_window = Toplevel()
        zoomed_window.title("Zoomed Image")
        image_large = image2.resize((740, 540))  # Larger size for the zoomed image
        photo_large = ImageTk.PhotoImage(image_large)
        label_large = Label(zoomed_window, image=photo_large)
        label_large.image = photo_large  #a reference
        label_large.pack()
    # Image setup
    image2 = Image.open("coffeemenue.jpg")
    image2 = image2.resize((370, 270))
    photo = ImageTk.PhotoImage(image2)
    w_photo = Label(fooddrinkFrame, image=photo)
    w_photo.image = photo  # a reference
    w_photo.place(x=300, y=195)
    # bind click event to the photo label to show a larger image on click
    w_photo.bind("<Button-1>", lambda event: zoomed_cafe())
    
    # define the cafe text
    long_text = ("*****      Restaurant Experience       *****"
                 "Enjoy a meal that's as memorable as your day at the zoo," 
                 "with dishes that cater to every palate, from the adventurous" 
                 "eater to the comfort food enthusiast.")

    #label widget with the text, setting a fixed width and enabling word wrap
    label = tk.Label(fooddrinkFrame, text=long_text, wraplength=313, justify="left", bg="white", fg="black", padx=10, pady=10, font=("Times New Roman", 12))
    label.place(x=10, y=550)
    #photo of restaurant menu with zoom function
    def zoomed_rest():
        zoomed_window = Toplevel()
        zoomed_window.title("Zoomed Image")
        image_large = image3.resize((560, 520))  # Larger size for the zoomed image
        photo_large = ImageTk.PhotoImage(image_large)
        label_large = Label(zoomed_window, image=photo_large)
        label_large.image = photo_large  #a reference
        label_large.pack()
    # Image setup
    image3 = Image.open("restaurant.jpg")
    image3 = image3.resize((280, 260))
    photo = ImageTk.PhotoImage(image3)
    w_photo = Label(fooddrinkFrame, image=photo)
    w_photo.image = photo  # a reference
    w_photo.place(x=350, y=465)
    # bind click event to the photo label to show a larger image on click
    w_photo.bind("<Button-1>", lambda event: zoomed_rest())
    #back button 
    storeBackButton = tk.Button(fooddrinkFrame, text="<-", bg="#8FBB6C", command=starter_screen)
    storeBackButton.place(width=70, height=30, y=680, x=18)
    #dark mood Button
    toggle_button5 = tk.Button(fooddrinkFrame, image=photo_light5, font=('Helvetica', 24),bg='#8FBB6C', command=toggle_theme5)
    toggle_button5.place(x=5, y=640)

# create the active map with all buttons,photos and videos
def map_p():
    global map_image
    # initialize the map frame
    mapFrame = tk.Frame(root, bg="#FFFFFF")
    mapFrame.place(width=700, height=800, x=0, y=70)
    # load and display the map image
    image_path = "zoo map RZA.jpg"
    map_image = Image.open(image_path).resize((700, 500))
    photo = ImageTk.PhotoImage(map_image)
    map_label = tk.Label(mapFrame, image=photo)
    map_label.image = photo  #reference to avoid garbage collection
    map_label.place(x=0, y=0)

    # load the lion image
    lion_image = Image.open("lion.jpg")
    lion_image_resized = lion_image.resize((25, 25))
    lion_photo = ImageTk.PhotoImage(lion_image_resized)
    map_lion = tk.Label(mapFrame, image=lion_photo)
    map_lion.image = lion_photo  # reference to avoid garbage collection
    #create the button to the video
    video_button = tk.Button(mapFrame, image=lion_photo, bg = '#8FBB6C', command=lambda: play_video("lion_animal_-_114145 (540p).mp4", mapFrame))
    video_button.place(x=350, y=15)  # position to the lion on the map

    #cheetah icone
    Cheetah_image = Image.open("Cheetah.jpg")
    Cheetah_image_resized = Cheetah_image.resize((25, 25))
    Cheetah_photo = ImageTk.PhotoImage(Cheetah_image_resized)
    map_Cheetah = tk.Label(mapFrame, image=Cheetah_photo)
    map_Cheetah.image = Cheetah_photo  #reference to avoid garbage collection
    #create the button to the video
    Cheetah_button = tk.Button(mapFrame, image=Cheetah_photo, bg = '#8FBB6C', command=lambda: play_video("C_Video.mp4", mapFrame))
    Cheetah_button.place(x=390, y=30)  # Position to the cheetah on the map

    #Elephant icone
    Elephant_image = Image.open("Elephant.jpg")
    Elephant_image_resized = Elephant_image.resize((25, 25))
    Elephant_photo = ImageTk.PhotoImage(Elephant_image_resized)
    map_Elephant = tk.Label(mapFrame, image=Elephant_photo)
    map_Elephant.image = Elephant_photo  # reference to avoid garbage collection
    #create the button to the video
    Elephant_button = tk.Button(mapFrame, image=Elephant_photo, bg = '#8FBB6C', command=lambda: play_video("E_Video.mp4", mapFrame))
    Elephant_button.place(x=560, y=280)  # Position to the elephant on the map

    #Giraffe icone
    Giraffe_image = Image.open("Giraffe.jpg")
    Giraffe_image_resized = Giraffe_image.resize((25, 25))
    Giraffe_photo = ImageTk.PhotoImage(Giraffe_image_resized)
    map_Giraffe = tk.Label(mapFrame, image=Giraffe_photo)
    map_Giraffe.image = Giraffe_photo  #reference to avoid garbage collection
    #create the button to the video
    Giraffe_button = tk.Button(mapFrame, image=Giraffe_photo, bg = '#8FBB6C', command=lambda: play_video("G_Video.mp4", mapFrame))
    Giraffe_button.place(x=660, y=300)  # Position to the liongiraffe on the map

    #Hippopotamus icone
    Hippopotamus_image = Image.open("Hippopotamus.jpg")
    Hippopotamus_image_resized = Hippopotamus_image.resize((25, 25))
    Hippopotamus_photo = ImageTk.PhotoImage(Hippopotamus_image_resized)
    map_Hippopotamus = tk.Label(mapFrame, image=Hippopotamus_photo)
    map_Hippopotamus.image = Hippopotamus_photo  # reference to avoid garbage collection
    #create the button to the video
    Hippopotamus_button = tk.Button(mapFrame, image=Hippopotamus_photo, bg = '#8FBB6C', command=lambda: play_video("H_Video.mp4", mapFrame))
    Hippopotamus_button.place(x=580, y=109)  # Position to the Hippopotamus on the map

    #Rhinoceros icone
    Rhinoceros_image = Image.open("Rhinoceros.jpg")
    Rhinoceros_image_resized = Rhinoceros_image.resize((25, 25))
    Rhinoceros_photo = ImageTk.PhotoImage(Rhinoceros_image_resized)
    map_Rhinoceros = tk.Label(mapFrame, image=Rhinoceros_photo)
    map_Rhinoceros.image = Rhinoceros_photo  # reference to avoid garbage collection
    #create the button to the video
    Rhinoceros_button = tk.Button(mapFrame, image=Rhinoceros_photo, bg = '#8FBB6C', command=lambda: play_video("R_Video.mp4", mapFrame))
    Rhinoceros_button.place(x=430, y=210)  # Position the Rhinoceros on the map


    # Button to display information about animals and positioning below the map
    info_button = tk.Button(mapFrame, text="Learn about Lions",command=lambda: show_info("Lions", "Lions are social mammals that live in family groups called prides.",mapFrame))
    info_button.place(width=200, x=10, y=510)  
    
    info_button1 = tk.Button(mapFrame, text="Learn about Hippopotamus",command=lambda: show_info("Hippopotamus","Despite their stocky shape and short legs, hippos are incredibly fast swimmers \n and can run on land at speeds of up to 20 miles per hour over short distances.",mapFrame))
    info_button1.place(width=200, x=10, y=540)  
    
    info_button2 = tk.Button(mapFrame, text="Learn about Rhinoceros",command=lambda: show_info("Rhinoceros","their impressive horn, which is made from keratin,\n the same type of protein that makes up human hair and nails.", mapFrame))
    info_button2.place(width=200, x=10, y=570) 
    
    info_button3 = tk.Button(mapFrame, text="Learn about Elephant",command=lambda: show_info("Elephant","They communicate over long distances by producing a sub-sonic rumble\n that travels over the ground faster than sound through air.", mapFrame))
    info_button3.place(width=200, x=300, y=510)  
    
    info_button4 = tk.Button(mapFrame, text="Learn about Cheetah",command=lambda: show_info("Cheetah","Unlike other big cats, cheetahs cannot roar but instead purr,\n and they have semi-retractable claws that provide extra grip in their high-speed pursuits.", mapFrame))
    info_button4.place(width=200, x=300, y=540) 
    
    info_button5 = tk.Button(mapFrame, text="Learn about Giraffe",command=lambda: show_info("Giraffe","They are the tallest mammals on Earth, with necks that can be about 6 feet long and\n overall heights up to 18 feet for males.", mapFrame))
    info_button5.place(width=200, x=300, y=570)  
    
    # button to download the map image
    download_button = tk.Button(mapFrame, text="Download Map", command=download_map)
    download_button.place(x=550, y=510)  # Adjust position as needed

    # back button to return to the starter screen
    storeBackButton = tk.Button(mapFrame, text="<-", bg="#8FBB6C", command=starter_screen)
    storeBackButton.place(width=70, height=30, y=680, x=18)

#to download the map function
def download_map():
    global map_image
    try:
        # Get the path to the user's Downloads folder
        downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")

        # Check if the Downloads folder exists
        if not os.path.exists(downloads_folder):
            raise FileNotFoundError("Downloads folder not found")

        # Define the file path for the map image in the Downloads folder
        file_path = os.path.join(downloads_folder, "zoo_map_download.jpg")

        # Save the map image to the Downloads folder
        map_image.save(file_path)

        # Show a message indicating where the file is saved
        messagebox.showinfo("Map Downloaded", f"The map has been saved to:\n{file_path}")
    except Exception as e:
        # Show error message if saving fails
        messagebox.showerror("Error", f"Failed to save the map:\n{str(e)}")

#create function to review information about the animals
def show_info(title, content, mapFrame):
    """ Show information in a new pop-up window. """
    info_window = tk.Toplevel(mapFrame)
    info_window.title(title)
    # calculate the position relative to the main frame
    main_window_x = mapFrame.winfo_rootx()  # X coordinate of the main frame
    main_window_y = mapFrame.winfo_rooty()  # Y coordinate of the main frame
    main_window_width = mapFrame.winfo_width()  # Width of the main frame
    # set the position of the info window
    info_window_x = main_window_x + main_window_width + 20  # place it to the right with a padding of 20 pixels
    info_window_y = main_window_y
    # set the position of the info window
    info_window.geometry(f"+{info_window_x}+{info_window_y}")
    # create the label widget
    info_label = tk.Label(info_window, text=content, width=70, height=10)
    info_label.pack()  # pack to fill the available space

#to show the video about the animals when click the photo of the animals
def play_video(video_path, parent_frame):
    top = tk.Toplevel(parent_frame)
    top.title("Video Player")
    try:
        # open the video file
        cap = cv2.VideoCapture(video_path)
        # get the width and height of the video
        video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        video_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        # determine the scaling factor to fit the video within a 300x300 frame
        scale_factor = min(300 / video_width, 300 / video_height)
        # calculate the scaled dimensions
        scaled_width = int(video_width * scale_factor)
        scaled_height = int(video_height * scale_factor)
        canvas = tk.Canvas(top, width=scaled_width, height=scaled_height)
        canvas.pack()
        # list to hold the photo references
        photos = []
        def update_frame():
            ret, frame = cap.read()
            if ret:
                # resize the frame to fit the canvas size
                resized_frame = cv2.resize(frame, (scaled_width, scaled_height))
                photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)))
                photos.append(photo)  # reference to the photo
                canvas.create_image(0, 0, image=photo, anchor=tk.NW)
                top.after(33, update_frame)  # adjust frame delay based on the video's FPS (typically 30 FPS -> 33ms delay)
            else:
                cap.release()
                top.destroy()

        update_frame()
    except Exception as e:
        messagebox.showerror("Error", str(e))
        top.destroy()

#create the offers page and all the functions need    
is_dark_theme6 = False
photo_dark6 = None
photo_light6 = None
toggle_button6 = None  
#load and open the photo need to the dark mood 
def load_images6():
    global photo_light6, photo_dark6
    # Load and resize the icon image for both themes
    image = Image.open("accessibility2.png")
    resized_image = image.resize((30, 30))
    photo_dark6 = ImageTk.PhotoImage(resized_image)
    photo_light6 = ImageTk.PhotoImage(resized_image)
#create the dark mood function
def toggle_theme6():
    global toggle_button6, is_dark_theme6, offersFrame
    if is_dark_theme6:
        # switch to light theme
        offersFrame.config(bg='white')
        toggle_button6.config(image=photo_light6, bg='white')  # Use light theme icon
        is_dark_theme6 = False
    else:
        # switch to dark theme
        offersFrame.config(bg='black')
        toggle_button6.config(image=photo_dark6, bg='black')  # Use dark theme icon
        is_dark_theme6 = True  
#create the offers page
def offers_p():
    global offersFrame ,toggle_button6
    load_images6()
    # create the frame where all contents will fit in
    offersFrame =tk.Frame(root, bg="#FFFFFF")
    offersFrame.place(width=700, height=800, x=0, y=70) 
    #welcome message
    welcome1 = tk.Label(offersFrame, text="Welcome to Our Offers!", font=("Times New Roman", 20), bg="white")
    welcome1.place(x=5, y=5)
    # Define the long text
    text = ("Embark on a journey of exclusive benefits and delightful rewards with our special offers page! Designed" 
                 "with you in mind, our rewards program ensures that every interaction you have with us brings you closer" 
                 "to amazing discounts and special perks.\n"                                                               
                 "* Here's How You Can Earn Points:\n"
                 "1- Create an Account: Kickstart your adventure by signing up with us! Creating an account earns you an "   
                 "instant 5 points. It's our way of saying thank you for joining our family.\n"
                 "2- Daily Login: Keep the adventure alive every day! Each time you log in to your account, you'll earn 1point.\n"
                 "3- Ticket Purchases: Ready to explore the wonders of the zoo or relax in a comfortable hotel room? "  
                 "Every ticket purchase rewards you with 10 points.\n"
                 "* Unlocking Your Discounts:  \n"
                 "Turn Points into Savings: Your points are more than just numbers; they're keys to unlocking exclusive discounts.")

    #Label widget with the text, setting a fixed width and enabling word wrap
    label = tk.Label(offersFrame, text=text, wraplength=650, justify="left", bg="white", fg="black", padx=10, pady=10, font=("Times New Roman", 12))
    label.place(x=10, y=40)
    #photo of points table with zoom function
    def zoomed_points():
        zoomed_window = Toplevel()
        zoomed_window.title("Zoomed Image")
        image_large = image4.resize((690, 300))  # Larger size for the zoomed image
        photo_large = ImageTk.PhotoImage(image_large)
        label_large = Label(zoomed_window, image=photo_large)
        label_large.image = photo_large  # reference the photo
        label_large.pack()
    # Image setup
    image4 = Image.open("points table.jpg")
    image4 = image4.resize((335, 150))
    photo = ImageTk.PhotoImage(image4)
    w_photo = Label(offersFrame, image=photo)
    w_photo.image = photo  # a reference the photo
    w_photo.place(x=10, y=300)
    # bind click event to the photo label to show a larger image on click
    w_photo.bind("<Button-1>", lambda event: zoomed_points())
    #photo of points digram with zoom function
    def zoomed_digram():
        zoomed_window = Toplevel()
        zoomed_window.title("Zoomed Image")
        image_large = image5.resize((680, 600))  # larger size for the zoomed image
        photo_large = ImageTk.PhotoImage(image_large)
        label_large = Label(zoomed_window, image=photo_large)
        label_large.image = photo_large  #a reference the photo
        label_large.pack()
    # Image setup
    image5 = Image.open("points digram.jpg")
    image5 = image5.resize((340, 300))
    photo = ImageTk.PhotoImage(image5)
    w_photo = Label(offersFrame, image=photo)
    w_photo.image = photo  # a reference
    w_photo.place(x=350, y=300)
    # bind click event to the photo label to show a larger image on click
    w_photo.bind("<Button-1>", lambda event: zoomed_digram())
    #Summer Holidays discount : 30%
    welcome1 = tk.Label(offersFrame, text="*Summer Holidays discount : 30%", font=("Times New Roman", 12), bg="white")
    welcome1.place(x=10, y=500)
    #Half Terms discount: 20%
    welcome1 = tk.Label(offersFrame, text="*Half Terms discount: 20%", font=("Times New Roman", 12), bg="white")
    welcome1.place(x=10, y=540)
    #back button 
    storeBackButton = tk.Button(offersFrame, text="<-", bg="#8FBB6C", command=starter_screen)
    storeBackButton.place(width=70, height=30, y=680, x=18)
    # dark mood Button
    toggle_button6 = tk.Button(offersFrame, image=photo_light6, font=('Helvetica', 24),bg='#8FBB6C', command=toggle_theme6)
    toggle_button6.place(x=5, y=640)

#create the about us page and all functions need     
is_dark_theme7 = False
photo_dark7 = None
photo_light7 = None
toggle_button7 = None   
#load and open photo to use in dark mood function
def load_images7():
    global photo_light7, photo_dark7
    # Load and resize the icon image for both themes
    image = Image.open("accessibility2.png")
    resized_image = image.resize((30, 30))
    photo_dark7 = ImageTk.PhotoImage(resized_image)
    photo_light7 = ImageTk.PhotoImage(resized_image)
#create the dark mood function 
def toggle_theme7():
    global toggle_button7, is_dark_theme7, aboutFrame
    if is_dark_theme7:
        # Switch to light theme
        aboutFrame.config(bg='white')
        toggle_button7.config(image=photo_light7, bg='white')  # Use light theme icon
        is_dark_theme7 = False
    else:
        # Switch to dark theme
        aboutFrame.config(bg='black')
        toggle_button7.config(image=photo_dark7, bg='black')  # Use dark theme icon
        is_dark_theme7 = True  
#create the read text function
def read_aloud():
    global text
    global reading_enabled
    global aboutFrame
    global read_aloud_button
    engine = pyttsx3.init()
    #engine.runAndWait()
    if reading_enabled:
        engine.say(test)
        engine.runAndWait()
        reading_enabled = False
#create the about us page
def about_p():
    global aboutFrame ,toggle_button7,text, text1, text2, text3 ,current_text
    load_images7() 
     #create the frame where all contents will fit in
    aboutFrame =tk.Frame(root, bg="#FFFFFF")
    aboutFrame.place(width=700, height=800, x=0, y=70) 
    # define the long text
    text = ("Welcome to Our Zoo, a sanctuary of wildlife and natural beauty nestled in the heart of our " 
                "community. With a commitment to conservation, education, and unforgettable experiences, " 
                "Riget Zoo Adventure is more than just a place to see animals; it's a journey into the heart of " 
                "the animal kingdom.\n\n"
             "** Our Animals **\n"
             "At RZA, our pride lies in our diverse collection of species from all corners of the globe. From " 
                 "the majestic lions of the African Savanna to the elusive red pandas of the Asian forests," 
                 "each animal at our zoo is cared for with the utmost respect and devotion. Our exhibits " 
                 "are designed to mimic natural habitats, providing our animals with environments that support " 
                 "their health and well-being while offering visitors a glimpse into the world of wildlife.\n\n"
                 "** Our Ambition **\n"
                 "Our ambition is to inspire visitors with the beauty and complexity of the natural world. "
                 "Through immersive exhibits and engaging educational programs, we aim to foster a deeper " 
                 "understanding and appreciation of wildlife and their habitats. Conservation is at the core "
                 "of everything we do. We are dedicated to the protection of endangered species and their " 
                 "natural environments, working closely with local and international conservation organizations to promote biodiversity and sustainability.\n\n"
                 "** Contact Us **\n"
                 "For more information, to plan your visit, or to learn how you can support our conservation" 
                 "efforts, please get in touch:\n"
                 "Email :  RigetZooAdventures@outlook.com \n"
                 "Phone : \n "
                 "Address : \n")

    #label widget with the text, setting a fixed width and enabling word wrap
    label = tk.Label(aboutFrame, text=text, wraplength=650, justify="left", bg="white", fg="black", padx=10, pady=10, font=("Times New Roman", 14))
    label.place(x=5, y=5)
    #logo 
    image1 = Image.open("logo.jpg")
    image1 = image1.resize((325, 150))
    photo = ImageTk.PhotoImage(image1)
    # Create label with the image
    w_photo = Label(aboutFrame, image=photo)
    w_photo.image = photo
    w_photo.place(x=200, y=550)
    #back button 
    storeBackButton = tk.Button(aboutFrame, text="<-", bg="#8FBB6C", command=starter_screen)
    storeBackButton.place(width=70, height=30, y=680, x=18)
    #dark mood button
    toggle_button7 = tk.Button(aboutFrame, image=photo_light7, font=('Helvetica', 24),bg='#8FBB6C', command=toggle_theme7)
    toggle_button7.place(x=5, y=640)
    #load and open to use in read text button
    image = Image.open("auditory.png")
    image_resized = image.resize((30, 30))
    photo1 = ImageTk.PhotoImage(image_resized)
    photoD = tk.Label(aboutFrame, image=photo1)
    photoD.image = photo1

    # Button to read the text aloud
    read_aloud_button = tk.Button(aboutFrame, image=photo1, command=read_aloud, bg="white")
    read_aloud_button.place(x=650, y=640)

#create the educationvisit page and all the functions that need   
is_dark_theme8 = False
photo_dark8 = None
photo_light8 = None
toggle_button8 = None 
#load and open the photos that use in dark mood function
def load_images8():
    global photo_light8, photo_dark8
    # load and resize the icon image for both themes
    image = Image.open("accessibility2.png")
    resized_image = image.resize((30, 30))
    photo_dark8 = ImageTk.PhotoImage(resized_image)
    photo_light8 = ImageTk.PhotoImage(resized_image)
#create the dark mood function
# def toggle_theme8():
#     global toggle_button8, is_dark_theme8, educFrame
#     if is_dark_theme8:
#         # switch to light theme
#         educFrame.config(bg='white')
#         toggle_button8.config(image=photo_light8, bg='white')  # Use light theme icon
#         is_dark_theme8 = False
#     else:
#         # switch to dark theme
#         educFrame.config(bg='black')
#         toggle_button8.config(image=photo_dark8, bg='black')  # Use dark theme icon
#         is_dark_theme8 = True  
#create the read text function
def read_aloud():
    global text
    global reading_enabled
    global educFrame
    global read_aloud_button

    engine = pyttsx3.init()

    if reading_enabled:
        # read the text aloud
        engine.say(text)
        engine.runAndWait()
        reading_enabled = False
# create the educational visit page
def educationvisit_p():
    global educFrame ,toggle_button8,text
    load_images8()
    #create the frame where all contents will fit in
    educFrame =tk.Frame(root, bg="#FFFFFF")
    educFrame.place(width=700, height=800, x=0, y=70) 
    #image
    image1 = Image.open("kids.jpg")
    image1 = image1.resize((700, 130))
    photo = ImageTk.PhotoImage(image1)
    # Create label with the image
    w_photo = Label(educFrame, image=photo)
    w_photo.image = photo
    w_photo.place(x=0, y=0)
    #welcome message
    welcome1 = tk.Label(educFrame, text="Riget Zoo Adventure is dedicated to fostering a deep connection\n between young minds and the wonders of the natural world.", bg="white",font=("Times New Roman", 18), fg="#8FBB6C")
    welcome1.place(x=25, y=135)
    text = ("***School Group***\n"
            "* Tailored Educational Tours: Customized tours aligning with current curriculum standards \n   to enhance "
                 "students' learning on topics such as biodiversity, ecosystems,and \n   conservation efforts.\n"
                 "* Animal Encounters: Close-up encounters with select animals to foster a deeper \n   understanding " 
                 "and appreciation of wildlife.\n"
                 "* Resource Packs: Comprehensive educational materials provided for teachers to integrate \n   the visit "
                "into their lesson plans.\n"
                 "* Safety equipment: helmets for adventure activities within the zoo,sunscreen for outdoor \n   exposure, " 
                 "and hand sanitizers to maintain hygiene \n"
                 "* Book contact us email (RigetZooAdventures@outlook.com)\n\n "
                 "***Home Learning visitors***\n"
                 "* Guided Zoo Tours: Tailored tours led by expert guides to introduce students to the \n   wonders of wildlife.\n"
                 "* 30-Minute Educational Lecture: A concise, engaging lecture on topics like \n   conservation,animal behavior, "
                 "and ecosystems,tailored for young minds.\n"
                 "* Educational Materials: A variety of take-home resources designed to extend learning \n   beyond the visit, "
                 "including activity sheets and fact files..\n"
                 "* Safety equipment: helmets for adventure activities within the zoo,sunscreen for outdoor \n   exposure, and "
                 "hand sanitizers to maintain hygiene \n"
                 "* Book contact us email (RigetZooAdventures@outlook.com) ")

    #Label widget with the text, setting a fixed width and enabling word wrap
    label = tk.Label(educFrame, text=text, wraplength=680, justify="left", bg="white", fg="black", padx=10, pady=10, font=("Times New Roman", 14))
    label.place(x=5, y=190)
    #back button 
    storeBackButton = tk.Button(educFrame, text="<-", bg="#8FBB6C", command=starter_screen)
    storeBackButton.place(width=70, height=30, y=680, x=18)
    
    # toggle_button8 = tk.Button(educFrame, image=photo_light8, font=('Helvetica', 24),bg='#8FBB6C', command=toggle_theme8)
    # toggle_button8.place(x=5, y=640)

    image = Image.open("auditory.png")
    image_resized = image.resize((30, 30))
    photo1 = ImageTk.PhotoImage(image_resized)
    photoD = tk.Label(educFrame, image=photo1)
    photoD.image = photo1
    # Button to read the text aloud
    read_aloud_button = tk.Button(educFrame, image=photo1, command=read_aloud, bg="white")
    read_aloud_button.place(x=650, y=640)

#create the help page and all the functions it need
#create function checks whether the provided frame is currently visible on the screen
def toggle_answer(frame):
    """Toggle the visibility of the answer."""
    if frame.winfo_manager():
        frame.pack_forget()
    else:
        frame.pack(fill=tk.X)
#create function to holds the provided text within a label widge
def create_answer_frame(parent, text):
    """Create a frame that holds the answer and can be toggled."""
    answer_frame = tk.Frame(parent)
    answer_label = tk.Label(answer_frame, text=text, wraplength=500, padx=10)
    answer_label.pack(padx=10, pady=5)
    return answer_frame
#create function for clicking on a question button toggles the visibility of its corresponding answer.
def create_faq_section(help_text):
    """Create an FAQ section with interactive questions."""
    faqs = {
        "> Can I buy tickets for someone else?": "Yes, you can purchase multiple tickets and assign them to different names during the checkout process.",
        "> What should I do if I lose my ticket?": "Contact our support at (RigetZooAdventures@outlook.com) with your purchase details. We can reissue your ticket."
    }
    
    faq_frame = tk.LabelFrame(help_text, text="Frequently Asked Questions", padx=10, pady=10)
    faq_frame.place(width=700, height=200, x=10, y=400)
    
    answer_frames = {}
    for question, answer in faqs.items():
        q_button = tk.Button(faq_frame, text=question, relief=tk.FLAT, anchor="w", padx=10)
        q_button.pack(fill=tk.X)
        answer_frame = tk.Frame(faq_frame, padx=10, pady=5)
        answer_label = tk.Label(answer_frame, text=answer, wraplength=650)
        answer_label.pack()
        answer_frames[question] = answer_frame

        # bind the toggle function to the button command
        q_button.config(command=lambda af=answer_frame: toggle_answer(af))
def read_aloud():
    #global content
    global text
    global reading_enabled
    global helpFrame
    global read_aloud_button
    engine = pyttsx3.init()
    if reading_enabled:
        # Read the text aloud
        engine.say(text)
        engine.runAndWait()
        reading_enabled = False

reading_enabled = True
read_aloud_button = None
#create the help page 
def help_p():
    global text
    global help_text
    global helpFrame
    helpFrame =tk.Frame(root, bg="#FFFFFF")
    helpFrame.place(width=700, height=800, x=0, y=70) 
    # Create a scrolled text widget
    help_text = scrolledtext.ScrolledText(helpFrame, wrap=tk.WORD)
    help_text.pack(fill=tk.BOTH, expand=True)

    # Inserting text into the scrolled text widget
    text = """
    Welcome to the Zoo App Help Page
    --------------------------------
    Our app is designed to enhance your visit by providing detailed information at your fingertips.

    How to Purchase Tickets:
    ------------------------
    1. Create account and then log in 
    2. Navigate to the 'Tickets' section in the main menu.
    3. Select the type of ticket, enter the number of tickets, and proceed to checkout.

    How to Book Room in Hotel:
    --------------------------
    1. Create account and then log in 
    2. Navigate to the 'Plane your visit' section in the main menu then Hotel.
    3. Select the type of room, enter the number of guests, check in ,check out and proceed to checkout.

 
    For further assistance, please contact support at (RigetZooAdventures@outlook.com).
    """
    textL = tk.Label(help_text, text=text, wraplength=650, justify="left", bg="white", fg="black", padx=10, pady=10, font=("Times New Roman", 12))
    textL.place(x=5, y=5)
    create_faq_section(helpFrame)  # Create the interactive FAQ section within the help frame

    image = Image.open("auditory.png")
    image_resized = image.resize((40, 40))
    photo1 = ImageTk.PhotoImage(image_resized)
    photoD = tk.Label(helpFrame, image=photo1)
    photoD.image = photo1
    # button to read the text aloud
    read_aloud_button = tk.Button(helpFrame, image=photo1, command=read_aloud)
    read_aloud_button.place(x=10, y=600)
    # back button to return to the main/starter screen
    back_button = tk.Button(helpFrame, text="<-", bg="#8FBB6C", command=starter_screen)
    back_button.place(width=70, height=30, y=680, x=10)
#create the read text function to used it in help page 

#I did import datetime again because some time code not response 
import datetime    
def grad_date(cal):
    date_str = cal.get_date()
    date_obj = datetime.datetime.strptime(date_str, '%m/%d/%y').date()
    available_tickets = get_ticket_availability(date_obj.strftime('%Y-%m-%d')) 
    # clear previous tags
    cal.calevent_remove('all')
    if available_tickets > 0:
        messagebox.showinfo("Ticket Availability", f"Available tickets for {date_obj}: {available_tickets}")
        cal.calevent_create(date_obj, 'Available', 'available')
        cal.tag_config('available', background='green', foreground='black')
    else:
        messagebox.showinfo("Ticket Availability", f"Tickets for {date_obj} are sold out.")
        cal.calevent_create(date_obj, 'Sold Out', 'sold_out')
        cal.tag_config('sold_out', background='red', foreground='white')
     
#create the buy the ticket page 
def ticket_p():
    #create the frame where all fit in 
    ticketFrame =tk.Frame(root, bg="#FFFFFF")
    ticketFrame.place(width=700, height=800, x=0, y=70) 
    dateLabel = tk.Label(ticketFrame, text = 'Date')
    dateLabel.place(x=10, y=10)
    slotLabel = tk.Label(ticketFrame, text = 'Slot Time')
    slotLabel.place(x=220, y=10)
    # entry bars
    Date = tk.Entry(ticketFrame)
    Date.place(width=150, x=50, y=10)
    SlotTime = tk.Entry(ticketFrame)
    SlotTime.place(width=150, x=290, y=10)
    tk.Label(ticketFrame, text="Availability Date:").place(x=10, y=40)
    # set the calendar to start in 2024
    cal = Calendar(ticketFrame, selectmode='day', year=2024, month=4, day=1)
    cal.place(x=20, y=70)
    #check the avaiblity in calender
    check_availability_button = tk.Button(ticketFrame, text="Check Availability", command=lambda: grad_date(cal))
    check_availability_button.place(x=300, y=150) 
    #function to show the ticket
    ticket_data = get_all_products()
    #print("Ticket data fetched:", ticket_data)
    if not ticket_data:
        print("No ticket data available.")
        return
    ticket_counts = {}
    position = 300  # position to avoid overlap with the calendar

    for item, price in ticket_data.items():
        itemFrame = tk.Frame(ticketFrame, bg="#FFFFFF")
        itemFrame.place(width=700, height=50, x=0, y=position)

        ticketName = tk.Label(itemFrame, text=item)
        ticketPrice = tk.Label(itemFrame, text=f"£{price}")
        
        ticket_counts[item] = 0  # Initialize ticket count for this item
        count_label = tk.Label(itemFrame, text=ticket_counts[item])
        

        def make_update_count(item, count_label):
          def update_count(change):
            new_count = ticket_counts[item] + change
            if new_count < 0:
                new_count = 0  # Prevent negative ticket count
            ticket_counts[item] = new_count
            count_label.config(text=str(new_count))
          return update_count

        update_count = make_update_count(item, count_label)

        increase_button = tk.Button(itemFrame, text="+", command=lambda uc=update_count: uc(1))
        decrease_button = tk.Button(itemFrame, text="-", command=lambda uc=update_count: uc(-1))


        ticketName.place(width=250, height=30, x=5)
        ticketPrice.place(width=60, height=30, x=350)
        decrease_button.place(x=500, y=2)
        count_label.place(x=550, y=2)
        increase_button.place(x=600, y=2)
                                
        position += 60

    print("Ticket purchase screen loaded.")

    position += 60
    #function to encapsulate adding to basket and showing message
    def add_to_basket():
        global profile_id
        profile_id = get_profile_id_by_user_id(_user_id)
        if not profile_id:
         messagebox.showerror("Error", "Please log in to buy the ticket .")
         Account_p()
        else:
         insert_ticket_data(profile_id, Date.get(), SlotTime.get(), ticket_data, ticket_counts)
         messagebox.showinfo("Success", "Your ticket added to basket successfully.")
         basket_p(profile_id)

    BasketButton = tk.Button(ticketFrame, text=" Add To Basket ", bg='#8FBB6C', command=add_to_basket)
    BasketButton.place(width=350, heigh=50, x=190, y=550)

    storeBackButton = tk.Button(ticketFrame, text="<-", bg="#8FBB6C", command=starter_screen)
    storeBackButton.place(width=70, height=30, y=600, x=18)

#I did import datetime again because some time code not response 
import datetime  
#create the function for room type in hotel function
def roomtype_date(cal):
    date_str = cal.get_date()
    date_obj = datetime.datetime.strptime(date_str, '%m/%d/%y').date() 
    # function call to check room availability
    available_single, available_double = get_room_availability(date_obj.strftime('%Y-%m-%d'))
    # clear previous tags
    cal.calevent_remove('all')
    if available_single > 0 or available_double > 0:
        messagebox.showinfo("Room Availability",
                            f"Availability for {date_obj}:\nSingle rooms: {available_single}\nDouble rooms: {available_double}")
        cal.calevent_create(date_obj, 'Available', 'available')
        cal.tag_config('available', background='green', foreground='black')
    else:
        messagebox.showinfo("Room Availability", f"All rooms for {date_obj} are sold out.")
        cal.calevent_create(date_obj, 'Sold Out', 'sold_out')
        cal.tag_config('sold_out', background='red', foreground='white')
    
#create the book room in hotel page 
def roomhotel_p():        
    roomhotelFrame =tk.Frame(root, bg="#FFFFFF")
    roomhotelFrame.place(width=700, height=800, x=0, y=70) 
    checkinLabel = tk.Label(roomhotelFrame, text = 'Check In ')
    checkinLabel.place(x=10, y=10)
    checkoutLabel = tk.Label(roomhotelFrame, text = 'Check Out')
    checkoutLabel.place(x=320, y=10)
    NoGLabel = tk.Label(roomhotelFrame, text = 'Number of Guests ')
    NoGLabel.place(x=320, y=40)
    
    # entry bars
    checkin = tk.Entry(roomhotelFrame)
    checkin.place(width=150, x=80, y=10)
    checkout = tk.Entry(roomhotelFrame)
    checkout.place(width=150, x=430, y=10)
    noG = tk.Entry(roomhotelFrame)
    noG.place(width=150, x=430, y=40)
    
    tk.Label(roomhotelFrame, text="Availability Date:").place(x=10, y=40)
    # set the calendar to start in 2024
    cal = Calendar(roomhotelFrame, selectmode='day', year=2024, month=4, day=1)
    cal.place(x=20, y=70)
    #show the avaiability of room in calender
    check_availability_button = tk.Button(roomhotelFrame, text="Check Availability", command=lambda: roomtype_date(cal))
    check_availability_button.place(x=300, y=150) 
    #function to show the room 
    room_data = get_all_room()
    #print("room data fetched:", room_data)
    if not room_data:
        print("No room data available.")
        return
    room_counts = {}
    position = 300  # position to avoid overlap with the calendar

    for item, bprice in room_data.items():
        bookFrame = tk.Frame(roomhotelFrame, bg="#FFFFFF")
        bookFrame.place(width=700, height=50, x=0, y=position)

        ticketName = tk.Label(bookFrame, text=item)
        ticketPrice = tk.Label(bookFrame, text=f"£{bprice}")
        
        room_counts[item] = 0  # Initialize ticket count for this item
        count_label = tk.Label(bookFrame, text=room_counts[item])
        

        def make_update_count(item, count_label):
          def update_count(change):
            new_count = room_counts[item] + change
            if new_count < 0:
                new_count = 0  # Prevent negative ticket count
            room_counts[item] = new_count
            count_label.config(text=str(new_count))
          return update_count

        update_count = make_update_count(item, count_label)

        increase_button = tk.Button(bookFrame, text="+", command=lambda uc=update_count: uc(1))
        decrease_button = tk.Button(bookFrame, text="-", command=lambda uc=update_count: uc(-1))


        ticketName.place(width=250, height=30, x=5)
        ticketPrice.place(width=60, height=30, x=350)
        decrease_button.place(x=500, y=2)
        count_label.place(x=550, y=2)
        increase_button.place(x=600, y=2)
                                
        position += 60

    print("Ticket purchase screen loaded.")

    position += 60
    # function to encapsulate adding to basket and showing message
    def add_to_basket():
        global profile_id
        profile_id = get_profile_id_by_user_id(_user_id)
        if not profile_id:
         messagebox.showerror("Error", "Please log in to book room in the hotel .")
         Account_p()
        else:
         insert_room_data(profile_id, checkin.get(), checkout.get(), noG.get(), room_data, room_counts)
         messagebox.showinfo("Success", "Your Booking added to basket successfully.")
         basket_p(profile_id)

    BasketButton = tk.Button(roomhotelFrame, text=" Add To Basket ", bg='#8FBB6C', command=add_to_basket)
    BasketButton.place(width=350, heigh=50, x=190, y=550)
    storeBackButton = tk.Button(roomhotelFrame, text="<-", bg="#8FBB6C", command=starter_screen)
    storeBackButton.place(width=70, height=30, y=600, x=18)

#create the basket page to show all items
def basket_p(profile_id): 
    total = 0
    bprice = 0
    total_cost = 0
    total_ticket_price = 0
    total_booking_price = 0
    total_membership = 0

    # create a frame for the basket page
    basketFrame =tk.Frame(root, bg="#FFFFFF")
    basketFrame.place(width=700, height=800, x=0, y=70)

    # header labels
    tk.Label(basketFrame, text="Ticket informations", bg="white").grid(row=0, column=0)
    tk.Label(basketFrame, text="Ticket Type", bg="white").grid(row=1, column=0)
    tk.Label(basketFrame, text="Quantity", bg="white").grid(row=1, column=1)
    tk.Label(basketFrame, text="Price of Ticket", bg="white").grid(row=1, column=2)
    
    tk.Label(basketFrame, text="Booking Room informations", bg="white").grid(row=6, column=0)
    tk.Label(basketFrame, text="Room Type", bg="white").grid(row=7, column=0)
    tk.Label(basketFrame, text="Quantity", bg="white").grid(row=7, column=1)
    tk.Label(basketFrame, text="Days", bg="white").grid(row=7, column=2)
    tk.Label(basketFrame, text="Price of booking", bg="white").grid(row=7, column=3)
    
    tk.Label(basketFrame, text="Membership informations", bg="white").grid(row=13, column=0)
    tk.Label(basketFrame, text="Member Type", bg="white").grid(row=14, column=0)
    tk.Label(basketFrame, text="Price", bg="white").grid(row=14, column=1)
    #functions to fetch all items frome database
    ticket_data = fetch_tickets_since_last_login(profile_id)
    print (ticket_data)
    reward_points = fetch_reward_points(profile_id)
    booking_data = fetch_booking_since_last_login(profile_id)
    membership_data = fetch_membership_since_last_login(profile_id)
    #place the ticket datas 
    ticket_row = 2
    for item, count, tprice in ticket_data:
        if count > 0:
            total = tprice * count
            total_ticket_price += total
            tk.Label(basketFrame, text=item, bg="white").grid(row=ticket_row, column=0)
            tk.Label(basketFrame, text=count, bg="white").grid(row=ticket_row, column=1)
            tk.Label(basketFrame, text=f"£{total}", bg="white").grid(row=ticket_row, column=2)
            ticket_row += 1  # Increment row for next ticket
    # display booking details dynamically
    booking_row = 8 # start after tickets
    for item, count, price, no_days in booking_data:
        if count > 0:
            bprice = price
            total_booking_price += bprice
            tk.Label(basketFrame, text=item, bg="white").grid(row=booking_row, column=0)
            tk.Label(basketFrame, text=count, bg="white").grid(row=booking_row, column=1)
            tk.Label(basketFrame, text=no_days, bg="white").grid(row=booking_row, column=2)
            tk.Label(basketFrame, text=f"£{price}", bg="white").grid(row=booking_row, column=3)
            booking_row += 1  # Increment row for next booking
    # display membership details dynamically
    membership_row = 15 #start after booking room
    for item, price in membership_data:
        #if count > 0:
            total_membership += price
            tk.Label(basketFrame, text=item, bg="white").grid(row=membership_row, column=0)
            tk.Label(basketFrame, text=f"£{price}", bg="white").grid(row=membership_row, column=1)
            membership_row += 1  # increment row for next booking
    
    # calculate and display the total cost and discount
    total_cost = total_ticket_price + total_booking_price + total_membership
    total_cost = round(total_cost, 2)
    discount = calculate_and_show_discount(reward_points, total_cost)
    tk.Label(basketFrame, text="Total Cost:", bg="white").grid(row=max(ticket_row, booking_row) + 19, column=0)
    tk.Label(basketFrame, text=f"£{total_cost}", bg="white").grid(row=max(ticket_row, booking_row) + 19, column=1)
    tk.Label(basketFrame, text="Discount:", bg="white").grid(row=max(ticket_row, booking_row) + 20, column=0)
    tk.Label(basketFrame, text=f"£{discount}", bg="white").grid(row=max(ticket_row, booking_row) + 20, column=1)
    #function to grouping all functions need after click pay button
    def saveF():
        insert_basket_data(profile_id, ticket_data)
        insert_roomtobasket_data(profile_id, booking_data)
        insert_finalpricetobasket_data(profile_id, discount)
        insert_membershiptobasket(profile_id, membership_data)
        Pay_p()
    PayButton = tk.Button(basketFrame, text=" Pay ", bg='#8FBB6C', command=saveF)
    PayButton.place(width=350, heigh=50, x=190, y=550)
    #back button
    storeBackButton = tk.Button(basketFrame, text="<-", bg="#8FBB6C", command=starter_screen)
    storeBackButton.place(width=70, height=30, y=600, x=18)

#create the pay page 
def Pay_p():
    # Create a frame for all to fit in
    payFrame =tk.Frame(root, bg="#FFFFFF")
    payFrame.place(width=700, height=800, x=0, y=70)
    # card information
    paymentlabel = tk.Label(payFrame, text='Card Informations', bg="white", font=("Times New Roman", 24))
    # labels 
    nameOnCardLabel = tk.Label(payFrame, text="Name on card", bg="white")
    cardNumberLabel = tk.Label(payFrame, text="Card number", bg="white")
    cvv2Label = tk.Label(payFrame, text="CVV2", bg="white")
    # entry
    nameOnCard = Entry(payFrame)
    cardNumber = Entry(payFrame)
    cvv2 = Entry(payFrame)
    # layout the label and entery
    paymentlabel.place(width=350, height=100, x=180, y=20)
    
    nameOnCardLabel.place(width=150, x=100, y=130)
    nameOnCard.place(width=200, x=250, y=130)
    
    cardNumberLabel.place(width=150, x=100, y=160)
    cardNumber.place(width=200, x=250, y=160)

    cvv2Label.place(width=150, x=100, y=190)
    cvv2.place(width=200, x=250, y=190)
    # encapsulate adding to basket, showing message and send email with all details
    def saveandclose():
        global email
        ticket_details = fetch_ticket_basket(profile_id)  # function to fetch ticket details
        booking_details = fetch_booking_basket(profile_id) # function to fetch bookin room details
        final_price = fetch_finalprice_basket(profile_id)  # function to fetch final price details
        membership_details = fetch_membership_since_last_login(profile_id) # function to fetch membership details
        ticket_info = "\n".join([f"{item}, Quantity: {count}, Price: £{price}, Date: {date}, Slot Time: {slot_time}"
                             for item, count, price, date, slot_time in ticket_details])
        booking_info = "\n".join([f"{item}, Quantity: {count}, Price: £{price}, Number Days: {Number_Days}, Check in: {Check_in}, Check out: {Check_out}"
                             for item, count, price, Number_Days, Check_in, Check_out in booking_details])
        membership_info = "\n".join([f"{item}, Price: £{price}" for item, price in membership_details])
        finalprice_info = f"Final Price after discount: £{final_price[0][0]}"                     
        email_body = f"Hello {_firstnamr} {_lastname},\n\n" \
                 "Thank you for your purchase. Here are your order details:\n" \
                 f"{ticket_info} \n {booking_info} \n {finalprice_info}\n {membership_info}\n\n" \
                 "We hope you enjoy your visit to Riget Zoo Adventures!"

        email_subject = "Your visit to Riget Zoo Adventures"
        # Send the email
        send_email(_email, email_subject, email_body, "RigetZooAdventures@outlook.com", "12qw##12QW##")
        messagebox.showinfo("Success", "Your payment was successful.")
        close_p()
    # Pay button
    payButton = tk.Button(payFrame, text="Pay",bg='#8FBB6C', command=saveandclose)
    payButton.place(width=350, height=50, x=150, y=400)

#create function to close the app
def close_window():
    root.destroy()
#create the close page
def close_p():
  # create a frame for fit all in it
  CFrame =tk.Frame(root, bg="#FFFFFF")
  CFrame.place(width=700, height=800, x=0, y=70)
  # create a label with a message
  message_label = tk.Label(CFrame, text="THANKS", bg="white", font=("Times New Roman", 24))
  message_label.place(width=350, height=50, x=200, y=50)

  message_label2 = tk.Label(CFrame, text="You will recive an Email", bg="white", font=("Times New Roman", 24))
  message_label2.place(width=350, height=50, x=200, y=100)

  message_label1 = tk.Label(CFrame, text="with all information", bg="white", font=("Times New Roman", 24))
  message_label1.place(width=350, height=50, x=200, y=150)

 # Create a Close button
  close_button = tk.Button(CFrame, text="Close",bg='#8FBB6C', command=close_window)
  close_button.place(width=350, height=50, x=200, y=480)

if __name__ == "__main__":
    starter_screen()