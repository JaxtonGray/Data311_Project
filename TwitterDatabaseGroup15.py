# Reference code: https://www.sqlitetutorial.net/sqlite-python/creating-tables/

# this is a test
import sqlite3
#Test


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

# Posting New Tweets # Samin
# Viewing User's Timeline # Samin
# Liking tweets # Anthony
def like_tweet(user_id,tweet_id):
    try:
        # See if user has already liked tweet
        cursor.execute("SELECT * FROM LikesRetweets WHERE UserID = ? AND TweetID = ?", (user_id,tweet_id))
        existing_like = cursor.fetchone()

        if existing_like:
            print("You've already liked this tweet.")
        else:
            cursor.execute("INSERT INTO LikesRetweets (UserID, TweetID)", (user_id,tweet_id))
            conn.commit()
            print("You have successfully liked the tweet.")
    except sqlite3.Error as like_tweet_error:
        print("Errpr occured while liking tweet",like_tweet_error)
        
# Showing the number of Likes of Tweets # Anthony
    
# Comments on Tweets # Samin
def post_comment(user_id, tweet_id, comment_text):
    try:
        cursor.execute("INSERT INTO Comments (UserID, TweetID, CommentText) VALUES (?, ?, ?)", (user_id, tweet_id, comment_text))
        conn.commit()
        print("Comment posted successfully.")
    except sqlite3.Error as comment_post_error:
        print("Error occurred while posting comment:", comment_post_error)

# Following and Unfollowing Users # Jax

# CLI Menu # Anthony
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
# Help feature and Documentation # Jax
            