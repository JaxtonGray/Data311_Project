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
    email = input("Email: ")
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

    # Check to see if email already exists within database, if so then ask for a new one
    emailCheck = True # Flag for if email is taken
    while emailCheck:
        cur.execute("SELECT Email FROM UserProfiles WHERE Email = ?", (email,))
        if cur.fetchone() is None:
            emailCheck = False
        else:
            print("Email already exists. Please select a different email.")
            email = input("Email: ")

    # Ask for user's full name and proifle image link
    fullname = input("Full Name: ")
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
    # Connect to database
    conn = sqlite3.connect("twitter_like.db")
    cursor = conn.cursor()
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

    # Close the database connection
    conn.close()

def view_timeline(user_id):
    try:
        conn = sqlite3.connect("twitter_like.db")
        cursor = conn.cursor()

        cursor.execute("SELECT FollowingUserID FROM FollowersFollowing WHERE FollowerUserID = ?", (user_id,))
        following_users = cursor.fetchall()

        if not following_users:
            print("You are not following any users, or no follow data found.")
            return

        print("Following User IDs:", [fu[0] for fu in following_users])  # Debug print

        for (following_user_id,) in following_users:
            cursor.execute("SELECT TweetContent, CreationTimestamp FROM Tweets WHERE UserID = ? ORDER BY CreationTimestamp DESC", (following_user_id,))
            tweets = cursor.fetchall()

            if tweets:
                print(f"Timeline for User {following_user_id}:")
                for tweet in tweets:
                    print(f"{tweet[1]}: {tweet[0]}")
            else:
                print(f"No tweets found for User {following_user_id}")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()


# Liking tweets # Anthony
def like_tweet(user_id, tweet_id):
    # Connect to database
    conn = sqlite3.connect("twitter_like.db")
    cursor = conn.cursor()

    while True:
        # Check if the tweet exists in the database
        cursor.execute("SELECT * FROM Tweets WHERE TweetID = ?", (tweet_id,))
        tweet_exists = cursor.fetchone()

        if tweet_exists:
            # Check if the user has already liked the tweet
            cursor.execute("SELECT * FROM LikesRetweets WHERE UserID = ? AND TweetID = ?", (user_id, tweet_id))
            existing_like = cursor.fetchone()

            if existing_like:
                print("You have already liked this tweet.")
            else:
                # Insert a new like for the tweet
                cursor.execute("INSERT INTO LikesRetweets (UserID, TweetID) VALUES (?, ?)", (user_id, tweet_id))
                conn.commit()
                print("You have liked the tweet successfully.")

            conn.close()
            break
        else:
            # If the tweet ID does not exist, prompt the user to retry or exit
            print("The tweet ID does not exist.")
            retry = input("Would you like to retry? (Y/N): ")
            if retry.lower() != 'y':
                conn.close()
                break
            tweet_id = input("Enter the Tweet ID to like: ")

# Show number of likes on Tweet # Anthony
def display_tweet_likes(tweet_id):
    # Connect to the database
    conn = sqlite3.connect("twitter_like.db")
    cursor = conn.cursor()

    while True:
        # Check if the tweet exists in the database
        cursor.execute("SELECT * FROM Tweets WHERE TweetID = ?", (tweet_id,))
        tweet_exists = cursor.fetchone()

        if tweet_exists:
            # Fetch and display likes for the tweet
            cursor.execute("SELECT UserProfiles.Username FROM LikesRetweets "
                           "INNER JOIN UserProfiles ON LikesRetweets.UserID = UserProfiles.UserID "
                           "WHERE LikesRetweets.TweetID = ?", (tweet_id,))
            likes = cursor.fetchall()

            if likes:
                print(f"Likes for Tweet ID {tweet_id}:")
                for like in likes:
                    print(f"User: {like[0]}")
            else:
                print("No likes found for this tweet.")

            conn.close()
            break
        else:
            # If the tweet ID does not exist, prompt the user to retry or exit
            print("The tweet ID does not exist.")
            retry = input("Would you like to retry? (Y/N): ")
            if retry.lower() != 'y':
                conn.close()
                break
            tweet_id = input("Enter the Tweet ID to view likes: ")
    
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

    # Close the database connection
    conn.close()

# Following and Unfollowing Users # Jax
def follow_unfollow(logged_in_user, target_user_id, action):
    # Connect to the database
    conn = sqlite3.connect("twitter_like.db")
    cursor = conn.cursor()

    while True:
        # Check if the target user ID exists in the database
        cursor.execute("SELECT * FROM UserProfiles WHERE UserID = ?", (target_user_id,))
        user_exists = cursor.fetchone()

        if user_exists:
            # Prevent users from following themselves
            if logged_in_user == target_user_id and action == "follow":
                print("Error: You cannot follow yourself.")
            else:
                if action == "follow":
                    # Check if the user is already following the target user
                    cursor.execute("SELECT * FROM FollowersFollowing WHERE FollowerUserID = ? AND FollowingUserID = ?",
                                   (logged_in_user, target_user_id))
                    already_following = cursor.fetchone()

                    if already_following:
                        print("You are already following this user.")
                    else:
                        # Follow the target user
                        cursor.execute("INSERT INTO FollowersFollowing (FollowerUserID, FollowingUserID) VALUES (?, ?)",
                                       (logged_in_user, target_user_id))
                        conn.commit()
                        print("You have followed the user successfully.")

                elif action == "unfollow":
                    # Check if the user is following the target user
                    cursor.execute("SELECT * FROM FollowersFollowing WHERE FollowerUserID = ? AND FollowingUserID = ?",
                                   (logged_in_user, target_user_id))
                    already_following = cursor.fetchone()

                    if already_following:
                        # Unfollow the target user
                        cursor.execute("DELETE FROM FollowersFollowing WHERE FollowerUserID = ? AND FollowingUserID = ?",
                                       (logged_in_user, target_user_id))
                        conn.commit()
                        print("You have unfollowed the user successfully.")
                    else:
                        print("You are not following this user.")

            conn.close()
            break
        else:
            # If the target user ID does not exist, prompt the user to retry or exit
            print("Invalid user ID. The user does not exist.")
            retry = input("Would you like to retry? (Y/N): ")
            if retry.lower() != 'y':
                conn.close()
                break
            target_user_id = input("Enter the User ID: ")

# CLI Menu # Anthony
def CLI_Menu():
    # Log in or register loop
    isLogged_in = False
    while not isLogged_in:
        print("\nTwitter-Like CLI Application")
        print("1. Log In")
        print("2. Register")
        choice = input("Enter your choice: ")

        if choice == '1':
            logged_in_user = user_login()
            isLogged_in = True
        else:
            user_registration()


    while True:
        print("\nTwitter-Like CLI Application")
        print(f"Logged in as User ID: {logged_in_user} \n")
        print("1. Post a Tweet")
        print("2. View Timeline")
        print("3. Like a Tweet")
        print("4, View Tweet Likes")
        print("5. View Tweet Comments") # Added view likes option
        print("6. Follow a User")
        print("7. Unfollow a User")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
        # Handle posting a tweet
            tweet_content = input("Enter your tweet: ")
            post_tweet(logged_in_user, tweet_content)

        elif choice == '2':
        # Handle viewing the timeline
            view_timeline(logged_in_user)

        elif choice == '3':
        # Handle liking a tweet
            tweet_id = input("Enter the Tweet ID to like: ")
            like_tweet(logged_in_user, tweet_id) 

        elif choice == '4':
        # Handle showing number of likes of tweet
            tweet_id = input("Enter the Tweet ID to view likes: ")
            display_tweet_likes(tweet_id) 

        elif choice == '5':
        # Handle viewing tweet comments
            tweet_id = input("Enter the Tweet ID to view comments: ")
            view_comments(tweet_id)

        elif choice == '6':
        # Handle following a user
            target_user_id = input("Enter User ID to follow: ")
            follow_unfollow(logged_in_user, target_user_id, "follow")

        elif choice == '7':
        # Handle unfollowing a user
            target_user_id = input("Enter User ID to unfollow: ")
            follow_unfollow(logged_in_user, target_user_id, "unfollow")

        elif choice == '8':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")

# Help feature and Documentation # Jax



CLI_Menu()