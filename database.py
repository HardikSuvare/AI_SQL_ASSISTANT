import sqlite3

conn = sqlite3.connect("college.db")

cursor = conn.cursor()

cursor.execute(""" Create Table students (ID int,Name varchar(30),python int,DBMS int,Percentage varchar(30),City varchar(30))""")

cursor.execute(""" INSERT INTO students VALUES(1,'Hardik',90,85,'90%','Mumbai')""")

cursor.execute(""" INSERT INTO students VALUES(2,'Rahul',80,70,'75%','Pune')""")

cursor.execute(""" INSERT INTO students VALUES(3,'Asmita',95,92,'95%','Mumbai')""")

cursor.execute(""" INSERT INTO students VALUEs(4,'Ramesh',75,65,'80%','Pune')""")

conn.commit()

print("Data Inserted")