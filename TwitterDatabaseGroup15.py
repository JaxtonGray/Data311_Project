# Reference code: https://www.sqlitetutorial.net/sqlite-python/creating-tables/

import sqlite3

def sql(database):
    # Create a new SQLite database (or connect to an existing one)
    conn = sqlite3.connect("twitter_like.db")
    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    # Create User Profiles table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS UserProfiles (
    UserID INTEGER PRIMARY KEY,
    Username TEXT UNIQUE NOT NULL,
    Password TEXT NOT NULL,
    FullName TEXT,
    Email TEXT,
    ProfileImage TEXT,
    RegistrationDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

# Create Tweets table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Tweets (
    TweetID INTEGER PRIMARY KEY,
    UserID INTEGER,
    TweetContent TEXT,
    CreationTimestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (UserID) REFERENCES UserProfiles(UserID)
    )
    ''')

# Create Followers/Following table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS FollowersFollowing (
    FollowID INTEGER PRIMARY KEY,
    FollowerUserID INTEGER,
    FollowingUserID INTEGER,
    FOREIGN KEY (FollowerUserID) REFERENCES UserProfiles(UserID),
    FOREIGN KEY (FollowingUserID) REFERENCES UserProfiles(UserID)
    )
    ''')

# Create Likes/Retweets table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS LikesRetweets (
    LikeRetweetID INTEGER PRIMARY KEY,
    UserID INTEGER,
    TweetID INTEGER,
    FOREIGN KEY (UserID) REFERENCES UserProfiles(UserID),
    FOREIGN KEY (TweetID) REFERENCES Tweets(TweetID)
    )
    ''')

# Create Comments table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Comments (
    CommentID INTEGER PRIMARY KEY,
    UserID INTEGER,
    TweetID INTEGER,
    CommentText TEXT,
    CommentTimestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (UserID) REFERENCES UserProfiles(UserID),
    FOREIGN KEY (TweetID) REFERENCES Tweets(TweetID)
    )
    ''')

# Commit changes and close connection
    conn.commit()
    conn.close()


# User Registration and Login # Jax
def user_registration():
    # Connect to the database
    con = sqlite3.connect("twitter_like.db")
    cur = con.cursor()

    # Greet new user and ask for user registrationn information
    username = input("Username: ")
    password = input("Password: ") ###NOTE: Figure out password hashing????

    # Check to see if username already exists within database, if so then ask for a new one
    userCheck = True # Flag for if username is taken
    while userCheck:
        cur.execute("SELECT Username FROM UserProfiles WHERE Username = ?", (username,))
        if cur.fetchone() is None: # If the username does not exist in the database
            userCheck = False # Set flag to false to exit loop
        else: # Otherwise, the username exists in the database
            print("Username already exists. Please select a different username.")
            username = input("Username: ")

    # Ask for user's full name and email and proifle image link
    fullname = input("Full Name: ")
    email = input("Email: ")
    profileImage = input("Profile Image Link: ")

    # Generate a unique user ID
    cur.execute("SELECT MAX(UserID) FROM UserProfiles") # Get the highest UserID
    userID = cur.fetchone()[0] # Fetch the highest UserID
    if userID is None: # If there are no users in the database
        userID = 1 # Set the UserID to 1
    else:
        userID += 1 # Otherwise, increment the UserID by 1 to generate new highest UserID

    # Insert user information into the database
    cur.execute("""
                INSERT INTO UserProfiles (UserID, Username, Password, FullName, Email, ProfileImage) VALUES (?, ?, ?, ?, ?, ?)
                """, (userID, username, password, fullname, email, profileImage))
    con.commit() # Commit changes to the database
    con.close() # Close connection to the database
def user_login():
    pass
# Posting New Tweets # Samin
# Viewing User's Timeline # Samin
# Liking tweets # Anthony
# Showing the number of Likes of Tweets # Anthony
# Comments on Tweets # Samin
# Following and Unfollowing Users # Jax

# CLI Menu # Anthony
def CLI_Menu(choice):
    while True:
        print("Twitter-Like CLI Application")
        print("1. Post a Tweet")
        print("2. View Timeline")
        print("3. Like a Tweet")
        print("4. View Tweet Comments")
        print("5. Follow a User")
        print("6. Unfollow a User")
        print("7. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
        # Handle posting a tweet
            pass
        elif choice == '2':
        # Handle viewing the timeline
            pass
        elif choice == '3':
        # Handle liking a tweet
            pass
        elif choice == '4':
        # Handle viewing tweet comments
            pass
        elif choice == '5':
        # Handle following a user
            pass
        elif choice == '6':
        # Handle unfollowing a user
            pass
        elif choice == '7':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")
# Help feature and Documentation # Jax
