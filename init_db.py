import sqlite3

conn = sqlite3.connect('database.db')
print("Opened database successfully");

# conn.execute('CREATE TABLE users (ID INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, addr TEXT, city TEXT, pin TEXT)')
conn.execute('CREATE TABLE users (ID INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, addr TEXT)')
print("Table created successfully");
conn.close()
