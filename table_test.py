import sqlite3

# Connect to the database (creates a new file if it doesn't exist)
conn = sqlite3.connect('mydatabase.db')
cursor = conn.cursor()

# Create the Users table
cursor.execute('''CREATE TABLE IF NOT EXISTS Users
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   first_name TEXT NOT NULL,
                   last_name TEXT NOT NULL,
                   username TEXT NOT NULL,
                   password TEXT NOT NULL,
                   email TEXT NOT NULL,
                   age INTEGER NOT NULL,
                   phone TEXT NOT NULL)''')

# Commit the changes
conn.commit()

# Get a list of all tables in the database
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables in the database:")
for table in tables:
    print(table[0])

# Get information about the Users table
cursor.execute("PRAGMA table_info('Users')")
columns = cursor.fetchall()
print("\nUsers table structure:")
for column in columns:
    print(column)

# Close the database connection
conn.close()