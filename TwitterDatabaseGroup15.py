# Reference code: https://www.sqlitetutorial.net/sqlite-python/creating-tables/

# this is a test
import sqlite3

def sql (database):
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


# User Registration and Login

# Posting New Tweets
# Viewing User's Timeline
# Liking tweets
# Showing the number of Likes of Tweets
# Comments on Tweets
# Following and Unfollowing Users 

# CLI Menu
def CLI_Menu (choice):
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
# Help feature and Documentation
            