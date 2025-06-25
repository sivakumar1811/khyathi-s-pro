import sqlite3

conn = sqlite3.connect('database.db')  # or the filename your app uses
cursor = conn.cursor()

# Create tables example
cursor.execute('''
CREATE TABLE IF NOT EXISTS departments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);
''')

# Add other tables your app needs here

conn.commit()
conn.close()

print("Database created successfully.")
