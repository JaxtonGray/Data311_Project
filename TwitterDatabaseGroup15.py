# Reference code: https://www.sqlitetutorial.net/sqlite-python/creating-tables/

# this is a test
import sqlite3

def sql (database):
    # Create a new SQLite database (or connect to an existing one)
    conn = sqlite3.connect("twitter_like.db")
    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    # Create a table for user profiles
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_profiles (
    user_id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    full_name TEXT,
    email TEXT,
    profile_image TEXT,
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Create a table for tweets
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tweets (
    tweet_id INTEGER PRIMARY KEY,
    user_id INTEGER FOREIGN KEY,
    tweet_content TEXT NOT NULL,
    creation_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Create a table for followers_or_following
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS followers_or_following (
    follow_id INTEGER PRIMARY KEY,
    follower_user_id INTEGER FOREIGN KEY,
    following_user_id INTEGER FOREIGN KEY
    )
    ''')

    # Create a table for likes_or_retweets
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS likes_or_retweets (
    like_or_retweet_id INTEGER PRIMARY KEY,
    user_id INTEGER FOREIGN KEY,
    tweet_id INTEGER FOREIGN KEY,
    )
    ''')

    # Create a table for comments
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS comments (
    comment_id INTEGER PRIMARY KEY,
    user_id INTEGER FOREIGN KEY,
    tweet_id INTEGER FOREIGN KEY,
    comment_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Commit the changes and close the connection
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
            