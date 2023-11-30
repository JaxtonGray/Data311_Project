# Reference code: https://www.sqlitetutorial.net/sqlite-python/creating-tables/

import sqlite3
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
    # Connect to the database
    con = sqlite3.connect("twitter_like.db")
    cur = con.cursor()

    # Ask user for username and password
    username = input("Username: ")
    password = input("Password: ")

    # Check to see if username matches, keep repeating until username matches
    userCheck = True # Flag for if username is taken
    while userCheck:
        cur.execute("SELECT Username FROM UserProfiles WHERE Username = ?", (username,))
        if cur.fetchone() is None: # If the username does not exist in the database
            print("Username does not exist. Please try again.")
            username = input("Username: ")
        else: # Otherwise, the username exists in the database
            userCheck = False # Set flag to false to exit loop
    
    # Check to see if password matches, keep repeating until password matches
    passCheck = True # Flag for if password is correct
    while passCheck:
        cur.execute("SELECT Password FROM UserProfiles WHERE Username = ?", (username,))
        if cur.fetchone()[0] != password:
            print("Password is incorrect. Please try again.")
            password = input("Password: ")
        else:
            passCheck = False
    
    # Get the UserID of the user
    cur.execute("SELECT UserID FROM UserProfiles WHERE Username = ?", (username,))
    userID = cur.fetchone()[0]

    con.close()

    return userID

# Posting New Tweets # Samin
def post_tweet(user_id, tweet_content):
    # Validation for tweet content
    if not tweet_content:
        print("Tweet content cannot be empty.")
        return
    if len(tweet_content) > 280:  # Twitter's character limit
        print("Tweet exceeds the maximum character limit of 280.")
        return

    try:
        cursor.execute("INSERT INTO Tweets (UserID, TweetContent) VALUES (?, ?)", (user_id, tweet_content))
        conn.commit()
        print("Tweet posted successfully.")
    except sqlite3.Error as tweet_post_error:
        print("Error occurred while posting the tweet:", tweet_post_error)

# Viewing User's Timeline # Samin

# Liking tweets # Anthony
def like_tweet(user_id, tweet_id):
    # Connect to the database
    conn = sqlite3.connect("twitter_like.db")
    cursor = conn.cursor()

    # Check if the user has already liked the tweet
    cursor.execute("SELECT * FROM LikesRetweets WHERE UserID = ? AND TweetID = ?", (user_id, tweet_id))
    existing_like = cursor.fetchone()

    if existing_like:
        print("You have already liked this tweet.")
    else:
        # Insert a new record into the LikesRetweets table
        cursor.execute("INSERT INTO LikesRetweets (UserID, TweetID) VALUES (?, ?)", (user_id, tweet_id))
        conn.commit()
        print("You have liked the tweet successfully.")

    # Close the connection
    conn.close()

# Show number of likes on Tweet # Anthony
def display_tweet_likes (tweet_id):
    conn = sqlite3.connect("twitter_like.db")
    cursor = conn.cursor()

    # Retrieve user IDs who liked the specified tweet
    cursor.execute("SELECT UserID FROM LikesRetweets WHERE TweetID = ?", (tweet_id,))
    likes = cursor.fetchall()

    if likes:
        print(f"Likes for Tweet ID {tweet_id}:")
        for like in likes:
            print(f"User ID: {like[0]}")
    else:
        print("No likes found for this tweet.")

    conn.close()
    
# Comments on Tweets # Samin
def post_comment(user_id, tweet_id, comment_text):
    try:
        cursor.execute("INSERT INTO Comments (UserID, TweetID, CommentText) VALUES (?, ?, ?)", (user_id, tweet_id, comment_text))
        conn.commit()
        print("Comment posted successfully.")
    except sqlite3.Error as comment_post_error:
        print("Error occurred while posting comment:", comment_post_error)

#viewing comments on a tweet
def view_comments(tweet_id):
    try:
        cursor.execute("SELECT UserProfiles.Username, Comments.CommentText FROM Comments JOIN UserProfiles ON Comments.UserID = UserProfiles.UserID WHERE TweetID = ?", (tweet_id,))
        comments = cursor.fetchall()

        if comments:
            for comment in comments:
                print(f"{comment[0]} commented: {comment[1]}")
        else:
            print("No comments on this tweet.")
    except sqlite3.Error as view_comment_error:
        print("Error occurred while fetching comments:", view_comment_error)

# Following and Unfollowing Users # Jax

# CLI Menu # Anthony
def CLI_Menu(choice):
    while True:
        print("Twitter-Like CLI Application")
        print("1. Post a Tweet")
        print("2. View Timeline")
        print("3. Like a Tweet")
        print("4, View Tweet Likes")
        print("5. View Tweet Comments")
        print("6. Follow a User")
        print("7. Unfollow a User")
        print("8. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
        # Handle posting a tweet
            pass
        elif choice == '2':
        # Handle viewing the timeline
            pass
        elif choice == '3':
        # Handle liking a tweet
            user_id = 1 # replace with actual user id
            tweet_id = 1 # replace with tweet id
            like_tweet(user_id,tweet_id) # if "3" is chosen, call the like_tweet function
        elif choice == '4':
        # Handle showing number of likes of tweet
            tweet_id = 1
            display_tweet_likes(tweet_id)
        elif choice == '5':
        # Handle viewing tweet comments
            pass
        elif choice == '6':
        # Handle following a user
            pass
        elif choice == '7':
        # Handle unfollowing a user
            pass
        elif choice == '8':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")
# Help feature and Documentation # Jax