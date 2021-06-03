import sqlite3

connection = sqlite3.connect('login_data.db', check_same_thread = False)
cursor = connection.cursor()

cursor.execute(
    """CREATE TABLE users(
     pk INTEGER PRIMARY KEY AUTOINCREMENT,
     username VARCHAR(16),
     password VARCHAR(32),
     email VARCHAR(32),
     date TEXT
    );"""
)

connection.commit()
cursor.close()
connection.close()


connection = sqlite3.connect('tasks.db', check_same_thread = False)
cursor = connection.cursor()

cursor.execute(
    """CREATE TABLE tasks(
     pk INTEGER PRIMARY KEY AUTOINCREMENT,
     username VARCHAR(16),
     email VARCHAR(32),
     subject VARCHAR(32),
     memo VARCHAR(1000),
     status VARCHAR(16),
     date TEXT
    );"""
)

connection.commit()
cursor.close()
connection.close()


connection = sqlite3.connect('news.db', check_same_thread = False)
cursor = connection.cursor()
cursor.execute(
    """CREATE TABLE mails(
     pk INTEGER PRIMARY KEY AUTOINCREMENT,
     email VARCHAR(32),
     date TEXT
    );"""
)

connection.commit()
cursor.close()
connection.close()
