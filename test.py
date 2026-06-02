import sqlite3

conn = sqlite3.connect("college.db")

cursor = conn.cursor()

cursor.execute(
    "SELECT * FROM students"
)

result = cursor.fetchall()

print(result)